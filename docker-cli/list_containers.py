import docker



client = docker.from_env()


## list running container

running = client.containers.list()
print(f"Running Containers: {len(running)}")

for c in running:
    print(f" - {c.name} ({c.short_id}) - Status: {c.status} - Network: {c.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']} - Image: {c.image.tags[0] if c.image.tags else 'untagged'}")
    
## All containers Inlcuding stooped 
all_containers = client.containers.list(all=True)
print(f"All Containers: {len(all_containers)}")
   

## Label Filtering 

team_containers = client.containers.list(
    filters={
        "label": "teams=platform"
    }
)

print(f"Platfrom team containers: {len(team_containers)}")


## By Status 
exited = client.containers.list(
    all=True,
    filters={
        "status": "exited"
    }
)
print(f"Exited containers: {len(exited)}")



