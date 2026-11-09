import "./Footer.css"

export default function Footer() {
    return (
        <footer id="gegeha-footer">
            <div className="CC-Container">
                <p id="cc">Powered by <a href="https://www.gegeha.com/" title="Gegeha's Website" target="_blank">Gegeha <img className="emoji" src="/api/v1/get-img/download?f=ImgServe%20Web%20UI/Gegeha.svg" alt="Gegeha Logo" loading="lazy"></img></a></p>
            </div>

            <div className="FooterIContainer">
                <p>Copyright © 2024-{new Date().getFullYear()} Gegeha. All Rights Reserved.</p>

                <div>
                    <div className="footer-sec">
                        <h1>ImgServe</h1>
                        <ul>
                            <li><a href="https://www.gegeha.com/imgserve" title="Gegeha's ImgServe Info Page" target="_blank">Development Page</a></li>
                            <li><a href="/docs" title="ImgServe Documentation">Documentation and API usage</a></li>
                            <li><a href="https://github.com/Real1F2L/ImgServe" title="ImgServe's Github Repository" target="_blank">Github Repository</a></li>
                        </ul>
                    </div>
                    <div className="footer-sec">
                        <h1>Designed by Gegeha</h1>
                        <ul>
                            <li><a href="https://dev.gegeha.com/portfolio/" title="ImgServe Documentation">Owner and Developer<br></br>Aden Cabreja</a></li>
                            <li><a href="https://www.gegeha.com/about-us" title="Gegeha's ImgServe Info Page" target="_blank">Our mission</a></li>
                        </ul>
                    </div>
                    <div className="footer-sec">
                        <h1>Support</h1>
                        <ul>
                            <li><a href="mailto:business@gegeha.com" title="Gegeha Business Email">Email</a></li>
                            <li><a href="https://discord.com/invite/RHt7wvmfEp" title="Gegeha Discord Server" target="_blank">Discord Server</a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </footer>
    )
}