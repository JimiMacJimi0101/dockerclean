import time
import docker

client = docker.DockerClient(base_url='tcp://118.244.195.128:2375')

while True:
    containers = client.containers.list(all=True)
    for container in containers:
        if "mts" not in container.name:
            try:
                container.stop()
                container.remove()
                print(f"Stopped and removed container: {container.name}")
            except docker.errors.APIError as e:
                print(f"Error stopping/removing container {container.name}: {e}")
    
    time.sleep(5)  # Pause for 5 seconds before the next iteration
