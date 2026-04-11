import docker
import time
import logging
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)

client = docker.from_env()

#! Configs
CHECK_INTERVAL = 30
MAX_RESTART_ATTEMPTS = 3 
restart_counts = {}


def check_container_health(container):
    container.reload()
    name = container.name
    status = container.status
    
    if status != "running":
        logger.warning(f"Container '{name}' is not running (status: {status}). Attempting to restart...")
        return False
    
    health = container.attrs.get("State", {}).get("Health", {})
    if health:
        health_status = health.get("State", "none")
        if health_status == "unhealthy":
            logger.warning(f"{name} is unhealthy")
            
            health_log = health.get("Log", [])
            if health_log:
                last_check = health_log[-1]
                logger.warning(f"Warning:{name} is unhealthy. Last health check: {last_check}")

            return False

## Check resources stat

    stats = container.stats(stream=False)
    cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                stats["precpu_stats"]["cpu_usage"]["total_usage"]
    system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                   stats["precpu_stats"]["system_cpu_usage"]
    cpu_percent = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0
    
    mem_usage = stats["memory_stats"].get("usage", 0)
    mem_limit = stats["memory_stats"].get("limit", 1)
    mem_percent = (mem_usage / mem_limit) * 100.0
    
    logger.info(f"{name}: CPU={cpu_percent:.2f}%, MEM={mem_percent:.2f}%")
    
    
    if mem_percent > 90:
        logger.warning(f"{name} memory usage is critically high: {mem_percent:.2f}%")
    
    return True




def restart_container(container):
    """Restart the container and track restart attempts, Prevnting loops"""
    name = container.name
    count = restart_counts.get(name, 0)
    
    if count >= MAX_RESTART_ATTEMPTS:
        logger.error(f"Container {name} has been restarted {count} times. Manual intervension is needed")
        return False
    
    logger.info(f"Resatarting {name} (attempt {count + 1})/{MAX_RESTART_ATTEMPTS}")
    container.restart(timeout=30)
    restart_counts[name] = count + 1
    return True

def main():
    
    logger.info("Starting Docker Health Monitor. . . ")
    
    while True:
        try:
            containers = client.containers.list(
                filters={
                    "label": "monitor=true"
                }
            )
            
            if not containers:
                #! Set Fallback
                containers = client.containers.list()
                
                
            for container in containers:
                try:
                    healthy = check_container_health(container)
                    if not healthy:
                        restart_container(container)
                except Exception as e:
                    logger.error(f"Error checking {container.name}: {e}") 
                
        except Exception as e:
            logger.error(f"Monitor error: {e}")
            
        time.sleep(CHECK_INTERVAL)
                
if __name__ == "__main__":
    main()