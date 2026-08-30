import { useState } from 'react'

import './index.css'

import FileExplorer from '../../Components/FileExplorer/FileExplorer.jsx'

function Home() {
  const [count, setCount] = useState(0)

  return (
    <>
      <section id='hero'>
        <div className='horFlex'>
          <img className='heroIcon' src="http://127.0.0.1:8080/api/v1/get-img/download?f=ImgServe-NoSteam.svg" alt="ImgServe Logo"></img>
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

      <section id='FileExplorer'>
        <FileExplorer />
      </section>
    </>
  )
}

export default Home
