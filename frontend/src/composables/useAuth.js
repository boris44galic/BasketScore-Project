import { ref, computed } from 'vue'
import { getMe, logoutApi } from '../api'

// Module-level — same state shared across every component
const isLoggedIn = ref(false)
const user = ref(null)
const isAdmin = computed(() => user.value?.is_staff === true)

export function useAuth() {
  const loadUser = async () => {
    const token = localStorage.getItem('access')
    if (!token) {
      isLoggedIn.value = false
      return
    }
    try {
      user.value = await getMe()
      isLoggedIn.value = true
    } catch {
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      user.value = null
      isLoggedIn.value = false
    }
  }

  const logoutUser = async () => {
    await logoutApi()
    user.value = null
    isLoggedIn.value = false
  }

  return { isLoggedIn, isAdmin, user, loadUser, logoutUser }
}
