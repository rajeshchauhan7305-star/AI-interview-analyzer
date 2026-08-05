import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Profile() {
  const [profile, setProfile] = useState<any>(null)

  useEffect(() => {
    axios.get('/api/users/me', { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } })
      .then((response) => setProfile(response.data))
  }, [])

  if (!profile) return <div className="p-16 text-center">Loading...</div>

  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <section className="card-glass">
        <h2 className="text-3xl font-semibold">My Profile</h2>
        <div className="mt-6 space-y-3 text-slate-300">
          <p><strong>Name:</strong> {profile.full_name}</p>
          <p><strong>Email:</strong> {profile.email}</p>
          <p><strong>Verified:</strong> {profile.is_verified ? 'Yes' : 'No'}</p>
        </div>
      </section>
    </main>
  )
}
