import disco
from disco.core.constants import JobStatus
import pathlib
from disco.docker_image import DockerImage

#we will timeout if the job ran for over 5 minutes
#this is up to your application and change it accordingly
LIVE_TESTS_TIMEOUT_SECONDS = 300

DISCO_EMAIL = 'ray_ifx@dis.co'
DISCO_PASSWORD = 'impact123'

disco.set_credentials(DISCO_EMAIL, DISCO_PASSWORD, save_to_config=True)

#list of docker images we got
i = 0
docker_images = DockerImage.list_docker_images()
for docker_image in docker_images:
    print("================================================================")
    print("Selection Number: "+str(i))
    print("ID: "+str(docker_image.id))
    print("Name: "+str(docker_image.name))
    print("Is Active: "+str(docker_image.is_active))
    print("Repository Type: "+str(docker_image.repository_type))
    print("================================================================")
    i = i + 1

print("Please Select Your Docker Image. Enter the number 0, 1, 2, 3, ...")
selection = input()
docker_id = DockerImage.list_docker_images()[int(selection)].id


#this will upload a simple server script and runs the tasks
script_id = disco.upload_file('server.py', pathlib.Path('./server.py'))
input_file_ids = [disco.upload_file('task1.txt', pathlib.Path('./task1.txt')), disco.upload_file('task2.txt', pathlib.Path('./task2.txt'))]


#create the job with the scripts and input files
job = disco.Job.create(script_id, input_file_ids, docker_image_id=docker_id)
job.start()


print(f'Waiting for job {job.job_id} to finish...')
job.wait_for_status(JobStatus.done, interval=5, timeout=LIVE_TESTS_TIMEOUT_SECONDS)
print(f'job {job.job_id} finished!')

print('Waiting for the jobs results')
task_results = job.get_results(block=True)

print('Finished getting the results')
task_result_outputs = [task_result.stdout for task_result in task_results]
print ("Task Results Outputs")

for task_result in task_results: 
    task_result.write_files("./")
