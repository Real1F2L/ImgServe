import { Route, Routes } from 'react-router-dom'

// Layout
import Layout from './Components/Layout.jsx'

// Pages
import Home from './pages/Home/Home.jsx'
// import Error_404 from './pages/errors/404.jsx'
import InspectImg from './pages/Inspect/inspect-img.jsx';
import Error_404 from './pages/errors/404.jsx';

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} />

        <Route path="/inspect/*" element={<InspectImg />} />

        <Route path="*" element={<Error_404 />} />
      </Routes>
    </Layout>
  )
}