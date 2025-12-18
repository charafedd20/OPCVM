import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Optimize from './pages/Optimize'
import './App.css'

function App() {
  return (
    <Router>
      <nav className="bg-primary-600 text-white p-4 shadow-lg">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <Link to="/" className="text-xl font-bold">Portfolio Optimizer Pro</Link>
          <div className="space-x-4">
            <Link to="/" className="hover:text-primary-200">Accueil</Link>
            <Link to="/optimize" className="hover:text-primary-200">Optimiser</Link>
          </div>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/optimize" element={<Optimize />} />
      </Routes>
    </Router>
  )
}

export default App

