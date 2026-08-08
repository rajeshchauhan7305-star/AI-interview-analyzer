import { useEffect, useState } from 'react'
import api from '../services/api'

export default function History() {
  const [history, setHistory] = useState<any[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/interviews/history')
      .then((response) => setHistory(response.data))
      .catch(() => setError('Unable to load interview history.'))
  }, [])

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Interview History</h2>
        {error && <p className="mt-4 text-rose-400">{error}</p>}
        <div className="mt-8 space-y-4">
          {history.length ? history.map((interview) => (
            <div key={interview.id} className="rounded-3xl bg-slate-900 p-5">
              <p className="text-white">Interview #{interview.id}</p>
              <p className="text-slate-400">Category: {interview.category_name || interview.category_id}</p>
              <p className="text-slate-400">Difficulty: {interview.difficulty}</p>
              <p className="text-slate-400">Score: {interview.total_score}</p>
              <p className="text-slate-400">Result: {interview.recommendation}</p>
              <p className="text-slate-400">Date: {new Date(interview.created_at).toLocaleString()}</p>
            </div>
          )) : <p className="text-slate-400">No history yet.</p>}
        </div>
      </section>
    </main>
  )
}
