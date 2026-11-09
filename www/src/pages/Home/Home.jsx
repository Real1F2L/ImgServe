import './index.css'

import FileExplorer from '../../Components/FileExplorer/FileExplorer.jsx'
import FileCountStats from '../../Components/FileCountStats/FileCountStats.jsx'

function Home() {
  return (
    <>
      <section id='hero'>
        <div className='horFlex'>
          <img className='heroIcon' src="/api/v1/get-img/download?f=ImgServe%20Web%20UI/ImgServe.svg" alt="ImgServe Logo"></img>
          <h1>ImgServe</h1>
        </div>
        <h2>
          Get Images 
          <span id='HeroHeader'>
            <span>Your Way.</span>
            <span>The Best Way.</span>
            <span>The Fastest Way.</span>
            <span>Any Way.</span>
            <span>Your Way.</span>
          </span>
        </h2>
      </section>

      <FileCountStats />

      <FileExplorer />
    </>
  )
}

export default Home
