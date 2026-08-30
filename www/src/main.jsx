import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

import App from './App.jsx'

import './sitewide.js'
import './sitewide.css'

createRoot(document.querySelector('body')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
