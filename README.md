This repo is going to give you the basic idea about Dockerization.
All the instructions and explaining will be in this README file.

# Hello Docker

## Run
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