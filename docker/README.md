# Use the Docker of the deepbots

## In case you would like to add other functionalities/libraries on the docker:

* Edit the Dockerfile
* Build the docker image using below commands
* Building argument ```branch``` specify the ```dev``` or the ```master``` branch of deepbots.

### Building and tagging a Docker image:
```bash
$ docker build -t yourusername/repository-name --build-arg branch=dev .
```

## Pull the existing image from DockerHub

```bash
$ docker pull nickok/deepbots-dev
```

## For the use of Cuda on your docker container

You should install NVIDIA Container Toolkit on your ```host``` machine.

1) Setup the stable repository and the GPG key:
``` bash
$ distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```
2) Install the nvidia-docker2 package (and dependencies) after updating the package listing:

``` bash
$ sudo apt-get update
```

``` bash
$ sudo apt-get install -y nvidia-docker2
```

Restart the Docker daemon to complete the installation after setting the default runtime:
``` bash
$ sudo sudo systemctl restart docker
```



## Run docker

### Use docker with ```cpu```
Mount Webots project and run it on interactive Docker container:
```bash
$ docker run -it -v /absolute/path/to/webots/project:/workspace/name-of-project nickok/deepbots-dev
```

### Use docker with ```cuda``` (GPU)
``` bash
$ docker run --rm --gpus all run -it -v /absolute/path/to/webots/project:/workspace/name-of-project nickok/deepbots
```

After starting the docker container you can start Webots headlessly using xvfb:
```bash
$ xvfb-run webots --stdout --stderr --batch --no-sandbox --mode=fast /path/to/your/world/file

```

Start Webots headlessly using xvfb and save the output at out.txt:
```bash
$ xvfb-run webots --stdout --stderr --batch --no-sandbox --mode=fast /path/to/your/world/file &> out.txt &
```