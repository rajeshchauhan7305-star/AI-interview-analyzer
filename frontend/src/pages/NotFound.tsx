import { Link } from 'react-router-dom'

export default function NotFound() {
  return (
    <main className="mx-auto max-w-4xl px-6 py-16 text-center">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Page Not Found</h2>
        <p className="mt-4 text-slate-400">The page you are looking for does not exist.</p>
        <Link className="button-glass mt-8 inline-block" to="/">
          Go back home
        </Link>
      </section>
    </main>
  )
}
