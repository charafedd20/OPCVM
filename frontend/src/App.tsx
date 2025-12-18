import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Optimize from './pages/Optimize'
import './App.css'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/optimize" element={<Optimize />} />
      </Routes>
    </Router>
  )
}

export default App

