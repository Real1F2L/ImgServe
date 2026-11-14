import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import "./FileExplorer.css"


export default function FileExplorer() {
  const [files, setFiles] = useState([]);
  const [dirs, setDirs] = useState([]);
  const [loading, setloading] = useState(true);
  const [copiedFilePath, setCopiedFilePath] = useState(null);
  const copyPopupTimeout = useRef(null);
  const navigate = useNavigate();

  useEffect(() => () => window.clearTimeout(copyPopupTimeout.current), []);
  
  // Grab current dir from url
  const windowdir = decodeURI(window.location.pathname).split("/").splice(1);
  windowdir.pop(); //? Get dir not file

  // Remove items from the start
  if (["inspect"].includes(windowdir[0])) {
    windowdir.shift();
  }

  // Set current dir
  const [currentDir, setCurrentDir] = useState(windowdir.join("/"));

  // Search folder when dir changes
  useEffect(() => {
    setloading(true);

    fetch(`/api/v1/folder-search?f=${currentDir}`, {
      method: "GET"
    })
      .then(res => res.json())
      .then((data) => {
        setFiles(data.files)
        setDirs(data.dirs)
      })
      .catch(err => {
        setloading(true);
        console.log(err);
      })
      .finally(() => {
        setloading(false);
      })
  }, [currentDir]);

  return (
    <section id='FileExplorer'>
      <h1>File Explorer</h1>
      <p>Explore files inside your ImgServe Library</p>

      <div className='DirContainer clickable'
        tabIndex={0}
        onClick={() => {
          if (currentDir !== "") {
            setCurrentDir(currentDir.split("/").slice(0, -1).join("/"))
          }
        }
        }
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            if (currentDir !== "") {
              setCurrentDir(currentDir.split("/").slice(0, -1).join("/"))
            }
          }
        }}
      >
        <img className='back' alt='Back' loading='lazy' src="/api/v1/get-img/download?f=ImgServe%20Web%20UI/Back.svg"></img>
        <h1 id='currentDir'>/{currentDir}</h1>
      </div>

      <table id="ExplorerTable">
        <thead>
          <tr>
            <th>Type</th>
            <th>Name</th>
            <th>Extension</th>
            <th>Is Image</th>
            <th>Resizable</th>
            <th>Is Video</th>
            <th>Last Modified</th>
            <th>Size</th>

            <th></th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          {dirs.map((dir, i) => {
            return (
              <tr key={i} className='Folder clickable'
                tabIndex={0}
                onClick={() => {
                  if (currentDir === "") {
                    setCurrentDir(dir.name)
                    return
                  }
                  setCurrentDir(currentDir + "/" + dir.name)
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    if (currentDir === "") {
                      setCurrentDir(dir.name)
                      return
                    }
                    setCurrentDir(currentDir + "/" + dir.name)
                  }
                }}
              >
                <td></td>
                <td>{dir.name}</td>
                <td className='Empty'></td>
                <td className='Empty'></td>
                <td className='Empty'></td>
                <td className='Empty'></td>
                <td className='Empty'></td>
                <td>{dir.items_inside} Items</td>
                <td className='Empty'></td>
                <td className='Empty'></td>
              </tr>
            )
          })
          }


          {files.map((file, i) => {
            const is_image = Boolean(file.is_image);
            const fileName = file.extension ? `${file.name}.${file.extension}` : file.name;
            const filePath = [currentDir, fileName].filter(Boolean).join("/");
            const downloadEndpoint = is_image ? "/api/v1/get-img/download" : "/api/v1/file-download";
            const downloadUrl = `${downloadEndpoint}?${new URLSearchParams({ f: filePath })}`;
            return (
              <tr key={i} className={`${file.is_image ? 'Image clickable' : 'File'}`}
                tabIndex={0}
                onClick={() => {
                  if (file.is_image) {
                    navigate(`/inspect/${filePath}`);
                  }
                }}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    if (file.is_image) {
                      navigate(`/inspect/${filePath}`);
                    }
                  }
                }}
              >
                <td></td>
                <td>{file.name}</td>
                <td>{file.extension}</td>
                <td className={file.is_image ? 'True' : 'False'}></td>
                <td className={file.is_resizable_image ? 'True' : 'False'}></td>
                <td className={file.is_video ? 'True' : 'False'}></td>
                <td>{getCleanTimeString(file.last_modified)}</td>
                <td>{formatFileSize(file.size_bytes)}</td>
                <td className='copy-cell'>
                  <button
                    className='file-action copy'
                    type='button'
                    title='Copy download link'
                    aria-label={`Copy download link for ${fileName}`}
                    onKeyDown={(e) => e.stopPropagation()}
                    onClick={async (e) => {
                      e.stopPropagation();
                      try {
                        await navigator.clipboard.writeText(new URL(downloadUrl, window.location.origin).href);
                        setCopiedFilePath(filePath);
                        window.clearTimeout(copyPopupTimeout.current);
                        copyPopupTimeout.current = window.setTimeout(() => setCopiedFilePath(null), 1200);
                      } catch (error) {
                        console.error("Could not copy the download link:", error);
                      }
                    }}
                  />
                  {copiedFilePath === filePath && <span className='copy-popup' role='status'>Copied!</span>}
                </td>
                <td>
                  <a
                    className='file-action download'
                    href={downloadUrl}
                    download={fileName}
                    title='Download File'
                    aria-label={`Download ${fileName}`}
                    onKeyDown={(e) => e.stopPropagation()}
                    onClick={(e) => e.stopPropagation()}
                  />
                </td>
              </tr>
            )
          })
          }

          {
            files.length == 0 && dirs.length == 0 &&
            <tr>
              <td colSpan={10} className='emptymsg'>This directory is empty.</td>
            </tr>
          }
        </tbody>
      </table>
    </section>
  )
}

function getCleanTimeString(time) {
  return new Intl.DateTimeFormat('en-US', {
    month: "short",
    day: "numeric",
    year: "numeric",

    hour: "numeric",
    minute: "numeric",
  }).format(new Date(time * 1000))
}

/**
 * Takes in a size in bytes and returns a human readable string
 * @param {number} size
 * @returns {string}
 */
function formatFileSize(size) {
  if (size < 1024) {
    return size + " Bytes"
  } else if (size < 1024 ** 2) {
    return Math.round(size / 1024) + " KiB"
  } else if (size < 1024 ** 3) {
    return Math.round(size / 1024 ** 2) + " MiB"
  } else {
    return Math.round(size / 1024 ** 3) + " GiB"
  }
}