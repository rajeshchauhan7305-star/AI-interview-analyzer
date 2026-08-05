import { useEffect, useState } from 'react'
import axios from 'axios'

export default function History() {
  const [history, setHistory] = useState<any[]>([])

  useEffect(() => {
    axios.get('/api/interviews/history', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then((response) => setHistory(response.data))
  }, [])

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Interview History</h2>
        <div className="mt-8 space-y-4">
          {history.length ? history.map((interview) => (
            <div key={interview.id} className="rounded-3xl bg-slate-900 p-5">
              <p>Interview #{interview.id}</p>
              <p>Score: {interview.total_score}</p>
              <p>Result: {interview.recommendation}</p>
            </div>
          )) : <p className="text-slate-400">No history available.</p>}
        </div>
      </section>
    </main>
  )
}
