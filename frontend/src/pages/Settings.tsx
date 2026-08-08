import { useEffect, useState } from 'react'

export default function Settings() {
  const [darkMode, setDarkMode] = useState(true)

  useEffect(() => {
    const stored = localStorage.getItem('darkMode')
    setDarkMode(stored !== 'false')
  }, [])

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode)
    localStorage.setItem('darkMode', darkMode ? 'true' : 'false')
  }, [darkMode])

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Settings</h2>
        <div className="mt-6 space-y-5 text-slate-300">
          <div className="flex items-center justify-between rounded-3xl border border-white/10 bg-slate-900 p-6">
            <div>
              <p className="font-semibold text-white">Theme</p>
              <p className="text-slate-400">Toggle the UI theme for your session.</p>
            </div>
            <button className="button-glass" type="button" onClick={() => setDarkMode((value) => !value)}>
              {darkMode ? 'Switch to Light' : 'Switch to Dark'}
            </button>
          </div>
          <div className="rounded-3xl border border-white/10 bg-slate-900 p-6">
            <p className="font-semibold text-white">Notification Preferences</p>
            <p className="mt-2 text-slate-400">Preferences are saved locally in your browser.</p>
          </div>
        </div>
      </section>
    </main>
  )
}
