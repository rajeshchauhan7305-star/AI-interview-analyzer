import { Link } from 'react-router-dom'

export default function Home() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h1 className="text-5xl font-bold">AI Interview Analyzer</h1>
        <p className="mt-6 max-w-3xl text-slate-300">
          Practice mock interviews, analyze responses with AI, track your history, and generate reports.
        </p>
        <div className="mt-10 flex flex-wrap gap-4">
          <Link className="button-glass" to="/login">Login</Link>
          <Link className="button-glass" to="/register">Register</Link>
        </div>
      </section>
    </main>
  )
}
