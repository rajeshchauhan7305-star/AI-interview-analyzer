import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Report() {
  const [reports, setReports] = useState<any[]>([])

  useEffect(() => {
    axios.get('/api/reports/me', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then((response) => setReports(response.data))
  }, [])

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">My Reports</h2>
        <div className="mt-8 space-y-4">
          {reports.length ? reports.map((report) => (
            <div key={report.id} className="rounded-3xl bg-slate-900 p-5">
              <p>Interview #{report.interview_id}</p>
              <p>Score: {report.overall_score}</p>
            </div>
          )) : <p className="text-slate-400">No reports yet.</p>}
        </div>
      </section>
    </main>
  )
}
