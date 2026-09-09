import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import "./FileExplorer.css"


export default function FileExplorer() {
  const [files, setFiles] = useState([])
  const [dirs, setDirs] = useState([])
  const [currentDir, setCurrentDir] = useState("")
  const navigate = useNavigate();

  // Search folder when dir changes
  useEffect(() => {
    fetch(`http://127.0.0.1:8080/api/v1/folder-search?f=${currentDir}`, {
      method: "GET"
    })
    .then(res => res.json())
    .then((data) => {
      setFiles(data.files)
      setDirs(data.dirs)
    });
  }, [currentDir]);

  return (
    <section id='FileExplorer'>
      <h1>File Explorer</h1>
      <p>Explore files inside your ImgServe Library</p>

      <h1 className='clickable' id='currentDir'
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
        /{currentDir}
      </h1>
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
          {
            dirs.map((dir, i) => {
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
          {
            files.map((file, i) => {
              const is_image = file.is_image ? 'True' : 'False'
              return (
                <tr key={i} className={`File clickable ${is_image ? 'Image' : ''}`}
                  tabIndex={0}
                  onClick={() => {
                    navigate(`/inspect/${currentDir}/${file.name}.${file.extension}`);
                  }}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      navigate(`/inspect/${currentDir}/${file.name}.${file.extension}`);
                    }
                  }}
                >
                  <td></td>
                  <td>{file.name}</td>
                  <td>{file.extension}</td>
                  <td className={is_image}></td>
                  <td className={file.is_resizable_image ? 'True' : 'False'}></td>
                  <td className={file.is_video ? 'True' : 'False'}></td>
                  <td>{getCleanTimeString(file.last_modified)}</td>
                  <td>{formatFileSize(file.size_bytes)}</td>
                  <td className='copy clickable' title='Copy to Clipboard'></td>
                  <td className='download clickable' title='Download File'></td>
                </tr>
              )
            })
          }

          {
            files.length === 0 && dirs.length === 0 &&
              <tr>
                <td colSpan={10}>This folder is empty.</td>
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