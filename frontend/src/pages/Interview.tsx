import { useState } from 'react'
import axios from 'axios'

const categories = [
  { id: 1, name: 'Software Developer' },
  { id: 2, name: 'Python Developer' },
  { id: 3, name: 'Web Developer' },
]

export default function Interview() {
  const [categoryId, setCategoryId] = useState(1)
  const [difficulty, setDifficulty] = useState('Easy')
  const [questions, setQuestions] = useState<any[]>([])

  const startInterview = async () => {
    const token = localStorage.getItem('token')
    const response = await axios.post('/api/interviews/start', { category_id: categoryId, difficulty }, { headers: { Authorization: `Bearer ${token}` } })
    setQuestions(response.data.questions)
  }

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">Start Mock Interview</h2>
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          <select className="rounded-2xl border border-white/10 bg-slate-950 p-3" value={categoryId} onChange={(e) => setCategoryId(Number(e.target.value))}>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
          <select className="rounded-2xl border border-white/10 bg-slate-950 p-3" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            <option>Easy</option>
            <option>Medium</option>
            <option>Hard</option>
          </select>
        </div>
        <button className="button-glass mt-6" onClick={startInterview}>Generate Questions</button>
        <div className="mt-8 space-y-4">
          {questions.map((question) => (
            <div key={question.id} className="rounded-3xl bg-slate-900 p-5">
              <p className="font-semibold">Q: {question.text}</p>
            </div>
          ))}
        </div>
      </section>
    </main>
  )
}
