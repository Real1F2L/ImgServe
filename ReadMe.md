# ImgServe
**Thank you for checking out ImgServe!**

The goal is to revolutionize how we serve images online to save time and data.

ImgServe is a free and open source image serving API that can Cache, Resize, and Reformat images on the fly!

## Features
- Easily and Quickly resize images
- Resize and change bitrate for videos
- Switch to modern format webp
- Store edited images for future use

## Examples of Resizing
![Size 64](https://shareapi.gegeha.com/download?size=64&file=images/index/chopper/3.png)
![Size 128](https://shareapi.gegeha.com/download?size=128&file=images/index/chopper/3.png)
![Size 256](https://shareapi.gegeha.com/download?size=256&file=images/index/chopper/3.png)

![Size 64](https://shareapi.gegeha.com/download?size=64&file=images/index/chopper/2.png)
![Size 128Size 128](https://shareapi.gegeha.com/download?size=128&file=images/index/chopper/2.png)
![Size 256](https://shareapi.gegeha.com/download?size=256&file=images/index/chopper/2.png)

![Size 64](https://shareapi.gegeha.com/download?size=64&file=images/index/chopper/1.png)
![Size 128](https://shareapi.gegeha.com/download?size=128&file=images/index/chopper/1.png)
![Size 256](https://shareapi.gegeha.com/download?size=256&file=images/index/chopper/1.png)

#### each of these images are from the same website, using the same image!

## Table of How-To-Install 
- [Installation](#Installation)
  - [Windows](#Installation-on-windows)
  - [Linux](#Installation-on-Linux)
  - [Docker](#Installation-In-Docker)
    - [Docker-compose.yml](#Using-dockercompose.yml)
    - [Docker command](#Using-Docker-Command)
- [Usage](#usage)
- [License](#license)

# Installation

### Installation on windows

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/ImgServe.git
  cd ImgServe
  ```
2. Edit config.json
3. Run Start.bat! It will auto-install packages and open the script

### Installation on Linux

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/ImgServe.git
  cd ImgServe
  ```
2. Create a new virtual environment (optional):
 ```bash
 python -m venv .venv
 ```
3. Install packages:
 ```bash
 python -m pip install -r requirements.txt
 ```
4. Edit config.json
5. Run __init__.py
  ```bash
  python Scripts/__init__.py
  ```

## Installation In Docker

### Using dockercompose.yml

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/ImgServe.git
  cd ImgServe
  ```
3. Edit the the docker-compose.yml
4. Edit config.json
5. Create the container:
 ```Bash
 docker-compose up -d --no-recreate
 ```

### Using Docker Command

1. Clone the repository:
  ```bash
  git clone https://github.com/yourusername/ImgServe.git
  cd ImgServe
  ```

2. Edit config.json

3. Create a new image using the DockerFile and start the container:

 ```bash
 docker build -t imgserve:1.0.0 . && \
 docker run -d \ 
   --name imgserve \
   --restart unless-stopped \
   -p 8080:80 \
   -v ./:/app/ \         # Mount current directory to /app
   -v ./Files/:/Files/   # Folder containing the files you want to share
   imgserve:1.0.0
 ```
 
## Usage
1. Install latest version of [Python](https://www.python.org/downloads/)
2. Follow the instructions at [Installation](#Installation)

## License
- You may:
  - Use ImgServe
  - Distribute ImgServe
  - Edit and modify ImgServe (You must state changes if you distribute)
- You may NOT under any circumstances:
  - Sell ImgServe
  - Claim credit for ImgServe

## Contact
- Business Email: [business@gegeha.com](mailto:business@gegeha.com)
- Discord: [1f2l](https://discord.com/users/686579767813734412)
- [Join my Discord Server](https://discord.com/invite/RHt7wvmfEp)
