This repo is going to give you the basic idea about Dockerization.

All the instructions and explaining are in this README file.

# Hello Docker

## Prepare
You need to install some tools to follow the instructions bellow:

1. Docker Commnunity Edition (required): you should follow [this link](https://docs.docker.com/install/linux/docker-ce/ubuntu/) to install.
2. Python 3.6.8 (optional for coding): I coded this demo on this version of python. Although the demo is just a another helloworld app. But i'm not sure it will run correctly on your machine. Consider to install Python 3.6.8 or use `pyenv` to switch the python bin.  
3. Pipenv (optional for coding): Instead of pip, I use Pipenv. So please use it to manage the dependencies. Follow [this link](https://github.com/pyenv/pyenv#installation) to install or simply try `pip install pipenv`
> I'm using Ubuntu to handle this demo. So may there are differences from your system. 

## What is docker? Image? Container?
1. Docker is a technology that allows you virtualizing,  running and isolating your application.
For simple understanding, consider Docker just as like as "another" Virtualbox, VMware. You install Docker. You run your application on Docker, that's it!

2. Docker image is a file that contains application, the Operation System's dependencies. All things are packaged in one image. The PS4 needs the disc to play the game, so Docker needs the image to run the application.

3. A container is a machine instance which is virtualized and created by Docker. When it's running, you can log in, manipulated inside it like a real machine. You play an PS4 game, you're in the digital 3D world of the game. You run a container, you're in the virtual machine.

## Two ways to dockerize an app
There are two ways to run an application on Docker:

### 1. make the app fit to the container

- The most important thing to care about is CONFIGURATION.
- You have to review all lines of code to know which lines are configurable.
- Change the config function for accepting two sources of configuration: ENV variables and the config file. Two sources have to stay in the right priority: env first, config file after.
- You use the config file for the development state. And use the ENV vars for production state. Remember that you cannot change the config file in an image, container. Because the docker image must be immutable.
> Actually you can manipulate the container, exec commands to change a file inside it. But don't fall in this trap. Remember Docker will help us save time for deployment because it does the deployment process automatically. You don't want to waste time on a physical machine, you also don't want to waste time on virtual Docker machine too.

### 2. make the container fit to the app 
- Again, the configuration is important here.
- Check out your code, find all its own configuration files.
- Build a script which run and adapts the value from the ENV into config files you found above.
- So in this way, you don't change you codes. You build (coding) another adapter to collect the configuration from ENV.  
> There is another way to run application. You make a instance of the OS first, Ubuntu, CentOS, etc. Then you "log-in" to this instance, then install and do many things need to run the application. But let remember it's a bad idea, it's anti-pattern of Docker.

## Run this demo
1. You need to build the image first:
```bash
docker build -t demopythondocker .
```
> -t consider as tag name (image's name)

2. Run the image as an container:
```bash
docker run -d --rm -e "APP_NAME=app01" -e "APP_BIND=0.0.0.0" -p "8080:8080" 
```
Then access this link on your browser. You should see: "Hello World from app01"

## How do I make this app more dockernized?
I'm going explaining my process in the first way above, make the app fit the container.

### The first step, check the configable lines:

Let take a look at the line [app.py:9](https://github.com/hostingwithdocker/demopythondocker/blob/readme/app.py#L9)
```python
resp.body = ('Hello World from %s' % cfg('app', 'name'))
```
It gets app's name via the function `cfg()` in [config.py](https://github.com/hostingwithdocker/demopythondocker/blob/readme/config.py#L9)

I decided to make this function more docker, by changing from:
```python
def cfg(section, key, casting=str):
    #configParser read the config from "config.ini"
    return casting(configParser.get(section, key))
```
to this:
```python
def cfg(section, key, casting=str):
    var_env = str(section+"_"+key).upper()
    # Give the environment variable a shot before using the config file
    if var_env in os.environ:
        return os.environ[var_env]
        
    return casting(configParser.get(section, key))
```

As you see, I check the env var first then only take config file if env empty.

Now, this app accepts config value from env and also the `config.ini` on my local code base.

### The second step, write Dockerfile to build image
You need a file which is called Dockerfile. In this file, you write down all the step that docker needs to follow to build an image.
You can find more about Dockerfile [format here](https://docs.docker.com/engine/reference/builder/).

The purpose of building image is packaging all required things to run the app. Include the source codes, OS dependencies, etc.


```Dockerfile
# To start the build process, 
# insert the image of a Linux machine (Alpine OS) which preinstalled python 3.6.8
# You can find all image you need at hub.docker.com  
FROM python:3.6.8-alpine3.9

# Set this ENV var for pipenv. It helps Pipenv know it must create the virtualenv inside the project directory 
ENV PIPENV_VENV_IN_PROJECT=1

# Set the working directory
WORKDIR /app

# Copy the source code from the project dir into the directory app/ inside the container.
COPY ./ /app

# Run some initial command to make the container environmment best fit for the app
RUN apk update && apk add bash tzdata &&\
    cp /usr/share/zoneinfo/Asia/Singapore /etc/localtime &&\
    pip install --upgrade setuptools pip wheel pipenv &&\
    pipenv install

# Tell Docker expose the the port of the application. 
# This is the internal port of the container
# Don't confuse with the port of the host (the physical machine)
EXPOSE 8080

# CMD tell docker run this command everytime it starts the container.
CMD ["/bin/bash","/app/run-container.sh"]
```

You also need add a `.dockerignore` file. This one will help docker know what files should be ignore when copy source code to the container.
```
.git/
.idea
.venv/
__pycache__/
*.pyc
*.swp
config.ini
```

### Build your image
When you have `Dockerfile` and `.dockerignore`, let's build the image:
```bash
docker built -t demopythondocker:1.0.0 .
```
This command will make the image with name "demopythondocker:1.0.0", or if you don't specify the version, Docker will auto names it "demopythondocker:latest".
The image name also known as `tag`, the number after `:` known as the version of the image.   
Notice the dot "." at the end of the above command, it's a path to the directory for Dockerfile.

### Run the app on Docker
```bash
docker run -d \
    -e "APP_NAME=app01" \
    -e "APP_BIND=0.0.0.0" \
    -p 8080:8080 \
    --name mydemo \
    demopythondocker:latest
```

The command above run the image `demopythondocker:latest` under the name `mydemo`.
It also gives the configurations via the env by place `-e`.
Finally, It publishes the container port to the physical machine's port via `-p`.

Once the container run up, you can control it by some commands:
```bash
# List the running container on the system
docker ps 

# List all container, include the stop containers
docker ps -a

# Stop the container by its name, also give the container's id here
docker stop mydemo

# Start the container
docker start mydemo

# Or restart the container
docker restart mydemo
```