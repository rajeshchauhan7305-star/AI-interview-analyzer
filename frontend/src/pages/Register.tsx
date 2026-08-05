import { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Register() {
  const [email, setEmail] = useState('')
  const [fullName, setFullName] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      await axios.post('/api/auth/register', { email, full_name: fullName, password })
      navigate('/login')
    } catch (err) {
      setError('Registration failed. Try again.')
    }
  }

  return (
    <main className="mx-auto max-w-xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Register</h2>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <label className="block text-sm text-slate-300">
            Full Name
            <input value={fullName} onChange={(e) => setFullName(e.target.value)} className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white" />
          </label>
          <label className="block text-sm text-slate-300">
            Email
            <input value={email} onChange={(e) => setEmail(e.target.value)} className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white" />
          </label>
          <label className="block text-sm text-slate-300">
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white" />
          </label>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <button className="button-glass w-full" type="submit">Register</button>
        </form>
      </section>
    </main>
  )
}
