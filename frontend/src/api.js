import axios from 'axios'

const api = axios.create({
  baseURL: '/api/',
  headers: { 'Content-Type': 'application/json' },
})

// Attach JWT access token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auto-refresh access token on 401
let isRefreshing = false
let refreshQueue = []

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config
    if (error.response?.status === 401 && !original._retry) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          refreshQueue.push({ resolve, reject })
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }
      original._retry = true
      isRefreshing = true
      const refresh = localStorage.getItem('refresh')
      if (refresh) {
        try {
          const { data } = await axios.post('/api/auth/refresh/', { refresh })
          localStorage.setItem('access', data.access)
          if (data.refresh) localStorage.setItem('refresh', data.refresh)
          refreshQueue.forEach((p) => p.resolve(data.access))
          refreshQueue = []
          original.headers.Authorization = `Bearer ${data.access}`
          return api(original)
        } catch (e) {
          refreshQueue.forEach((p) => p.reject(e))
          refreshQueue = []
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
        } finally {
          isRefreshing = false
        }
      } else {
        isRefreshing = false
      }
    }
    return Promise.reject(error)
  },
)

// ── Auth 
export async function login(email, password) {
  const { data } = await api.post('auth/login/', { email, password })
  localStorage.setItem('access', data.access)
  localStorage.setItem('refresh', data.refresh)
  return data
}

export async function register(payload) {
  const { data } = await api.post('auth/register/', payload)
  localStorage.setItem('access', data.access)
  localStorage.setItem('refresh', data.refresh)
  return data
}

export async function logoutApi() {
  const refresh = localStorage.getItem('refresh')
  try {
    await api.post('auth/logout/', { refresh })
  } catch {}
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}

export async function getMe() {
  const { data } = await api.get('auth/me/')
  return data
}

export async function updateMe(payload) {
  const { data } = await api.patch('auth/me/', payload)
  return data
}

export async function changePassword(current_password, new_password) {
  const { data } = await api.post('auth/change-password/', { current_password, new_password })
  return data
}

// ── Admin — users  
export async function adminGetUsers(params = {}) {
  const { data } = await api.get('users/admin/', { params })
  return data
}

export async function adminUpdateUser(id, payload) {
  const { data } = await api.patch(`users/admin/${id}/`, payload)
  return data
}

export async function adminDeleteUser(id) {
  await api.delete(`users/admin/${id}/`)
}

// ── Admin — create records  
export async function adminCreateLeagueTeam(payload) {
  const { data } = await api.post('league-teams/', payload)
  return data
}

export async function adminCreateMatch(payload) {
  const { data } = await api.post('matches/', payload)
  return data
}

export async function adminCreatePlayerStats(payload) {
  const { data } = await api.post('player-stats/', payload)
  return data
}

// ── Favourites  
export async function getFavourites() {
  const { data } = await api.get('favourites/')
  return data
}

export async function toggleFavourite(teamId) {
  const { data } = await api.post(`favourites/${teamId}/toggle/`)
  return data
}

// ── Pagination helpers  
export async function fetchAll(endpoint, params = {}) {
  const results = []
  let url = endpoint
  while (url) {
    const res = await api.get(url, { params: url === endpoint ? params : {} })
    results.push(...res.data.results)
    url = res.data.next ? res.data.next.replace(/^.*\/api\//, '') : null
  }
  return results
}

export async function fetchPages(endpoint, pages = 5, params = {}) {
  const first = await api.get(endpoint, { params })
  const total = first.data.count
  const totalPages = Math.ceil(total / 20)
  const remaining = Math.min(pages, totalPages) - 1
  if (remaining <= 0) return first.data.results

  const rest = await Promise.all(
    Array.from({ length: remaining }, (_, i) =>
      api.get(endpoint, { params: { ...params, page: i + 2 } }),
    ),
  )
  return [...first.data.results, ...rest.flatMap((r) => r.data.results)]
}

export default api
