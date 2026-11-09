# ImgServe

 ImgServe is an image library API built for developers. Allowing you to request any size or type of file on demand, caching generated results for faster repeat access, and providing a simple web UI for quick access to your images.

 It is designed for self-hosting and works well as a simple image backend for websites and apps that require grabbing images from the internet. ImgServe has proven to increase web performance and page build times, scoring higher on Cloudflare and Chrome evaluations than pages without ImgServe.

 ## Features
 - Create a publicly available image Library
 - Store many types of images: SVG, PNG, JPG, WEBP, BMP
 - Browse files and directories in the web UI
 - Resize images at any time
 - Convert images to compressed, request efficient formats
 - Download raw files directly from the library
 - Cache resized output for resource optimization
 - Self-host in Docker

 ## Setting Up The Container with Docker Compose

 1. Clone the repository
 ```bash
 git clone https://github.com/Real1F2L/ImgServe.git ImgServe

 cd ImgServe
 ```

 2. Clone the example config if you have not already:

 ```bash
 cp Options.yml.example Options.yml
 ```

 3. Start the app with Docker Compose:

 ```bash
docker compose up -d --build
 ```

 `docker-compose.yml` is included in the project files.

 ImgServe, by default, runs on port 8080. Proxypass it through your webserver or portforward it (not recommended) to make your images available on the internet.

 ## API usage

 The app exposes REST endpoints under `/api/v1/`.

### Routes:
- `/api/v1/get-img/download` - download a raw image file from the library
  - `f`: relative path to the image to download

- `/api/v1/get-img/convert` - convert an image to a different supported format
  - `f`: relative path to the image
  - `t`: output type (`png`, `jpg`, `webp`, `bmp`)

- `/api/v1/get-img/resize` - resize and optionally convert an image
  - `f`: path to the image relative to the library root
  - `w`: target width in pixels
  - `h`: target height in pixels
  - `t`: output type (`png`, `jpeg`, `jpg`, `webp`, `bmp`, or `keep`)
  - You can provide width or height. If both are provided the larger is used. Aspect ratio is always maintained.

- `/api/v1/folder-search` — list all files and folders inside a library directory
  - `f`: relative path, cannot be a file

- `/api/v1/file-search` — get data on a specific file
  - `f`: relative path to file

- `/api/v1/data/library-file-counts` - get statistics on files in the library
  - No parameters required
  - Statistics update periodically as per config

 ## Notes

 - Image metadata such as location may be served through this API, ensure you know what your putting online
 - ImgServe does **NOT** automatically make your images public to the internet, the ImgServe port must be proxypassed or portforwarded to be available. ImgServe **DOES** make your images available to the local network.

 ## Contact
 - Business Email: [business@gegeha.com](mailto:business@gegeha.com)
 - Discord: [1f2l](https://discord.com/users/686579767813734412)