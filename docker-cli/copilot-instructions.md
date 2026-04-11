# Copilot Instructions for `docker-cli`

## Overview
This directory contains Python CLI tools and classes for managing Docker containers, images, and events using the Docker SDK for Python. Each script is focused on a specific aspect of Docker management (e.g., cleanup, health monitoring, event listening, image building).

## Key Conventions
- **Python 3** is required. Use a virtual environment for dependencies.
- All scripts use the `docker` Python package (`pip install docker`).
- Scripts are intended to be run directly (not as a package/module).
- Logging and print statements are used for output and status.
- Error handling is present for Docker daemon connectivity and missing dependencies.

## Directory Structure
- `Class.py`: (WIP) Class-based Docker client abstraction.
- `cleanup.py`: Remove old containers/images based on age.
- `connect.py`: Print Docker server info.
- `contianer_mamangment.py`: Start and inspect a sample container.
- `event_listener.py`: Listen for Docker events and print status.
- `health_monitor.py`: Monitor container health and restart if needed.
- `image_builder.py`: Build Docker images from a Dockerfile.
- `list_containers.py`: List containers by status, label, and network info.
- `Dockerfile`: Minimal Alpine-based image for running a Python HTTP server.

## Build & Test
- No unified test or build command; run scripts individually:
  - `python3 scriptname.py`
- Ensure Docker daemon is running and accessible by your user.
- For development, use the provided `Dockerfile` to build a test image if needed.

## Common Pitfalls
- Docker daemon must be running and accessible (permissions may be required).
- The `docker` Python package must be installed in your environment.
- Some scripts assume the presence of specific images (e.g., `nginx:alpine`).
- Network and label filters are case-sensitive.

## Extending
- Add new scripts for additional Docker management tasks.
- Follow the pattern of using `docker.from_env()` and handling exceptions for robust scripts.

## Example Prompts
- "List all running containers and their IP addresses."
- "Remove all stopped containers older than 24 hours."
- "Build a Docker image from the current directory."
- "Monitor container health and restart unhealthy containers."

---
For more details, see individual script files in this directory.
