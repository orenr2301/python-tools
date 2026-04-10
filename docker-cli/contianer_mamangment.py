import docker
import sys
import time
import json

try:
    import docker
    from docker.errors import DockerException
except ModuleNotFoundError as exc:
    print("Missing dependency: install the Docker SDK for Python with:")
    print("    pip install docker")
    raise SystemExit(1) from exc

try:
    client = docker.from_env()
except DockerException as exc:
    print("Could not connect to the Docker daemon.")
    print("Make sure Docker is running and that your user has permission to access it.")
    print("On Linux, add your user to the 'docker' group or run this script with sudo.")
    print(f"Details: {exc}")
    raise SystemExit(1) from exc

container = client.containers.run(
    "nginx:alpine",
    name="web_server",
    ports={"80/tcp": 8080},
    detach=True,
    environment={"NGINX_HOST": "localhost"},
    labels={"app": "web", "team": "platform"},
)

print(f"Started container: {container.name} ({container.short_id})")

# Wait for start
time.sleep(2)

# Getting container details
container.reload()

network = json.dumps(container.attrs['NetworkSettings'], indent=2)


print(network)

# for network_name, network_config in network.items():
#     ip_address = network_config.get('IPAddress')
#     if ip_address:
#         print(f"Container IP address on network '{network_name}': {ip_address}")
    
    
print(f"Container status: {container.status}") 
print(f"IP: {container.attrs['NetworkSettings']['Networks']['bridge']['IPAddress']}")

## Executing command
exit_code, output = container.exec_run("nginx -v")
print(f"Nginx version: {output.decode().strip()}")

## Get Container logs 
logs = container.logs(tail=10).decode()
print(f"Recents logs:\n{logs}")

#! Stop and removing container
container.stop(timeout=10)
container.remove()
print("Container stopped and removed")


