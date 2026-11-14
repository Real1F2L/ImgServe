import { useNavigate } from 'react-router-dom'
import { useParams } from 'react-router-dom'
import { useEffect, useRef, useState } from 'react';

import { Ring2 } from 'ldrs/react'
import 'ldrs/react/Ring2.css'

import "./inspect-img.css"

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
    const [downloadFormat, setDownloadFormat] = useState("webp");
    const [showCopyPopup, setShowCopyPopup] = useState(false);
    const copyPopupTimeout = useRef(null);

    // Loading
    const [loading, setLoading] = useState(true);

    // Canvas vars
    const maxCanvasSize = 1024;

    // Request img data from the backend
    useEffect(() => {
        if (!filePath) {
            return;
        }

        // If new filepath is the same as the old filepath, skip
        if (imgJSON?.path === filePath) {
            return;
        }

        // Unload image url from ImgEditor and show loading icon
        setImgURL(null);
        setOgImg(null);
        setLoading(true);

        // Fetch image data
        fetch("/api/v1/file-search?f=" + filePath, {
            method: "GET"
        })
        .then(res => {
            // Redirect to 404 page if the image doesn't exist
            if (!res.ok || [400, 404].includes(res.status)) {
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
            setDownloadFormat(body.is_resizable_image ? "webp" : "original");

            // Load a original image blob if this is a resizable image
            //? This is used to resize the image locally and avoid resize request spam
            if (body.is_resizable_image) {
                loadImage();
            }

            // Change the image url to a regular download (for non-resizeable images)
            else {
                setImgURL(`/api/v1/get-img/download?f=${filePath}`);
            }
        });

        const loadImage = async () => {
            // Fetch the image
            const res = await fetch(`/api/v1/get-img/download?f=${filePath}`);

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

    useEffect(() => () => window.clearTimeout(copyPopupTimeout.current), []);

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

        // Debounce expensive resizing to prevent spam
        const debounceResizeTimeout = setTimeout(() => {
            if (imgJSON.is_resizable_image) {
                resizeImage();
            }
        }, 300);

        return () => clearTimeout(debounceResizeTimeout);
    }, [ogImg, width, height]);

    // Copy the img url to resize the image to what its set to
    const copyImageUrl = async () => {
        try {
            const params = new URLSearchParams({ f: filePath });
            let endpoint = "/api/v1/get-img/download";

            if (imgJSON?.is_resizable_image) {
                params.set("w", String(width));
                params.set("h", String(height));
                params.set("t", downloadFormat === "original" ? "keep" : downloadFormat);
                endpoint = "/api/v1/get-img/resize";
            }

            const imageUrl = new URL(`${endpoint}?${params}`, window.location.origin).href;
            await navigator.clipboard.writeText(imageUrl);
            setShowCopyPopup(true);
            window.clearTimeout(copyPopupTimeout.current);
            copyPopupTimeout.current = window.setTimeout(() => setShowCopyPopup(false), 1200);
        } catch (error) {
            console.error("Could not copy image URL:", error);
        }
    };

    // Download the raw image
    const downloadImage = async () => {
        try {
            if (!imgJSON) {
                throw new Error("Image information is not available.");
            }

            const params = new URLSearchParams({ f: filePath });
            let extension = imgJSON.extension;
            let endpoint = "/api/v1/get-img/download";

            if (downloadFormat !== "original") {
                if (!imgJSON.is_resizable_image) {
                    throw new Error("This image format cannot be converted.");
                }
                params.set("w", String(width));
                params.set("h", String(height));
                params.set("t", downloadFormat);
                endpoint = "/api/v1/get-img/resize";
                extension = downloadFormat;
            }

            const response = await fetch(`${endpoint}?${params}`);
            if (!response.ok) {
                throw new Error(`Download failed with status ${response.status}.`);
            }

            const downloadUrl = URL.createObjectURL(await response.blob());
            const link = document.createElement("a");
            link.href = downloadUrl;
            link.download = `${imgJSON.name}.${extension}`;
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.setTimeout(() => URL.revokeObjectURL(downloadUrl), 1000);
        } catch (error) {
            console.error("Could not download image:", error);
        }
    };
    

    return (
        <>
            <section id='inspect-hero'>


                <div className='ImgContainer'>

                    {/* Image preview and resize controls */}
                    <div className='ImageResizeControls'>
                        <div className='ImgEditor'>
                            <div id='loadingIcon'
                            style={{display: loading ? "flex" : "none"}}
                            >
                                <p>Your Image is Loading...</p>
                                <Ring2
                                size="60"
                                stroke="7"
                                strokeLength="0.25"
                                bgOpacity="0.2"
                                speed="0.7"
                                color="var(--font-black)"
                                />
                            </div>

                            <img alt={imgJSON?.name} title={imgJSON?.name} src={ImgURL} loading='eager'

                            style={{display: loading ? "none" : "block"}}
                            onLoad={() => setLoading(false)}
                            onError={() => setLoading(false)}></img>
                        </div>

                        {imgJSON?.is_resizable_image && (
                            <>
                                <input
                                    className='ImageWidthSlider'
                                    type='range'
                                    min='1'
                                    max={imgJSON.width}
                                    step='1'
                                    value={width ?? imgJSON.width}
                                    aria-label='Image width'
                                    aria-valuetext={`${width ?? imgJSON.width} pixels`}
                                    disabled={loading}
                                    onChange={(e) => setWidth(Number(e.target.value))}
                                />
                                <input
                                    className='ImageHeightSlider'
                                    type='range'
                                    min='1'
                                    max={imgJSON.height}
                                    step='1'
                                    value={height ?? imgJSON.height}
                                    aria-label='Image height'
                                    aria-valuetext={`${height ?? imgJSON.height} pixels`}
                                    disabled={loading}
                                    onChange={(e) => setHeight(Number(e.target.value))}
                                />
                            </>
                        )}
                    </div>


                    {/* Options */}
                    <div className='ImgOptions'>
                        <div className='ImgOptions-section FormatOption'>
                            <h2>Image Format</h2>
                            <select
                                value={downloadFormat}
                                onChange={(e) => setDownloadFormat(e.target.value)}
                            >
                                {imgJSON?.is_resizable_image && (
                                    <>
                                        <option value="webp">WEBP</option>
                                        <option value="png">PNG</option>
                                        <option value="jpeg">JPEG</option>
                                        <option value="bmp">BMP</option>
                                    </>
                                )}
                                <option value="original">Original ({imgJSON?.extension?.toUpperCase()})</option>
                            </select>
                        </div>

                        <div className='ImgOptions-section SizeOption'>
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

                        <div className='ImgOptions-section ImgActions'>
                            <div className='InspectCopyControl'>
                                <button type='button' onClick={copyImageUrl} disabled={loading}>Copy</button>
                                {showCopyPopup && <span className='copy-popup' role='status'>Copied!</span>}
                            </div>
                            <button type='button' onClick={downloadImage} disabled={loading}>Download</button>
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