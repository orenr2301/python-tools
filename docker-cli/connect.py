import docker


client = docker.from_env()

info = client.info

print(f"Docker version: {info['ServerVersion']}")
print(f"Containers running: {info['ContainerRunning']}")
print(f"Images: {info['Images']}")



