import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { fetchAll, fetchPages } from '@/api'

const LEAGUE_FLAGS = { 'NBA': '🇺🇸', 'Euroleague': '🇪🇺' }
const STATUS_MAP = { 'finished': 'finished', 'scheduled': 'scheduled', 'live': 'live' }

function normalizeMatch(m) {
  const statusKey = m.status.name.toLowerCase()
  const dt = new Date(m.match_date)
  return {
    id: m.id,
    leagueId: String(m.league.id),
    league: m.league.name,
    leagueLogo: m.league.logo,
    leagueFlag: LEAGUE_FLAGS[m.league.name] ?? '🏀',
    leagueCountry: m.home_team.city?.country?.name ?? '',
    homeTeamId: m.home_team.id,
    awayTeamId: m.away_team.id,
    homeTeam: m.home_team.name,
    awayTeam: m.away_team.name,
    homeTeamLogo: m.home_team.logo,
    awayTeamLogo: m.away_team.logo,
    homeScore: m.home_score,
    awayScore: m.away_score,
    status: STATUS_MAP[statusKey] ?? 'scheduled',
    time: dt.toLocaleTimeString('hr-HR', { hour: '2-digit', minute: '2-digit' }),
    quarter: null,
    clock: null,
    hall: m.hall?.name ?? null,
    matchDate: m.match_date,
    season: m.season?.name ?? '',
  }
}

export const useScoresStore = defineStore('scores', () => {
  const matches = ref([])
  const leagues = ref([])
  const loading = ref(false)
  const activeFilter = ref('all')
  const activeLeague = ref('all')

  const groupedMatches = computed(() => {
    const filtered = matches.value.filter(m => {
      if (activeLeague.value !== 'all' && m.leagueId !== activeLeague.value) return false
      if (activeFilter.value === 'live') return m.status === 'live'
      if (activeFilter.value === 'scheduled') return m.status === 'scheduled'
      if (activeFilter.value === 'finished') return m.status === 'finished'
      return true
    })

    const groups = {}
    for (const m of filtered) {
      if (!groups[m.leagueId]) {
        groups[m.leagueId] = {
          leagueId: m.leagueId,
          league: m.league,
          leagueFlag: m.leagueFlag,
          leagueLogo: m.leagueLogo,
          leagueCountry: m.leagueCountry,
          matches: [],
        }
      }
      groups[m.leagueId].matches.push(m)
    }
    return Object.values(groups)
  })

  const liveCount = computed(() =>
    matches.value.filter(m => m.status === 'live').length
  )

  function getMatchById(id) {
    return matches.value.find(m => m.id === Number(id))
  }

  async function fetchMatches() {
    loading.value = true
    try {
      const totalPages = Math.ceil(254 / 20) // safe upper bound
      const raw = await fetchPages('matches/', totalPages)
      matches.value = raw.map(normalizeMatch)
    } catch (e) {
      console.error('fetchMatches:', e)
    } finally {
      loading.value = false
    }
  }

  async function fetchLeagues() {
    try {
      const res = await fetchAll('leagues/')
      leagues.value = res
    } catch (e) {
      console.error('fetchLeagues:', e)
    }
  }

  async function init() {
    await Promise.all([fetchMatches(), fetchLeagues()])
  }

  return {
    matches, leagues, loading,
    activeFilter, activeLeague,
    groupedMatches, liveCount,
    getMatchById, init, fetchMatches, fetchLeagues,
  }
})
