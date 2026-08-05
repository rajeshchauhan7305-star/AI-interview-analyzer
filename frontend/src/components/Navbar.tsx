import { Link, useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'

export default function Navbar() {
  const [token, setToken] = useState<string | null>(null)
  const navigate = useNavigate()

  useEffect(() => {
    setToken(localStorage.getItem('token'))
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
    navigate('/login')
  }

  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-slate-950/90 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-6 py-4">
        <Link to="/" className="text-lg font-semibold text-white">
          AI Interview Analyzer
        </Link>
        <nav className="flex flex-wrap items-center gap-2">
          <Link className="button-glass" to="/">
            Home
          </Link>
          {token ? (
            <>
              <Link className="button-glass" to="/dashboard">
                Dashboard
              </Link>
              <Link className="button-glass" to="/interview">
                Interview
              </Link>
              <Link className="button-glass" to="/history">
                History
              </Link>
              <Link className="button-glass" to="/report">
                Reports
              </Link>
              <Link className="button-glass" to="/profile">
                Profile
              </Link>
              <Link className="button-glass" to="/settings">
                Settings
              </Link>
              <Link className="button-glass" to="/admin">
                Admin
              </Link>
              <button className="button-glass" onClick={handleLogout} type="button">
                Logout
              </button>
            </>
          ) : (
            <>
              <Link className="button-glass" to="/login">
                Login
              </Link>
              <Link className="button-glass" to="/register">
                Register
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  )
}
