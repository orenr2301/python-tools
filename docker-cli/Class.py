import docker
import time
import json
from datetime import datetime, timedelta, timezone

class DockerCli:
    def __init__(self):
        self.client = docker.from_env()
        self.