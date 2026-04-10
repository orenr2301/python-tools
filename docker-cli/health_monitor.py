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
        if he
        