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
![Size 64](https://imgserve.gegeha.com/download?size=64&file=images/index/chopper/3.png)
![Size 128](https://imgserve.gegeha.com/download?size=128&file=images/index/chopper/3.png)
![Size 256](https://imgserve.gegeha.com/download?size=256&file=images/index/chopper/3.png)

![Size 64](https://imgserve.gegeha.com/download?size=64&file=images/index/chopper/2.png)
![Size 128Size 128](https://imgserve.gegeha.com/download?size=128&file=images/index/chopper/2.png)
![Size 256](https://imgserve.gegeha.com/download?size=256&file=images/index/chopper/2.png)

![Size 64](https://imgserve.gegeha.com/download?size=64&file=images/index/chopper/1.png)
![Size 128](https://imgserve.gegeha.com/download?size=128&file=images/index/chopper/1.png)
![Size 256](https://imgserve.gegeha.com/download?size=256&file=images/index/chopper/1.png)

#### Each of these images are from the same [website](https://www.gegeha.com), using the same image!

## Table of How-To-Install 
- [Installation](#Installation)
  - [Windows](#Installation-on-windows)
  - [Linux](#Installation-on-Linux)
  - [Docker](#Installation-In-Docker)
    - [docker-compose.yml](#using-docker-compose)
    - [Docker command](#Using-Docker-Command)
- [Usage](#usage)
- [License](#license)

# Installation

### Installation on windows

1. Clone the repository:
  ```bash
  git clone https://github.com/Real1F2L/ImgServe.git ImgServe
  cd ImgServe
  ```
2. Edit config.json
3. Run Start.bat! It will auto-install packages and open the script

### Installation on Linux

1. Clone the repository:
  ```bash
  git clone https://github.com/Real1F2L/ImgServe.git ImgServe
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

### Using Docker Compose

1. Clone the repository:
  ```bash
  git clone https://github.com/Real1F2L/ImgServe.git ImgServe
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
  git clone https://github.com/Real1F2L/ImgServe.git ImgServe
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
   -v ./Files/:/app/Files/   # Folder containing the files you want to share
   -v ./config.json:/app/config.json # Mount config file so it live updates
   imgserve:1.0.0
 ```
 
## Usage
1. Install latest version of [Python](https://www.python.org/downloads/)
2. Follow the instructions at [Installation](#Installation)
3. ImgServe is an API that is entirely operated by URL query
  - For example: `[Your IP Address]:[Your Port]/searchFiles?folder=Projects/` will return all the files inside of "Projects/"
    
  - There are multiple subdirectories you can call from:
     - `/searchFiles` Returns JSON describing all the files inside a directory
     - `/get-file-contents` Returns a PlainTextResponse that contains the inside of a text file
     - `/download` Returns a file (Used for requesting images)
     - `/display-video` Returns a StreamingResponse (Used for playing resized videos)
     - And more to come...
   
  - There will soon be a deeper visual How-To on my [website](https://www.gegeha.com)

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
