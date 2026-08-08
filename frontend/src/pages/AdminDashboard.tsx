import { useEffect, useState } from 'react'
import api from '../services/api'

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null)
  const [users, setUsers] = useState<any[]>([])
  const [error, setError] = useState('')

  const loadStats = async () => {
    try {
      const response = await api.get('/admin/stats')
      setStats(response.data)
    } catch {
      setError('Unable to load admin stats.')
    }
  }

  const loadUsers = async () => {
    try {
      const response = await api.get('/admin/users')
      setUsers(response.data)
    } catch {
      setError('Unable to load user list.')
    }
  }

  useEffect(() => {
    loadStats()
    loadUsers()
  }, [])

  const handleUserAction = async (userId: number, action: 'block' | 'unblock' | 'delete') => {
    try {
      await api.post(`/admin/users/${userId}/${action}`)
      loadUsers()
    } catch {
      setError('Unable to update user.')
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-16">
      <section className="card-glass mb-8">
        <h2 className="text-3xl font-semibold">Admin Dashboard</h2>
        {error && <p className="mt-4 text-rose-400">{error}</p>}
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

      <section className="card-glass">
        <h3 className="text-2xl font-semibold">Manage Users</h3>
        <div className="mt-6 space-y-4">
          {users.length ? users.map((user) => (
            <div key={user.id} className="rounded-3xl bg-slate-900 p-5">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-white">{user.full_name}</p>
                  <p className="text-slate-400">{user.email}</p>
                  <p className="text-slate-400">Verified: {user.is_verified ? 'Yes' : 'No'}</p>
                  <p className="text-slate-400">Status: {user.is_active ? 'Active' : 'Blocked'}</p>
                </div>
                <div className="flex flex-wrap gap-2">
                  <button className="button-glass" onClick={() => handleUserAction(user.id, user.is_active ? 'block' : 'unblock')}>
                    {user.is_active ? 'Block' : 'Unblock'}
                  </button>
                  <button className="button-glass" onClick={() => handleUserAction(user.id, 'delete')}>
                    Delete
                  </button>
                </div>
              </div>
            </div>
          )) : <p className="text-slate-400">No users found.</p>}
        </div>
      </section>
    </main>
  )
}
