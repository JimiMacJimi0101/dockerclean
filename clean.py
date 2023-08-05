import subprocess
import sys

def stop_and_remove_containers(docker_host, container_names_to_keep):
    # Get the list of all container IDs
    container_ids = subprocess.check_output(['docker', '-H', docker_host, 'ps', '-aq'], encoding='ascii')
    container_ids = container_ids.strip().split()

    # Filter out container IDs based on their names
    container_ids_to_remove = []
    for container_id in container_ids:
        container_name = subprocess.check_output(['docker', '-H', docker_host, 'inspect', '-f', '{{.Name}}', container_id], encoding='ascii').strip()
        if container_name not in container_names_to_keep:
            container_ids_to_remove.append(container_id)

    # Stop and remove containers
    if container_ids_to_remove:
        for container_id in container_ids_to_remove:
            # Stop the container
            subprocess.check_call(['docker', '-H', docker_host, 'stop', container_id])
            # Get the name of the container
            container_name = subprocess.check_output(['docker', '-H', docker_host, 'inspect', '-f', '{{.Name}}', container_id], encoding='ascii').strip()
            # Remove the container
            subprocess.check_call(['docker', '-H', docker_host, 'rm', container_id])
            # Print the name of the removed container
            print(f'Removed container: {container_name}')

if __name__ == '__main__':
    # Parse command line arguments
    docker_host = sys.argv[1]
    container_names_to_keep = sys.argv[2:]

    # Stop and remove containers
    stop_and_remove_containers(docker_host, container_names_to_keep)
