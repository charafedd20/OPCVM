import { useState, useEffect } from 'react'
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import axios from 'axios'

const API_BASE = 'http://localhost:8000/api/v1'

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe']

function Analytics() {
  const [stocksSummary, setStocksSummary] = useState<any>(null)
  const [stockStats, setStockStats] = useState<any>(null)
  const [chartData, setChartData] = useState<any[]>([])
  const [opcvmSummary, setOpcvmSummary] = useState<any>(null)
  const [marketOverview, setMarketOverview] = useState<any>(null)
  const [selectedSymbol, setSelectedSymbol] = useState('ATW')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAllData()
  }, [])

  useEffect(() => {
    if (selectedSymbol) {
      fetchStockData(selectedSymbol)
    }
  }, [selectedSymbol])

  const fetchAllData = async () => {
    try {
      setLoading(true)
      const [stocks, opcvm, market] = await Promise.all([
        axios.get(`${API_BASE}/analytics/stocks/summary`),
        axios.get(`${API_BASE}/analytics/opcvm/summary`),
        axios.get(`${API_BASE}/analytics/market/overview`)
      ])
      
      setStocksSummary(stocks.data)
      setOpcvmSummary(opcvm.data)
      setMarketOverview(market.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchStockData = async (symbol: string) => {
    try {
      const [stats, chart] = await Promise.all([
        axios.get(`${API_BASE}/analytics/stocks/${symbol}/statistics?days=30`),
        axios.get(`${API_BASE}/analytics/stocks/${symbol}/chart-data?chart_type=line&days=30`)
      ])
      
      setStockStats(stats.data)
      setChartData(chart.data.data.map((d: any) => ({
        date: new Date(d.date).toLocaleDateString(),
        price: d.price,
        volume: d.volume
      })))
    } catch (error) {
      console.error('Error fetching stock data:', error)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Chargement des données...</p>
        </div>
      </div>
    )
  }

  const sectorData = stocksSummary?.sectors ? Object.entries(stocksSummary.sectors).map(([name, value]) => ({
    name,
    value
  })) : []

  const opcvmPerformanceData = opcvmSummary?.best_performers_1y?.map((opcvm: any) => ({
    name: opcvm.name.substring(0, 15),
    performance: opcvm.performance
  })) || []

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 text-gray-800">📊 Analytics & Visualisations</h1>

        {/* Market Overview */}
        {marketOverview && (
          <div className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-2xl font-bold mb-4">Vue d'ensemble du marché</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded">
                <p className="text-sm text-gray-600">Actions listées</p>
                <p className="text-2xl font-bold text-blue-600">{marketOverview.market_statistics.total_listed_stocks}</p>
              </div>
              <div className="bg-green-50 p-4 rounded">
                <p className="text-sm text-gray-600">Couverture données</p>
                <p className="text-2xl font-bold text-green-600">{marketOverview.market_statistics.coverage_percentage.toFixed(1)}%</p>
              </div>
              <div className="bg-purple-50 p-4 rounded">
                <p className="text-sm text-gray-600">Volume 30 jours</p>
                <p className="text-2xl font-bold text-purple-600">
                  {(marketOverview.trading_activity.last_30_days_volume / 1_000_000).toFixed(1)}M
                </p>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Sector Distribution */}
          {sectorData.length > 0 && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold mb-4">Répartition par secteur</h2>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={sectorData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {sectorData.map((entry: any, index: number) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Market Cap Statistics */}
          {stocksSummary?.market_cap_statistics && (
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-bold mb-4">Capitalisation boursière</h2>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-600">Moyenne:</span>
                  <span className="font-bold">{(stocksSummary.market_cap_statistics.mean / 1_000_000_000).toFixed(2)}B MAD</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Médiane:</span>
                  <span className="font-bold">{(stocksSummary.market_cap_statistics.median / 1_000_000_000).toFixed(2)}B MAD</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Min:</span>
                  <span className="font-bold">{(stocksSummary.market_cap_statistics.min / 1_000_000_000).toFixed(2)}B MAD</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Max:</span>
                  <span className="font-bold">{(stocksSummary.market_cap_statistics.max / 1_000_000_000).toFixed(2)}B MAD</span>
                </div>
                <div className="flex justify-between border-t pt-2">
                  <span className="text-gray-600">Total:</span>
                  <span className="font-bold text-primary-600">{(stocksSummary.market_cap_statistics.sum / 1_000_000_000).toFixed(2)}B MAD</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Stock Analysis */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4">Analyse d'action</h2>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Sélectionner une action:
            </label>
            <select
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
              className="border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              {stocksSummary?.most_traded_stocks?.map((stock: any) => (
                <option key={stock.symbol} value={stock.symbol}>
                  {stock.symbol}
                </option>
              ))}
            </select>
          </div>

          {chartData.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold mb-2">Évolution du prix - {selectedSymbol}</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="price" stroke="#667eea" strokeWidth={2} name="Prix (MAD)" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {stockStats && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-blue-50 p-4 rounded">
                <p className="text-sm text-gray-600">Rendement total (30j)</p>
                <p className={`text-2xl font-bold ${stockStats.price_trend.change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {stockStats.price_trend.change_percent.toFixed(2)}%
                </p>
              </div>
              <div className="bg-green-50 p-4 rounded">
                <p className="text-sm text-gray-600">Volatilité annualisée</p>
                <p className="text-2xl font-bold text-green-600">
                  {stockStats.returns_statistics.volatility_annualized.toFixed(2)}%
                </p>
              </div>
              <div className="bg-purple-50 p-4 rounded">
                <p className="text-sm text-gray-600">Sharpe Ratio</p>
                <p className="text-2xl font-bold text-purple-600">
                  {stockStats.returns_statistics.sharpe_ratio.toFixed(2)}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* OPCVM Performance */}
        {opcvmPerformanceData.length > 0 && (
          <div className="bg-white rounded-lg shadow-md p-6">
            <h2 className="text-2xl font-bold mb-4">Performance OPCVM (1 an)</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={opcvmPerformanceData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="performance" fill="#667eea" name="Performance (%)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </div>
  )
}

export default Analytics

