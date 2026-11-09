import { Route, Routes, useLocation, matchPath } from 'react-router-dom'
import { useEffect } from 'react';

// Layout
import Layout from './Components/Layout.jsx'

// Pages
import Home from './pages/Home/Home.jsx'
import InspectImg from './pages/Inspect/inspect-img.jsx';
import Error_404 from './pages/errors/404.jsx';

const titles = [
  { path: "/", title: "ImgServe" },
  { path: "/inspect/:path", title: "ImgServe | Inspect Image" },
];

export default function App() {

  const location = useLocation();

  useEffect(() => {
    const match = titles.find(({ path }) =>
      matchPath({ path, end: true }, location.pathname)
    );

    document.title = match?.title ?? "ImgServe | Untitled Page";
  }, [location.pathname]);

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