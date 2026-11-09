import Footer from "./Footer/Footer.jsx"
import Navbar from "./Navbar/Navbar.jsx"

export default function Layout({ children}) {
  return (
    <>
      <Navbar />

      <main>
        {children}

        <Footer />
      </main>
    </>
    )
}