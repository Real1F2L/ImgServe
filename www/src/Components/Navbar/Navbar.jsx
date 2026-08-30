import "./Navbar.css"
import { toggleTheme, isDarkTheme } from "../../sitewide.js"

export default function Navbar() {
    return (
        <nav>
            <div id="navTop">
                <div className="navLeft">
                    <a id="Home" href="/" title="ImgServe Home">
                        <img src="http://127.0.0.1:8080/api/v1/get-img/download?f=ImgServe%20Web%20UI/ImgServe-NoSteam.svg" alt="ImgServe Logo"></img>
                        <h1>ImgServe</h1>
                    </a>
                </div>
                <div className="navRight">
                    <a className={`ThemeToggleContainer ${isDarkTheme() ? "dark" : ""}`}
                        title="Toggle between light and dark mode"
                        onClick={() => {
                            toggleTheme();
                        }}    
                    >
                        <div>
                            <div className="ThemeSide"></div>
                            <div className="ThemeSide"></div>
                        </div>
                    </a>
                </div>
            </div>

            <div id="navBottom"></div>
        </nav>
    )
}