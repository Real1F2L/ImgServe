import { useState, useEffect } from 'react'
import "./FileExplorer.css"

export default function FileExplorer() {
  const [files, setFiles] = useState([])
  const [dirs, setDirs] = useState([])
  const [currentDir, setCurrentDir] = useState("")

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
  }, [currentDir])

  return (
    <>
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
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td></td>
                  <td>{dir.items_inside} Items</td>
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
                  // onClick={() => {
                  //   setCurrentDir(file.name)
                  // }}
                  // onKeyDown={(e) => {
                  //   if (e.key === "Enter") {
                  //     setCurrentDir(file.name)
                  //   }
                  // }}
                >
                  <td></td>
                  <td>{file.name}</td>
                  <td>{file.extension}</td>
                  <td className={is_image}></td>
                  <td className={file.is_resizable_image ? 'True' : 'False'}></td>
                  <td className={file.is_video ? 'True' : 'False'}></td>
                  <td>{new Date(file.last_modified).toLocaleString()}</td>
                  <td>{Math.floor(file.size_bytes / 1024)} <abbr title="Kibibyte">KiB</abbr></td>
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
    </>
  )
}