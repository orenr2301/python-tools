import docker
from datetime import datetime, timezone, timedelta

client = docker.from_env()


#! Configs

IMAGE_MAX_DAYS = 7
CONTAINER_MAX_AGE_HOURS= 24
PROTECTED_IMAGES = ["postgres", "redis", "registry"]


def cleanup_stooped_containers(max_age_hours):
    
    removed = 0
    cutoff = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
    
    containers = client.containers.list(
        all=True,
        filters={
            "status": "exited"
        }
    )
    
    for container in containers:
        finished = container.attrs["State"]["FinishedAt"]
        finished_dt = datetime.fromisoformat(finished.replace("Z", "+00:00"))
        
        if finished_dt < cutoff:
            print(f"Removing container {container.name} (stopped {finished})")
            container.remove(v=False)
            
    return removed

def cleanup_unused_images(max_age_days):
    
    removed = 0
    reclaimed_bytes = 0
    cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
    
    images = client.images.list()
    
    ## Skip dangled images with no tags
    for image in images:
        tags = image.tags
        if not tags:
            continue
        
        ## Skip protected
        if any(p in tag for tag in tags for p in PROTECTED_IMAGES):
            continue
        
        created = datetime.fromisoformat(
            image.attrs["Created"].replace("Z", "+00:00")
        )
        
        if created < cutoff:
            ## Check if image is used by any container
            try:
                containers = client.containers.list(
                    all=True,
                    filters={
                        "ancestor": image.id
                    }
                )
                if containers:
                    continue
            except Exception:
                continue
        
        size = image.attrs["Size"]
        print(f"Removing images {tags[0]} ({size / 1024 / 1024:.2f} MB)")
        try:
            client.images.remove(image.id, force=True)
            removed += 1
            reclaimed_bytes += size
        except docker.errors.APIError as e:
            print(f" Skipped: {e}")
            
    return removed, reclaimed_bytes


def cleanup_dangling_images():
    result = client.images.prune(filters={"dangling": True})
    deleted = len(result.get("ImagesDeleted", []))
    reclaimed = result.get("SpaceReclaimed", 0)
    return deleted, reclaimed

def cleanup_orphand_volumes():
    result = client.volumes.prune()
    deleted = len(result.get("VolumesDeleted", []) or [])
    reclaimed = result.get("SpaceReclaimed", 0)
    return deleted, reclaimed


def main():
    
    print("Cleaning up stopped containers...")
    removed_containers = cleanup_stooped_containers(CONTAINER_MAX_AGE_HOURS)
    print(f"Removed {removed_containers} stopped containers")
    
    print("\nCleaning up unused images...")
    removed_images, reclaimed_bytes = cleanup_unused_images(IMAGE_MAX_DAYS)
    print(f"Removed {removed_images} images, reclaimed {reclaimed_bytes / 1024 / 1024:.2f} MB")
    
    print("\nCleaning up dangling images...")
    deleted_dangling, reclaimed_dangling = cleanup_dangling_images()
    print(f"Removed {deleted_dangling} dangling images, reclaimed {reclaimed_dangling / 1024 / 1024:.2f} MB")
    
    print("\nCleaning up orphaned volumes...")
    deleted_volumes, reclaimed_volumes = cleanup_orphand_volumes()
    print(f"Removed {deleted_volumes} orphaned volumes, reclaimed {reclaimed_volumes / 1024 / 1024:.2f} MB")
    
    total_reclaimed = reclaimed_bytes + reclaimed_dangling + reclaimed_volumes
    print(f"\nTotal reclaimed space: {total_reclaimed / 1024 / 1024:.2f} MB")
    
if __name__ == "__main__":
    main()