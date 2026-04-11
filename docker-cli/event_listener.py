import docker
import json
from datetime import datetime


client = docker.from_env()


def handle_event(event):
    
    action = event.get("Action", "")
    actor = event.get("Actor", "")
    attributes = event.get("Attributes", {})
    name = attributes.get("name", "unknown")
    image = attributes.get("image", "unknown")
    
    timestamp = datetime.fromtimestamp(event.get("time", 0))
    
    print(f"[{timestamp}] {action}: {name} ({image})")
    
    if action == "die":
        exit_code = attributes.get("exitCode", "unknown")
        if exit_code != "0":
            print(f" WARNING: Container {name} exited with code {exit_code}")
            
    elif action == "oom":
        print(f" WARNING: Container {name} was killed due to out of memory, exited with code {exit_code}")
    
    elif action == "start":
        try:
            container = client.containers.get(actor["ID"])
            labels = container.labels
            if "team" not in labels:
                print(f"NOTICE: Container {name} is missing the 'team' label")
        except Exception:
            pass
        
def main():
    print(f"Listening for docker events...")
    for event in client.events(decode=True):
       try:
            handle_event(event)
       except Exception as e:
           print(f"Error handling event: {e}")
           
if __name__ == "__main__":
    main()