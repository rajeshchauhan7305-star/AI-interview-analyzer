import { useEffect, useState } from 'react'
import api from '../services/api'

export default function Profile() {
  const [profile, setProfile] = useState<any>(null)
  const [resume, setResume] = useState<any>(null)
  const [photoFile, setPhotoFile] = useState<File | null>(null)
  const [resumeFile, setResumeFile] = useState<File | null>(null)
  const [message, setMessage] = useState('')

  const loadProfile = async () => {
    const user = await api.get('/users/me')
    setProfile(user.data)
  }

  const loadResume = async () => {
    try {
      const response = await api.get('/resume/me')
      setResume(response.data)
    } catch {
      setResume(null)
    }
  }

  useEffect(() => {
    loadProfile()
    loadResume()
  }, [])

  const handleUploadPhoto = async () => {
    if (!photoFile) return
    const formData = new FormData()
    formData.append('file', photoFile)
    const response = await api.post('/users/me/photo', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    setProfile((prev: any) => ({ ...prev, photo_url: response.data.photo_url }))
    setMessage('Profile photo uploaded successfully.')
  }

  const handleUploadResume = async () => {
    if (!resumeFile) return
    const formData = new FormData()
    formData.append('file', resumeFile)
    await api.post('/resume/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    setMessage('Resume uploaded successfully.')
    loadResume()
  }

  if (!profile) return <div className="p-16 text-center">Loading...</div>

  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <section className="card-glass space-y-6">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start">
          <div className="flex-1 rounded-3xl bg-slate-900 p-6">
            <h2 className="text-3xl font-semibold">My Profile</h2>
            <div className="mt-6 space-y-3 text-slate-300">
              <p><strong>Name:</strong> {profile.full_name}</p>
              <p><strong>Email:</strong> {profile.email}</p>
              <p><strong>Verified:</strong> {profile.is_verified ? 'Yes' : 'No'}</p>
              <p><strong>Joined:</strong> {new Date(profile.created_at).toLocaleDateString()}</p>
              {profile.photo_url && (
                <div className="mt-4">
                  <img src={profile.photo_url} alt="Profile" className="h-40 w-40 rounded-3xl object-cover" />
                </div>
              )}
            </div>
          </div>
          <div className="w-full max-w-xl rounded-3xl bg-slate-900 p-6">
            <h3 className="text-2xl font-semibold">Upload assets</h3>
            <div className="mt-5 space-y-4">
              <label className="block text-sm text-slate-300">
                Profile photo
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => setPhotoFile(e.target.files?.[0] ?? null)}
                  className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white"
                />
              </label>
              <button className="button-glass w-full" onClick={handleUploadPhoto} type="button">
                Upload Photo
              </button>
              <label className="block text-sm text-slate-300">
                Resume (PDF/DOCX)
                <input
                  type="file"
                  accept=".pdf,.docx"
                  onChange={(e) => setResumeFile(e.target.files?.[0] ?? null)}
                  className="mt-2 w-full rounded-2xl border border-white/10 bg-slate-950 p-3 text-white"
                />
              </label>
              <button className="button-glass w-full" onClick={handleUploadResume} type="button">
                Upload Resume
              </button>
              {resume?.file_path && (
                <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
                  <p className="text-sm text-slate-400">Latest resume</p>
                  <a href={resume.file_path} target="_blank" rel="noreferrer" className="text-white underline">
                    Download resume
                  </a>
                </div>
              )}
            </div>
          </div>
        </div>
        {message && <p className="text-emerald-300">{message}</p>}
      </section>
    </main>
  )
}
