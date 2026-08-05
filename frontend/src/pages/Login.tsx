import { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      const response = await axios.post('/api/auth/login', { email, password })
      localStorage.setItem('token', response.data.access_token)
      navigate('/dashboard')
    } catch (err) {
      setError('Login failed. Check credentials.')
    }
  }

  return (
    <main className="mx-auto max-w-xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Login</h2>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <label className="block text-sm text-slate-300">
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white" />
          </label>
          <label className="block text-sm text-slate-300">
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white" />
          </label>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <button className="button-glass w-full" type="submit">Login</button>
        </form>
      </section>
    </main>
  )
}
