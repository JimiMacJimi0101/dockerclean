import sys
import subprocess
import time

def cleanup_remote_containers(remote_host, containers_to_keep):
    while True:
        # Get a list of all container names on the remote host
        all_containers = subprocess.check_output(["docker", "-H", remote_host, "ps", "-aq"], universal_newlines=True).splitlines()

        # Loop through all containers and stop/delete those that aren't in the keep list
        for container in all_containers:
            container_name = subprocess.check_output(["docker", "-H", remote_host, "inspect", "-f", "{{.Name}}", container], universal_newlines=True).strip("/")
            if container_name not in containers_to_keep:
                print(f"Stopping and deleting container on {remote_host}: {container_name}")
                subprocess.run(["docker", "-H", remote_host, "stop", container])
                subprocess.run(["docker", "-H", remote_host, "rm", container])
            else:
                print(f"Skipping container on {remote_host}: {container_name} (protected)")

        print("Cleanup complete.")
        time.sleep(3600)  # Delay for 1 hour before the next cleanup

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <remote_host>")
        sys.exit(1)

    remote_host = sys.argv[1]
    containers_to_keep = ["redis", "nexus", "mysql", "mongo", "mts"]
    
    cleanup_remote_containers(remote_host, containers_to_keep)
