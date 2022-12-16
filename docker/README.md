# Using deepbots with Docker
## Pull the existing image from [DockerHub](https://hub.docker.com/u/aidudezzz)
* Docker image without conda:
   ```bash
   docker pull aidudezzz/deepbots:0.1.3.dev3
   ```
   * You could replace `0.1.3.dev3` with another available tag: https://hub.docker.com/r/aidudezzz/deepbots/tags
* Docker image without conda:
   ```bash
   docker pull aidudezzz/deepbots-conda:0.1.3.dev3
   ```
   * You could replace `0.1.3.dev3` with another available tag: https://hub.docker.com/r/aidudezzz/deepbots-conda/tags
## Build and tag a Docker image:
You could replace `aidudezzz/deepbots:0.1.3.dev3` with another name and optionally add a tag in the 'name:tag' format.
* Docker image without conda:
   ```bash
   docker build -t aidudezzz/deepbots:0.1.3.dev3 --build-arg branch=dev .
   ```
* Docker image without conda:
   ```bash
   docker build -t aidudezzz/deepbots-conda:0.1.3.dev3 . --build-arg branch=dev --build-arg conda==true
   ```
In case you would like to add other functionalities/libraries on the Docker image:
* Edit the Dockerfile
* Build the Docker image
* Building arguments
   * `branch`
      * `dev`: Install [the latest version of deepbots on TestPyPI](https://test.pypi.org/search/?q=deepbots).
      * `main`: Install [the latest version of deepbots on PyPI](https://pypi.org/project/deepbots/).
      * `github`: Install from [the dev branch of deepbots on GitHub](https://github.com/aidudezzz/deepbots/tree/dev).
   * `conda`
      * `true`: Install miniconda.
## Use CUDA on your Docker container
You should install NVIDIA Container Toolkit on your ```host``` machine.

1) Setup the stable repository and the GPG key:
``` bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
   && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
   && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
```
2) Install the nvidia-docker2 package (and dependencies) after updating the package listing:

``` bash
sudo apt-get update
```

``` bash
sudo apt-get install -y nvidia-docker2
```

Restart the Docker daemon to complete the installation after setting the default runtime:
``` bash
sudo sudo systemctl restart docker
```

## Run a Docker container from the image

### Use Docker with CPU
Mount Webots project and run it on interactive Docker container:
```bash
docker run -it -v /absolute/path/to/webots/project:/workspace/name-of-project <user-name>/<repo-name>
```

### Use Docker with CUDA (GPU)
``` bash
docker run --rm --gpus all run -it -v /absolute/path/to/webots/project:/workspace/name-of-project <user-name>/<repo-name>
```

After starting the Docker container you can start Webots headlessly using xvfb:
```bash
xvfb-run webots --stdout --stderr --batch --mode=fast /path/to/your/world/file

```

Start Webots headlessly using xvfb and save the output at out.txt:
```bash
xvfb-run webots --stdout --stderr --batch --mode=fast /path/to/your/world/file &> out.txt &
```