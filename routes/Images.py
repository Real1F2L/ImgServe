# Image requesting routes

import mimetypes, io
#
from pathlib import Path
from PIL import Image
from fastapi import Query, Request
from fastapi.responses import FileResponse, Response
from fastapi.exceptions import HTTPException
from Scripts import utils
from Scripts.utils import Color, strip_image_metadata
from Scripts.ServerData import ServerData, resolve_library_path

@utils.fastAPI.get("/api/v1/get-img/download")
@utils.limiter.limit("1200/minute")
async def download_raw_img(
    request: Request,
    f: str = Query(..., title="The location of the file you want"),
    ):
    """Returns a raw image"""

    img_path = resolve_library_path(f)

    # Exists
    if not img_path.is_file():
        raise HTTPException(status_code=404, detail="Image could not be found")
    
    # Check if its a supported image
    if not img_path.suffix.replace(".", "") in utils.supported_download_image_extensions:
        raise HTTPException(status_code=400, detail="Must be a supported image type")

    media_type, _ = mimetypes.guess_type(img_path)

    return Response(
        content=strip_image_metadata(img_path),
        media_type=media_type
    )


@utils.fastAPI.get("/api/v1/get-img/convert")
@utils.limiter.limit("60/minute")
async def convert_img(
    request: Request,
    f: str = Query(..., title="The location of the file you want"),
    t: str = Query("webp", title="The file type of response (default webp)")
):
    """Converts a raw image to a new type"""

    img_path = resolve_library_path(f)

    # Exists
    if not img_path.is_file():
        raise HTTPException(status_code=404, detail="Image does not exist")
    
    # Check if its a supported image
    if not img_path.suffix.replace(".", "") in utils.supported_resize_image_extensions:
        raise HTTPException(status_code=400, detail="Must be a supported image type")

    # Check if the new image type is supported
    if not t in utils.supported_resize_image_extensions:
        raise HTTPException(status_code=400, detail="Must be a supported image type")

    #? Pillow doesn't support jpg
    if t == "jpg":
        t = "jpeg"

    # if it's already the same type
    if img_path.suffix.replace(".", "") == t:
        return Response(
            content=strip_image_metadata(img_path),
            media_type=f"image/{t}",
        )

    # Open image
    with Image.open(img_path) as image:
        output = io.BytesIO()

        # Jpg doesn't support rgba
        if t in ("jpg", "jpeg") and image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        image.save(output, format=t)

        output.seek(0)
        return Response(
            content=output.getvalue(),
            media_type=f"image/{t}",
        )


@utils.fastAPI.get("/api/v1/get-img/resize")
@utils.limiter.limit("60/minute")
async def resize_img(
    request: Request,
    f: str = Query(..., title="The location of the file you want"),
    w: int | None = Query(None, ge=1),
    h: int | None = Query(None, ge=1),
    t: str = Query("webp", title="The file type of response (default webp)"),
    ):
    """Resize and download an image"""

    img_path = resolve_library_path(f)

    # Exists
    if not img_path.is_file():
        raise HTTPException(status_code=404, detail="Image does not exist")
    
    # Check if its a supported image
    if not img_path.suffix.replace(".", "") in utils.supported_resize_image_extensions:
        raise HTTPException(status_code=400, detail="Must be a supported image type")

    # Must specify width or height
    if not w and not h:
        raise HTTPException(status_code=400, detail="Must specify width, height, or both")

    # Check if the new image type is supported
    if not t in utils.supported_resize_image_extensions:
        if t != "keep":
            raise HTTPException(status_code=400, detail="Must be a supported image type")

    # Keep the original image type
    og_img_type = img_path.suffix.replace(".", "")
    if t == "keep":
        t = og_img_type

    #? Pillow doesn't support "jpg"
    if t == "jpg":
        t = "jpeg"

    # Limit the maximum width and height to prevent resource exhaustion
    if w and w > 10000:
        raise HTTPException(status_code=400, detail="Width too large")
    if h and h > 10000:
        raise HTTPException(status_code=400, detail="Height too large")

    cache_path = (
        ServerData.get_cache_path()
        / img_path.parent.relative_to(ServerData.get_library_path())
        / f"{img_path.stem}_{w or 'auto'}x{h or 'auto'}.{t}"
    )

    # Make the parent directory if it doesn't exist
    cache_path.parent.mkdir(parents=True, exist_ok=True)

    # Return cached image if it already exists
    if cache_path.is_file():
        print("Found cached image")

        return FileResponse(
            cache_path,
            media_type=f"image/{t}",
        )

    # Open the image for resizing
    with Image.open(img_path) as image:
        og_w, og_h = image.size

        #? Use requested size, otherwise use original size (to allow for sizes that aren't specified)
        max_w = w or og_w
        max_h = h or og_h

        # Calculate which axis got scaled down the most
        #? 1.0 prevents upscaling 
        scale = min(
            max_w / og_w,
            max_h / og_h,
            1.0,
        )

        # Return original image if it is upscaling
        if scale == 1.0:

            # Convert the image to the new type
            if t != og_img_type:
                output = io.BytesIO()

                # Jpg doesn't support rgba
                if t in ("jpg", "jpeg") and image.mode not in ("RGB", "L"):
                    image = image.convert("RGB")

                image.save(output, format=t)

                output.seek(0)
                return Response(
                    content=output.getvalue(),
                    media_type=f"image/{t}",
                )

            # Return oriiginal image
            else:
                return Response(
                    strip_image_metadata(img_path),
                    media_type=f"image/{og_img_type}",
                )

        # Scale down both axis by that amount, maintains aspect ratio
        new_width = round(og_w * scale)
        new_height = round(og_h * scale)

        # Update the cache path
        cache_path = (
            ServerData.get_cache_path()
            / img_path.parent.relative_to(ServerData.get_library_path())
            / f"{img_path.stem}_{new_width if w else 'auto'}x{new_height if h else 'auto'}.{t}"
        )

        # Resize the image
        resized_img = image.resize((new_width, new_height), Image.Resampling.NEAREST)

        # Save the resized image to cache
        resized_img.save(cache_path, format=t)
    return FileResponse(cache_path, media_type=f"image/{t}")