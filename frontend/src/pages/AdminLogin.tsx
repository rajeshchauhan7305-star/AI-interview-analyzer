import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function AdminLogin() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      const response = await api.post('/admin/login', { email, password })
      localStorage.setItem('token', response.data.access_token)
      navigate('/admin')
    } catch (err) {
      setError('Admin login failed. Check credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto max-w-xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Admin Login</h2>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <label className="block text-sm text-slate-300">
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white"
            />
          </label>
          <label className="block text-sm text-slate-300">
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white"
            />
          </label>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <button className="button-glass w-full" type="submit" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign in as Admin'}
          </button>
        </form>
      </section>
    </main>
  )
}
