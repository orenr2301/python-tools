import docker
import time
import json
from datetime import datetime, timedelta, timezone

class DockerManager:
    def __init__(self):
        self.client = docker.from_env()
        
    def list_containers(self):
         return self.client.containers.list()
     
    def list_all_containers(self):
        return self.client.containers.list(all=True)
    
    def run_test_container(self):
        container = self.client.containers.run(
            name="test-web-container",
            image="nginx:alpine",
            detach=True,
            environment={"NGINX_HOST": "localhost" },
            labels={"run": "test", "type": "checker"},
            user="nginx",
        )
        return f"Container {container.name} ({container.short_id}) deployed . . .\n please free to test"
    
    def 
    
    