import { useState } from 'react'

export default function Settings() {
  const [darkMode] = useState(true)

  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Settings</h2>
        <p className="mt-4 text-slate-300">Dark mode is enabled for this professional interview experience.</p>
        <div className="mt-6 rounded-3xl bg-slate-900 p-6 text-slate-200">
          <p><strong>Theme:</strong> {darkMode ? 'Dark' : 'Light'}</p>
        </div>
      </section>
    </main>
  )
}
