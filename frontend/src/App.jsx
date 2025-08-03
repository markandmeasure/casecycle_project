import { useState } from 'react'
import './App.css'

function App() {
  const [opportunities, setOpportunities] = useState(null)
  const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '')

  const fetchOpportunities = async () => {
    try {
      const response = await fetch(new URL('/opportunities/', API_BASE_URL))
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
