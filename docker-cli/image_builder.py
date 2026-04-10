import docker
import json
import time

client = docker.from_env()

print("Building image. . . . .")

image, build_logs = client.images.build(
    path=".",
    tag="myapp:latest",
    nocache=True,
    buildargs={
        "APP_VERSION": "1.0.0",
        "MAINTAINER": "John Doe"
    },
    labels={
        "build_date": time.strftime("%Y-%m-%dT%H:%M:%S"),
    },
    rm=True,
    dockerfile="Dockerfile",
)


## Stream and build logs
for log_entry in build_logs:
    if 'stream' in log_entry:
        print(log_entry['stream'].strip())
    elif 'error' in log_entry:
        print(f"ERROR: {log_entry['error']}")
        
        
print(f"\nBuilt image: {image.tags}")
print(f"Image ID: {image.short_id}")
print(f"Size: {image.attrs['Size'] / 1024/ 1024:.2f} MB")


