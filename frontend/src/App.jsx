import { useState } from 'react'
import './App.css'

function App() {
  const [opportunities, setOpportunities] = useState(null)
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  const fetchOpportunities = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/opportunities/`)
      const data = await response.json()
      setOpportunities(data)
    } catch (error) {
      console.error('Error fetching opportunities:', error)
    }
  }

  return (
    <div className="App">
      <button onClick={fetchOpportunities}>Fetch Opportunities</button>
      {opportunities && (
        <pre>{JSON.stringify(opportunities, null, 2)}</pre>
      )}
    </div>
  )
}

export default App
