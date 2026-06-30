import { ref } from 'vue'
import { getFavourites, toggleFavourite } from '@/api'
import { useAuth } from './useAuth'

// Module-level — shared across all components
const favouriteTeams = ref([])
const favouriteTeamIds = ref(new Set())

export function useFavourites() {
  const { isLoggedIn } = useAuth()

  async function loadFavourites() {
    if (!isLoggedIn.value) {
      favouriteTeams.value = []
      favouriteTeamIds.value = new Set()
      return
    }
    try {
      const data = await getFavourites()
      favouriteTeams.value = data
      favouriteTeamIds.value = new Set(data.map(f => f.team.id))
    } catch {
      favouriteTeams.value = []
      favouriteTeamIds.value = new Set()
    }
  }

  function isFavourite(teamId) {
    return favouriteTeamIds.value.has(teamId)
  }

  async function toggle(teamId) {
    const { is_favourite } = await toggleFavourite(teamId)
    if (is_favourite) {
      favouriteTeamIds.value = new Set([...favouriteTeamIds.value, teamId])
    } else {
      const next = new Set(favouriteTeamIds.value)
      next.delete(teamId)
      favouriteTeamIds.value = next
      favouriteTeams.value = favouriteTeams.value.filter(f => f.team.id !== teamId)
    }
    return is_favourite
  }

  return { favouriteTeams, favouriteTeamIds, loadFavourites, isFavourite, toggle }
}
