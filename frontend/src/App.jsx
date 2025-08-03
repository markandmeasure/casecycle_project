import { useState } from 'react'
import './App.css'

function App() {
  const [opportunities, setOpportunities] = useState(null)
  const [errorMessage, setErrorMessage] = useState(null)
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

  const fetchOpportunities = async () => {
    try {
      setErrorMessage(null)
      const response = await fetch(`${API_BASE_URL}/opportunities/`)
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setOpportunities(data)
    } catch (error) {
      console.error('Error fetching opportunities:', error)
      setErrorMessage('Unable to fetch opportunities. Please try again later.')
    }
  }

  return (
    <div className="App">
      <button onClick={fetchOpportunities}>Fetch Opportunities</button>
      {errorMessage && (
        <div role="alert">{errorMessage}</div>
      )}
      {opportunities && (
        <pre>{JSON.stringify(opportunities, null, 2)}</pre>
      )}
    </div>
  )
}

export default App
