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
  const [selectedPeriod, setSelectedPeriod] = useState(30) // Default: 1 month
  const [loading, setLoading] = useState(true)

  const periods = [
    { label: '1 mois', days: 30 },
    { label: '3 mois', days: 90 },
    { label: '6 mois', days: 180 },
    { label: '1 an', days: 365 },
    { label: '3 ans', days: 1095 },
  ]

  useEffect(() => {
    fetchAllData()
  }, [])

  useEffect(() => {
    if (selectedSymbol) {
      fetchStockData(selectedSymbol)
    }
  }, [selectedSymbol, selectedPeriod])

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
        axios.get(`${API_BASE}/analytics/stocks/${symbol}/statistics?days=${selectedPeriod}`),
        axios.get(`${API_BASE}/analytics/stocks/${symbol}/chart-data?chart_type=line&days=${selectedPeriod}`)
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
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            {/* Stock Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sélectionner une action:
              </label>
              <select
                value={selectedSymbol}
                onChange={(e) => setSelectedSymbol(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-4 py-2 focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                {stocksSummary?.most_traded_stocks?.map((stock: any) => (
                  <option key={stock.symbol} value={stock.symbol}>
                    {stock.symbol} - {stocksSummary?.most_traded_stocks?.find((s: any) => s.symbol === stock.symbol)?.name || stock.symbol}
                  </option>
                ))}
              </select>
            </div>

            {/* Period Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Période d'analyse:
              </label>
              <div className="flex flex-wrap gap-2">
                {periods.map((period) => (
                  <button
                    key={period.days}
                    onClick={() => setSelectedPeriod(period.days)}
                    className={`px-4 py-2 rounded-md font-medium transition-all ${
                      selectedPeriod === period.days
                        ? 'bg-primary-600 text-white shadow-md'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {period.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {chartData.length > 0 && (
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <h3 className="text-lg font-semibold">
                  Évolution du prix - {selectedSymbol}
                </h3>
                <span className="text-sm text-gray-500">
                  Période: {periods.find(p => p.days === selectedPeriod)?.label} ({chartData.length} points)
                </span>
              </div>
              <ResponsiveContainer width="100%" height={400}>
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    interval="preserveStartEnd"
                  />
                  <YAxis />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.95)', border: '1px solid #ccc' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="price" 
                    stroke="#667eea" 
                    strokeWidth={2} 
                    name="Prix (MAD)"
                    dot={false}
                    activeDot={{ r: 6 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          )}

          {stockStats && (
            <div>
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-1">
                  Période analysée: {stockStats.period_days} jours ({stockStats.data_points} points de données)
                </p>
                <p className="text-xs text-gray-500">
                  {stockStats.date_range?.start && new Date(stockStats.date_range.start).toLocaleDateString()} - 
                  {stockStats.date_range?.end && new Date(stockStats.date_range.end).toLocaleDateString()}
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-blue-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Rendement total</p>
                  <p className={`text-2xl font-bold ${stockStats.price_trend.change_percent >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                    {stockStats.price_trend.change_percent.toFixed(2)}%
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {stockStats.price_trend.first_price.toFixed(2)} → {stockStats.price_trend.last_price.toFixed(2)} MAD
                  </p>
                </div>
                <div className="bg-green-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Volatilité annualisée</p>
                  <p className="text-2xl font-bold text-green-600">
                    {stockStats.returns_statistics.volatility_annualized.toFixed(2)}%
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Écart-type quotidien: {(stockStats.returns_statistics.std_daily * 100).toFixed(2)}%
                  </p>
                </div>
                <div className="bg-purple-50 p-4 rounded">
                  <p className="text-sm text-gray-600">Sharpe Ratio</p>
                  <p className="text-2xl font-bold text-purple-600">
                    {stockStats.returns_statistics.sharpe_ratio.toFixed(2)}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    Rendement moyen: {(stockStats.returns_statistics.mean_daily * 100).toFixed(3)}%/jour
                  </p>
                </div>
              </div>
              
              {/* Additional Statistics */}
              <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Prix moyen</p>
                  <p className="text-lg font-semibold">{stockStats.price_statistics.close.mean.toFixed(2)} MAD</p>
                </div>
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Prix min</p>
                  <p className="text-lg font-semibold">{stockStats.price_statistics.close.min.toFixed(2)} MAD</p>
                </div>
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Prix max</p>
                  <p className="text-lg font-semibold">{stockStats.price_statistics.close.max.toFixed(2)} MAD</p>
                </div>
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-xs text-gray-600">Volume moyen</p>
                  <p className="text-lg font-semibold">{(stockStats.volume_statistics.mean / 1000).toFixed(0)}K</p>
                </div>
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

