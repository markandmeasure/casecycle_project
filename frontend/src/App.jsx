import { useState } from 'react'
import './App.css'

function App() {
  const [opportunities, setOpportunities] = useState(null)

  const fetchOpportunities = async () => {
    try {
      const response = await fetch('/opportunities/')
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
