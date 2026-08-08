import { useState } from 'react'
import api from '../services/api'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    setLoading(true)
    setMessage('')
    setError('')

    try {
      await api.post('/auth/forgot-password', { email })
      setMessage('A password reset link has been sent if the email exists.')
    } catch (err) {
      setError('Unable to send password reset link. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="mx-auto max-w-xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Forgot Password</h2>
        <p className="mt-3 text-slate-400">Enter your email and we will send instructions to reset your password.</p>
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
          {message && <p className="text-sm text-emerald-400">{message}</p>}
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <button className="button-glass w-full" type="submit" disabled={loading}>
            {loading ? 'Sending…' : 'Send Reset Link'}
          </button>
        </form>
      </section>
    </main>
  )
}
