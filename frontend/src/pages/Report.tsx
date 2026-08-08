import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Report() {
  const [reports, setReports] = useState<any[]>([])
  const [error, setError] = useState('')

  useEffect(() => {
    api.get('/reports/me')
      .then((response) => setReports(response.data))
      .catch(() => setError('Unable to load reports.'))
  }, [])

  const downloadReport = async (id: number) => {
    try {
      const response = await api.get(`/interviews/reports/${id}`, { responseType: 'blob' })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `report_${id}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
    } catch {
      setError('Unable to download report.')
    }
  }

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">My Reports</h2>
        {error && <p className="mt-4 text-rose-400">{error}</p>}
        <div className="mt-8 space-y-4">
          {reports.length ? reports.map((report) => (
            <div key={report.id} className="rounded-3xl bg-slate-900 p-5">
              <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-white">Interview #{report.interview_id}</p>
                  <p className="text-slate-400">Score: {report.overall_score}</p>
                </div>
                <button className="button-glass" onClick={() => downloadReport(report.id)} type="button">
                  Download PDF
                </button>
              </div>
            </div>
          )) : <p className="text-slate-400">No reports yet.</p>}
        </div>
      </section>
    </main>
  )
}
