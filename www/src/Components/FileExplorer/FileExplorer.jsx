import "./FileExplorer.css"

export default function FileExplorer() {
  return (
    <>
      <h1>File Explorer</h1>
      <p>Explore files inside your ImgServe Library</p>

      <table id="ExplorerTable">
        <thead>
          <tr>
            <th>Type</th>
            <th>Name</th>
            <th>Extension</th>
            <th>Resizable</th>

            <th></th>
            <th></th>
          </tr>
        </thead>

        <tbody>
          <tr>
            <td>File</td>
            <td>Example Name</td>
            <td>jpg</td>
            <td>True</td>
            <td><button>Modify</button></td>
            <td><button>Download</button></td>
          </tr>
        </tbody>
      </table>
    </>
  )
}