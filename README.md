This repo is going to give you the basic idea about Dockerization.

All the instructions and explaining are in this README file.

# Hello Docker

## Prepare
You need to install some tools to follow the instructions bellow:

1. Docker Commnunity Edition (required): you should follow [this link](https://docs.docker.com/install/linux/docker-ce/ubuntu/) to install.
2. Python 3.6.8 (optional for coding): I coded this demo on this version of python. Although the demo is just a another helloworld app. But i'm not sure it will run correctly on your machine. Consider to install Python 3.6.8 or use `pyenv` to switch the python bin.  
3. Pipenv (optional for coding): Instead of pip, I use Pipenv. So please use it to manage the dependencies. Follow this link to install or simply try `pip install pipenv`
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