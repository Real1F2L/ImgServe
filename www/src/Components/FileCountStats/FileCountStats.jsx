import './FileCountStats.css'

import { useState, useEffect } from 'react'

export default function FileCountStats() {
    const [files, setFiles] = useState([]);
    const [images, setImages] = useState([]);
    const [svgs, setSvgs] = useState([]);
    const [dirs, setDirs] = useState([]);

    useEffect(() => {
        // Grab file counts from the backend
        fetch(`/api/v1/data/library-file-counts`, {
            method: "GET"
        })
        .then(res => res.json())
        .then((data) => {
            // Create a loop that increases the count of each file type until it reaches the correct value, for a smooth animation effect
            const filesCount = data.stats.files;
            const imagesCount = data.stats.images;
            const svgsCount = data.stats.svgs;
            const dirsCount = data.stats.dirs;

            function animateCount(setter, targetCount) {
                let currentCount = 0;

                const interval = setInterval(() => {
                    currentCount++;
                    setter(currentCount);

                    // Stop looping when the target is reached
                    if (currentCount >= targetCount) {
                        clearInterval(interval);
                    }

                }, 70 /* How quickly to increase */ );
            }

            animateCount(setFiles, filesCount);
            animateCount(setImages, imagesCount);
            animateCount(setSvgs, svgsCount);
            // animateCount(setDirs, dirsCount);
        })
    }, []);

    return (
        <section className="FileCountStats">
            <div className="Stat-Circle Files-stat">
                <h2>{files} File{files === 1 ? "" : "s"}</h2>
                <p>In Library</p>
            </div>
            <div className="Stat-Circle Images-stat">
                <h2>{images} Image{images === 1 ? "" : "s"}</h2>
                <p>In Library</p>
            </div>
            <div className="Stat-Circle SVG-stat">
                <h2>{svgs} SVG{svgs === 1 ? "" : "s"}</h2>
                <p>In Library</p>
            </div>
            {/* <div className="Stat-Circle Dirs-stat">
                <h2>{dirs} Dirs</h2>
                <p>In Library</p>
            </div> */}
        </section>
    )
}