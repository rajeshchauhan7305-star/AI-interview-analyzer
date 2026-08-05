import { useEffect, useState } from 'react'
import axios from 'axios'

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null)

  useEffect(() => {
    axios.get('/api/admin/stats', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then((response) => setStats(response.data))
  }, [])

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Admin Dashboard</h2>
        <div className="mt-8 grid gap-6 sm:grid-cols-3">
          <div className="rounded-3xl bg-slate-900 p-6 shadow-glass">
            <p className="text-sm text-slate-400">Total Users</p>
            <p className="mt-3 text-4xl font-bold">{stats?.total_users ?? '–'}</p>
          </div>
          <div className="rounded-3xl bg-slate-900 p-6 shadow-glass">
            <p className="text-sm text-slate-400">Active Users</p>
            <p className="mt-3 text-4xl font-bold">{stats?.active_users ?? '–'}</p>
          </div>
          <div className="rounded-3xl bg-slate-900 p-6 shadow-glass">
            <p className="text-sm text-slate-400">Total Interviews</p>
            <p className="mt-3 text-4xl font-bold">{stats?.total_interviews ?? '–'}</p>
          </div>
        </div>
      </section>
    </main>
  )
}
