import { Link } from 'react-router-dom'

function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-500 to-primary-700 flex items-center justify-center">
      <div className="text-center text-white">
        <h1 className="text-5xl font-bold mb-4">Portfolio Optimizer Pro</h1>
        <p className="text-xl mb-8">Advanced Portfolio Optimization with Risk Constraints</p>
        <Link
          to="/optimize"
          className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100 transition"
        >
          Start Optimizing
        </Link>
      </div>
    </div>
  )
}

export default Home

