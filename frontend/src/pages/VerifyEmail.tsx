import { useEffect, useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import api from '../services/api'

export default function VerifyEmail() {
  const [searchParams] = useSearchParams()
  const [message, setMessage] = useState('Verifying email...')
  const [error, setError] = useState('')
  const navigate = useNavigate()
  const token = searchParams.get('token')

  useEffect(() => {
    const verify = async () => {
      if (!token) {
        setError('Verification token is missing.')
        setMessage('')
        return
      }
      try {
        await api.post(`/auth/verify-email?token=${encodeURIComponent(token)}`)
        setMessage('Your email has been verified successfully. Redirecting to login...')
        setTimeout(() => navigate('/login'), 1600)
      } catch (err) {
        setError('Unable to verify email. The link may have expired.')
        setMessage('')
      }
    }
    verify()
  }, [token, navigate])

  return (
    <main className="mx-auto max-w-xl px-6 py-16">
      <section className="card-glass text-center">
        <h2 className="text-3xl font-semibold">Email Verification</h2>
        {message && <p className="mt-4 text-slate-300">{message}</p>}
        {error && <p className="mt-4 text-rose-400">{error}</p>}
      </section>
    </main>
  )
}
