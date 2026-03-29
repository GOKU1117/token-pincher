import { useState } from "react"
import axios from "axios"

export default function App() {
  const [prompt, setPrompt] = useState("")
  const [result, setResult] = useState(null)

  const analyze = async () => {
    const res = await axios.post("http://127.0.0.1:8000/analyze", {
      messages: [{ role: "user", content: prompt }]
    })
    setResult(res.data)
  }

  const optimize = async () => {
    const res = await axios.post("http://127.0.0.1:8000/optimize", {
      prompt
    })
    setPrompt(res.data.optimized)
  }

  return (
    <div style={{ padding: 40, fontFamily: "Arial" }}>
      <h1>🦀 TokenPincher</h1>

      <textarea
        style={{ width: "100%", height: 150 }}
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt..."
      />

      <br /><br />

      <button onClick={analyze}>Analyze</button>
      <button onClick={optimize} style={{ marginLeft: 10 }}>
        Optimize
      </button>

      <br /><br />

      {result && (
        <div>
          <p>Tokens: {result.tokens}</p>
          <p>Cost: {result.cost}</p>

          {result.warnings.length > 0 && (
            <ul>
              {result.warnings.map((w, i) => (
                <li key={i}>⚠ {w}</li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  )
}