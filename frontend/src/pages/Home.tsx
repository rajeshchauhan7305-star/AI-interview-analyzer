import { Link } from 'react-router-dom'

const features = [
  {
    title: 'Practice mock interviews',
    description: 'Generate questions, rehearse answers, and build confidence before the real interview.',
  },
  {
    title: 'Analyze your responses',
    description: 'Get AI-powered feedback on tone, structure, and relevance to improve your delivery.',
  },
  {
    title: 'Track progress over time',
    description: 'Save interview sessions, review your history, and identify your strongest areas.',
  },
]

export default function Home() {
  return (
    <main className="min-h-screen px-6 py-16">
      <div className="mx-auto grid max-w-7xl gap-10">
        <section className="card-glass grid gap-10 lg:grid-cols-[1.4fr_0.9fr] lg:items-center">
          <div className="space-y-8">
            <div className="inline-flex rounded-full bg-slate-900 px-4 py-2 text-sm uppercase tracking-[0.3em] text-slate-300">
              AI interview preparation
            </div>
            <div>
              <h1 className="text-5xl font-bold tracking-tight text-white sm:text-6xl">
                Practice smarter and improve your interview performance.
              </h1>
              <p className="mt-5 max-w-3xl text-lg leading-8 text-slate-300">
                AI Interview Analyzer helps you rehearse answers, receive real-time feedback, and generate polished reports that showcase your progress.
              </p>
            </div>
            <div className="flex flex-wrap gap-4">
              <Link className="button-glass" to="/login">
                Login
              </Link>
              <Link className="button-glass" to="/register">
                Register
              </Link>
            </div>
          </div>
          <div className="rounded-[32px] border border-white/10 bg-slate-950/70 p-8 shadow-glass">
            <h2 className="text-2xl font-semibold text-white">Get started in seconds</h2>
            <p className="mt-4 text-slate-300">
              Create an account to start practicing interview questions and tracking your progress. The more you prepare, the stronger your performance becomes.
            </p>
            <div className="mt-8 space-y-4">
              <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
                <p className="text-sm text-slate-400">Step 1</p>
                <p className="mt-2 text-white">Sign in or register to access your dashboard.</p>
              </div>
              <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
                <p className="text-sm text-slate-400">Step 2</p>
                <p className="mt-2 text-white">Generate interview questions, practice answers, and get AI insights.</p>
              </div>
              <div className="rounded-3xl border border-white/10 bg-white/5 p-5">
                <p className="text-sm text-slate-400">Step 3</p>
                <p className="mt-2 text-white">Review your history and share reports with confidence.</p>
              </div>
            </div>
          </div>
        </section>

        <section className="grid gap-6 md:grid-cols-3">
          {features.map((feature) => (
            <article key={feature.title} className="card-glass p-6">
              <h3 className="text-xl font-semibold text-white">{feature.title}</h3>
              <p className="mt-3 text-slate-300 leading-7">{feature.description}</p>
            </article>
          ))}
        </section>
      </div>
    </main>
  )
}
