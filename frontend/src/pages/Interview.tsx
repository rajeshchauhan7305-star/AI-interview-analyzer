import { useEffect, useMemo, useState } from 'react'
import api from '../services/api'

const difficulties = ['Easy', 'Medium', 'Hard']

export default function Interview() {
  const [categories, setCategories] = useState<any[]>([])
  const [categoryId, setCategoryId] = useState<number>(1)
  const [difficulty, setDifficulty] = useState('Easy')
  const [interviewId, setInterviewId] = useState<number | null>(null)
  const [questions, setQuestions] = useState<any[]>([])
  const [answers, setAnswers] = useState<Record<number, string>>({})
  const [analysis, setAnalysis] = useState<Record<number, any>>({})
  const [transcript, setTranscript] = useState('')
  const [message, setMessage] = useState('')

  const selectedCategory = useMemo(() => categories.find((category) => category.id === categoryId), [categories, categoryId])

  useEffect(() => {
    api.get('/questions/categories')
      .then((response) => {
        setCategories(response.data)
        if (response.data.length) {
          setCategoryId(response.data[0].id)
        }
      })
      .catch(() => {})
  }, [])

  const startInterview = async () => {
    setMessage('Generating interview session...')
    const response = await api.post('/interviews/start', { category_id: categoryId, difficulty })
    setInterviewId(response.data.interview_id)
    setQuestions(response.data.questions)
    setAnalysis({})
    setAnswers({})
    setMessage('Interview session started. Answer each question and submit for analysis.')
  }

  const handleAnswerChange = (questionId: number, value: string) => {
    setAnswers((prev) => ({ ...prev, [questionId]: value }))
  }

  const handleSubmitAnswer = async (questionId: number) => {
    const answer = answers[questionId]
    if (!interviewId || !answer) return
    const response = await api.post('/interviews/answer', {
      interview_id: interviewId,
      question_id: questionId,
      answer,
    })
    setAnalysis((prev) => ({ ...prev, [questionId]: response.data }))
    setMessage('Answer saved and analyzed successfully.')
  }

  const handleFinishInterview = async () => {
    if (!interviewId) return
    const response = await api.post('/interviews/finish', {
      interview_id: interviewId,
      summary: 'Completed interview session',
    })
    setMessage(`Interview finished with overall score ${response.data.overall_score}.`)
  }

  const handleTranscribe = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (!file) return
    const formData = new FormData()
    formData.append('file', file)
    const response = await api.post('/interviews/transcribe', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    setTranscript(response.data.transcript)
  }

  return (
    <main className="mx-auto max-w-6xl px-6 py-16">
      <section className="card-glass space-y-8">
        <div>
          <h2 className="text-3xl font-semibold">Mock Interview</h2>
          <p className="mt-3 text-slate-400">Select a category, set difficulty, and answer AI-generated questions. Use the transcript option to process voice answers.</p>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          <select className="rounded-2xl border border-white/10 bg-slate-950 p-3" value={categoryId} onChange={(e) => setCategoryId(Number(e.target.value))}>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
          <select className="rounded-2xl border border-white/10 bg-slate-950 p-3" value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            {difficulties.map((level) => (
              <option key={level}>{level}</option>
            ))}
          </select>
          <button className="button-glass" onClick={startInterview} type="button">Start Interview</button>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <label className="block text-sm text-slate-300">
            Upload voice answer
            <input type="file" accept="audio/*" onChange={handleTranscribe} className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white" />
          </label>
          {transcript && (
            <div className="rounded-3xl border border-white/10 bg-white/5 p-5 text-slate-300">
              <p className="text-sm text-slate-400">Transcription</p>
              <p className="mt-2">{transcript}</p>
            </div>
          )}
        </div>

        {message && <div className="rounded-3xl border border-emerald-500/30 bg-emerald-500/5 p-4 text-emerald-200">{message}</div>}

        <div className="space-y-6">
          {questions.map((question) => (
            <div key={question.id} className="rounded-3xl border border-white/10 bg-slate-900 p-6">
              <p className="text-lg font-semibold text-white">Q: {question.text}</p>
              <textarea
                rows={4}
                value={answers[question.id] || ''}
                onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                className="mt-4 w-full rounded-3xl border border-white/10 bg-slate-950 p-4 text-white"
              />
              <div className="mt-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <button className="button-glass" onClick={() => handleSubmitAnswer(question.id)} type="button">
                  Save Answer
                </button>
                {analysis[question.id] && (
                  <div className="rounded-3xl bg-white/5 p-4 text-slate-300">
                    <p className="font-semibold">AI Feedback</p>
                    <p className="mt-2 text-sm">{analysis[question.id].ai_feedback}</p>
                    <div className="mt-3 grid gap-2 sm:grid-cols-4 text-xs text-slate-300">
                      <span>Grammar: {analysis[question.id].grammar_score}</span>
                      <span>Technical: {analysis[question.id].technical_score}</span>
                      <span>Communication: {analysis[question.id].communication_score}</span>
                      <span>Confidence: {analysis[question.id].confidence_score}</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {questions.length > 0 && (
          <button className="button-glass w-full" onClick={handleFinishInterview} type="button">
            Finish Interview & Generate Report
          </button>
        )}
      </section>
    </main>
  )
}
