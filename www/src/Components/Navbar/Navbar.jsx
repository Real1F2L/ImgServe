import "./Navbar.css"

export default function Navbar() {
    return (
        <nav>
            <div id="navTop">
                <div className="navLeft">
                    <a id="Home">
                        <img src="http://127.0.0.1:8080/api/v1/get-img/download?f=ImgServe-NoSteam.svg" alt="ImgServe Logo"></img>
                        <h1>ImgServe</h1>
                    </a>
                </div>
                <div className="navRight">

                </div>
            </div>

            <div id="navBottom"></div>
        </nav>
    )
}