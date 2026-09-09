import { useNavigate } from 'react-router-dom'
import { useParams } from 'react-router-dom'
import { useEffect, useRef, useState } from 'react';

import "./index.css"

import FileExplorer from '../../Components/FileExplorer/FileExplorer';

export default function InspectImg() {
    const navigate = useNavigate();
    const { "*": filePath} = useParams();

    const [imgJSON, setImgJSON] = useState(null);

    // Width and height vars
    const [ogImg, setOgImg] = useState(null);
    const [ImgURL, setImgURL] = useState(null);
    const [width, setWidth] = useState(null);
    const [height, setHeight] = useState(null);

    // Canvas vars
    const maxCanvasSize = 1024;

    // Request img data from the backend
    useEffect(() => {
        if (!filePath) {
            return;
        }  

        // Fetch image data
        fetch("http://127.0.0.1:8080/api/v1/file-search?f=" + filePath, {
            method: "GET"
        })
        .then(res => {
            // Redirect to 404 page if the image doesn't exist
            if ([400, 404].includes(res.status)) {
                navigate("/404");
                return null;
            }

            return res;
        })
        .then(res => res.json())
        .then(body => {
            setImgJSON(body);
            setWidth(body.width);
            setHeight(body.height);

            // Load a original image blob if this is a resizable image
            //? This is used to resize the image locally and avoid resize request spam
            if (body.is_resizable_image) {
                loadImage();
            }

            // Change the image url to a regular download (for non-resizeable images)
            else {
                setImgURL(`http://127.0.0.1:8080/api/v1/get-img/download?f=${filePath}`);
            }
        });

        const loadImage = async () => {
            // Fetch the image
            const res = await fetch(`http://127.0.0.1:8080/api/v1/get-img/download?f=${filePath}`);

            // Blob the image
            const blob = await res.blob();

            setOgImg(blob);
        }
    }, [filePath]);

    // Store the old dimentions of the image
    const previousDimentions = useRef({
        width: null,
        height: null
    })

    // Og image aspect ratio
    const aspectRatio = imgJSON ? imgJSON.width / imgJSON.height : null;

    // Resize the image locally when the width or height changes
    useEffect(() => {
        if (!ogImg || !width || !height) {
            return;
        }

        // Variables for width and height after aspect ratio changes
        let newWidth = width;
        let newHeight = height;

        // Define max sizes
        const maxWidth = imgJSON?.width ?? Infinity;
        const maxHeight = imgJSON?.height ?? Infinity;

        // Determine which dimension changed
        const previous = previousDimentions.current;
        const widthChanged = previous.width !== width;
        const heightChanged = previous.height !== height;

        // If this is the first render
        if (previous.width === null || previous.height === null) {

            // Load previous dimentions
            previousDimentions.current = {
                width,
                height
            };
        }

        // If the width changed, change the height to match the aspect ratio
        if (widthChanged && !heightChanged) {
            // Prevent going over original size
            newWidth = Math.min(width, maxWidth);

            newHeight = Math.round(newWidth / aspectRatio);
            setHeight(newHeight);
            setWidth(newWidth);
        }
        // If the height changed, change the width to match the aspect ratio
        else if (heightChanged && !widthChanged) {
            // Prevent going over original size
            newHeight = Math.min(height, maxHeight);

            newWidth = Math.round(newHeight * aspectRatio);
            setWidth(newWidth);
            setHeight(newHeight);
        }

        // Load new dimentions
        previousDimentions.current = {
            width: newWidth,
            height: newHeight
        };

        // A function to resize the img and store it as a blob
        const resizeImage = async () => {
            // Turn the original image into a bitmap
            const bitmap = await createImageBitmap(ogImg);

            // Create a new canvas
            const canvas = document.createElement("canvas");
            canvas.width = newWidth;
            canvas.height = newHeight;
            
            const ctx = canvas.getContext("2d");

            // Draw the og image onto the canvas
            ctx.drawImage(bitmap, 0, 0, newWidth, newHeight);

            // Turn the canvas into a blob
            canvas.toBlob((blob) => {
                if (!blob) return;

                const url = URL.createObjectURL(blob);

                // Save the resized image url to be used
                setImgURL(url);
            }, ogImg.type);

            bitmap.close();
        }

        if (imgJSON.is_resizable_image) {
            resizeImage();
        }
    }, [ogImg, width, height]);
    

    return (
        <>
            <section id='hero'>
                <div className='ImgContainer'>
                    <div className='ImgEditor'>
                        <img alt={imgJSON?.name} title={imgJSON?.name} src={ImgURL} loading='lazy'></img>
                    </div>

                    <div className='ImgOptions'>
                        <div className='FormatOption'>
                            <h2>Image Format</h2>
                            <select>
                                <option value="webp">WEBP</option>
                                <option value="png">PNG</option>
                                <option value="jpeg">JPEG</option>
                            </select>
                        </div>

                        <div className='SizeOption'>
                            <h2>Image Size</h2>

                            <div>
                                <div className='SizeNumContainer'>
                                    <label>Width</label>
                                    <input type='number' step="1" min="1" value={width ?? "400"} onChange={(e) => setWidth(e.target.value)}></input>
                                </div>
                                <p className='x'>x</p>
                                <div className='SizeNumContainer'>
                                    <label>Height</label>
                                    <input type='number' step="1" min="1" value={height ?? "400"} onChange={(e) => setHeight(e.target.value)}></input>
                                </div>
                            </div>

                            <button
                                onClick={() => {
                                    setWidth(imgJSON?.width);
                                    setHeight(imgJSON?.height);
                                }}
                            >Native Size</button>
                        </div>

                        <div className='ImgActions'>
                            <button>Copy</button>
                            <button>Download</button>
                        </div>
                    </div>
                </div>

                <div>

                </div>
            </section>

            <FileExplorer />
        </>
    )
}