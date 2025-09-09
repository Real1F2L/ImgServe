# ImgServe
**Thank you for checking out ImgServe!**

The goal is to revolutionize how we serve images online to save time and data.

ImgServe is a free and open source image serving API that can Cache, Resize, and Reformat images on the fly!

## Features
- Efficiently resize and request images
- Use any image format
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

#### All of these images are from the same file, resized to whatever I like it to be!

## Table of How-To-Install 
- [ImgServe](#imgserve)
  - [Features](#features)
  - [Examples of Resizing](#examples-of-resizing)
      - [All of these images are from the same file, resized to whatever I like it to be!](#all-of-these-images-are-from-the-same-file-resized-to-whatever-i-like-it-to-be)
  - [Table of How-To-Install](#table-of-how-to-install)
- [Installation](#installation)
    - [Installation on Linux](#installation-on-linux)
  - [Installation In Docker](#installation-in-docker)
    - [Using Docker Compose](#using-docker-compose)
    - [Using Docker Command](#using-docker-command)
  - [Usage](#usage)
  - [Contact](#contact)

# Installation

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
4. Edit config.json to fit your setup
5. Run main.py
  ```bash
  python main.py
  ```

## Installation In Docker

### Using Docker Compose

1. Clone the repository:
  ```bash
  git clone https://github.com/Real1F2L/ImgServe.git ImgServe
  cd ImgServe
  ```
3. Edit docker-compose.yml to fit your setup
4. Edit config.json to fit your setup
5. Create the container:
 ```Bash
 docker-compose up -d
 ```

### Using Docker Command

1. Clone the repository:
  ```bash
  git clone https://github.com/Real1F2L/ImgServe.git ImgServe
  cd ImgServe
  ```

2. Edit config.json to fit your setup

3. Create a new image using the DockerFile and start the container:

 ```bash
 docker build -t imgserve:1.1.0 . && \
 docker run -d \ 
   --name imgserve \
   --restart unless-stopped \
   -p 8080:80 \
   -v ./:/ImgServe \
   -v /path/to/folder-you-want-to-share/:/ImgServe/Files/ \
   imgserve:1.1.0
 ```
 
## Usage
1. Install latest version of [Python](https://www.python.org/downloads/)
2. Follow the instructions at [Installation](#Installation)
3. ImgServe is an API that is entirely operated by URL query
  - For example: `[Your IP Address]:[Your Port]/image/resize?f=image.webp&s=128x128&t=png` will return image.webp resized to 128x128 as a png
    
  - There are multiple subdirectories with different queries you can use:
     - `/image/resize` Returns a resized version of a image
       - `f` The file location of the image
       - `s` The image size of the response (in the format 120x120)
       - `t` The file type of the response
       - `ar` Maintain aspect ratio (defaults to yes, setting this to anything but "y" makes it no)
     - `/image/download` Returns a raw image
       - `f` The file location of the image
     - And more to come...

## Contact
- Business Email: [business@gegeha.com](mailto:business@gegeha.com)
- Discord: [1f2l](https://discord.com/users/686579767813734412)
- [Discord Server](https://discord.com/invite/RHt7wvmfEp)