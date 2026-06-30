<template>
  <div class="mx-auto max-w-[1280px] px-4 py-6 md:px-8">
    <RouterLink to="/"
      class="mb-6 inline-flex items-center gap-2 text-sm text-[#64748b] transition hover:text-[#94a3b8]">
      <ChevronLeft class="h-4 w-4" /> Back to scores
    </RouterLink>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div class="h-40 animate-pulse rounded-2xl bg-[#1e293b]" />
      <div class="h-10 animate-pulse rounded-xl bg-[#1e293b]" />
      <div class="h-64 animate-pulse rounded-xl bg-[#1e293b]" />
    </div>

    <template v-else-if="team">
      <!-- Team header -->
      <div class="mb-4 rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6">
        <div class="flex flex-col items-center gap-5 sm:flex-row sm:items-center">
          <div class="flex h-28 w-28 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#1e293b]">
            <img v-if="team.logo" :src="team.logo" :alt="team.name"
              class="h-20 w-20 object-contain" @error="(e) => e.target.style.display='none'" />
            <span v-else class="text-5xl">🏀</span>
          </div>
          <div class="text-center sm:text-left">
            <div class="flex items-center justify-center gap-3 sm:justify-start">
              <h1 class="text-3xl font-extrabold text-white">{{ team.name }}</h1>
              <button @click="isLoggedIn ? toggle(Number(teamId)) : (showLogin = true)"
                class="cursor-pointer rounded-full p-1.5 transition hover:bg-[#1e293b] pl-4"
                :class="isFavourite(Number(teamId)) ? 'text-red-500' : 'text-[#475569] hover:text-red-400'">
                <Heart class="h-6 w-6" :class="isFavourite(Number(teamId)) ? 'fill-red-500' : ''" />
              </button>
            </div>
            <p class="mt-1 text-[15px] text-[#94a3b8]">
              {{ team.city?.name }}{{ team.city?.country?.name ? ', ' + team.city.country.name : '' }}
            </p>
            <div v-if="teamHall" class="mt-2 flex items-center gap-1.5 justify-center sm:justify-start">
              <MapPin class="h-4 w-4 text-[#64748b]" />
              <span class="text-[14px] text-[#64748b]">{{ teamHall }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="mb-4 flex gap-1 rounded-xl bg-[#1e293b] p-1">
        <button v-for="tab in tabs" :key="tab" @click="activeTab = tab"
          class="flex-1 rounded-lg py-2 text-sm font-semibold transition cursor-pointer"
          :class="activeTab === tab ? 'bg-[#0f172a] text-[#f1f5f9] shadow' : 'text-[#64748b] hover:text-[#94a3b8]'">
          {{ tab }}
        </button>
      </div>

      <!-- ── MATCHES ── -->
      <div v-if="activeTab === 'Matches'" class="rounded-xl border border-[#1e293b] bg-[#111827]">
        <div v-if="!teamMatches.length" class="py-12 text-center text-[#64748b]">No matches found.</div>
        <div v-else class="overflow-x-auto">
          <table class="w-full min-w-120 text-[14px]">
            <thead>
              <tr class="border-b border-[#1e293b] text-left">
                <th class="px-4 py-3 font-semibold text-white">Date</th>
                <th class="px-4 py-3 font-semibold text-white">Opponent</th>
                <th class="px-4 py-3 text-center font-semibold text-white">Result</th>
                <th class="px-4 py-3 text-center font-semibold text-white">Score</th>
                <th class="px-4 py-3 text-center font-semibold text-white">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="m in teamMatches" :key="m.id"
                class="border-b border-[#1e293b]/50 transition hover:bg-[#1e293b]/40 last:border-0 cursor-pointer"
                @click="router.push(`/match/${m.id}`)">
                <td class="px-5 py-3 text-[#94a3b8]">{{ formatDate(m.matchDate) }}</td>
                <td class="px-4 py-3">
                  <div class="flex items-center gap-2">
                    <img v-if="m.opponentLogo" :src="m.opponentLogo" class="h-6 w-6 object-contain"
                      @error="(e) => e.target.style.display='none'" />
                    <span class="font-semibold text-[#f1f5f9]">{{ m.opponent }}</span>
                    <span class="text-[11px] text-[#475569]">{{ m.homeAway }}</span>
                  </div>
                </td>
                <td class="px-4 py-3 text-center">
                  <span v-if="m.result" class="text-sm font-bold"
                    :class="m.result === 'W' ? 'text-[#00d4aa]' : 'text-[#ef4444]'">
                    {{ m.result }}
                  </span>
                  <span v-else class="text-[#64748b]">—</span>
                </td>
                <td class="px-4 py-3 text-center font-bold tabular-nums text-white">
                  {{ m.score }}
                </td>
                <td class="px-4 py-3 text-center">
                  <span class="rounded-full px-2.5 py-0.5 text-[11px] font-bold"
                    :class="m.status === 'live'
                      ? 'bg-red-500/10 text-red-400'
                      : m.status === 'finished'
                        ? 'bg-[#1e293b] text-[#64748b]'
                        : 'bg-[#1e293b] text-[#94a3b8]'">
                    {{ m.status === 'live' ? 'LIVE' : m.status === 'finished' ? 'Final' : m.time }}
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- ── PLAYERS ── -->
      <div v-else-if="activeTab === 'Players'" class="rounded-xl border border-[#1e293b] bg-[#111827]">
        <div v-if="playersLoading" class="p-5 space-y-2">
          <div v-for="i in 8" :key="i" class="h-12 animate-pulse rounded bg-[#1e293b]" />
        </div>
        <div v-else-if="!players.length" class="py-12 text-center text-[#64748b]">No players found.</div>
        <div v-else class="divide-y divide-[#1e293b]/60">
          <RouterLink v-for="p in players" :key="p.id" :to="`/player/${p.id}`"
            class="flex items-center gap-4 px-5 py-3.5 transition hover:bg-[#1e293b]/40">
            <div class="flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#1e293b]">
              <img v-if="p.image_url" :src="p.image_url" :alt="`${p.first_name} ${p.last_name}`"
                class="h-full w-full object-cover" @error="(e) => e.target.style.display='none'" />
              <span v-else class="text-[11px] font-bold text-[#64748b]">
                {{ p.first_name[0] }}{{ p.last_name[0] }}
              </span>
            </div>
            <div class="min-w-0 max-w-5xl flex-1 ">
              <p class="font-semibold text-[#f1f5f9]">{{ p.first_name }} {{ p.last_name }}</p>
              <p class="text-[12px] text-[#64748b]">{{ p.nationality?.name }}</p>
            </div>
            <span class="rounded-full bg-[#1e293b] px-3 py-1 text-[12px] font-semibold text-[#00d4aa]">
              {{ p.position?.name ?? '—' }}
            </span>
          </RouterLink>
        </div>
      </div>

      <!-- ── STANDINGS ── -->
      <div v-else-if="activeTab === 'Standings'" class="rounded-xl border border-[#1e293b] bg-[#111827]">
        <div v-if="standingsLoading" class="p-5 space-y-2">
          <div v-for="i in 10" :key="i" class="h-10 animate-pulse rounded bg-[#1e293b]" />
        </div>
        <div v-else-if="!standings.length" class="py-12 text-center text-[#64748b]">No standings data.</div>
        <div v-else class="overflow-x-auto">
          <table class="w-full text-[14px]">
            <thead>
              <tr class="border-b border-[#1e293b] text-left">
                <th class="px-4 py-3 font-semibold text-white">#</th>
                <th class="px-4 py-3 font-semibold text-white">Team</th>
                <th class="px-4 py-3 text-center font-semibold text-white">W</th>
                <th class="px-4 py-3 text-center font-semibold text-white">L</th>
                <th class="px-4 py-3 text-center font-semibold text-white">WIN RATE</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(row, idx) in standings" :key="row.id"
                class="border-b border-[#1e293b]/50 last:border-0 transition"
                :class="row.team.id === Number(teamId)
                  ? 'bg-[#00d4aa]/10'
                  : 'hover:bg-[#1e293b]/30'">
                <td class="px-4 py-3 font-semibold"
                  :class="row.team.id === Number(teamId) ? 'text-[#00d4aa]' : 'text-[#64748b]'">
                  {{ idx + 1 }}
                </td>
                <td class="px-4 py-3">
                  <RouterLink :to="`/team/${row.team.id}`"
                    class="flex items-center gap-2.5 transition hover:text-[#00d4aa]">
                    <img v-if="row.team.logo" :src="row.team.logo" class="h-6 w-6 object-contain"
                      @error="(e) => e.target.style.display='none'" />
                    <span class="font-semibold"
                      :class="row.team.id === Number(teamId) ? 'text-[#00d4aa]' : 'text-[#f1f5f9]'">
                      {{ row.team.name }}
                    </span>
                  </RouterLink>
                </td>
                <td class="px-4 py-3 text-center font-semibold text-white">{{ row.win }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.loss }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.pct }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <div v-else class="py-20 text-center text-[#64748b]">
      <p class="text-lg font-semibold text-[#94a3b8]">Team not found</p>
    </div>
  </div>

  <LoginModal v-model="showLogin" />
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ChevronLeft, MapPin, Heart } from 'lucide-vue-next'
import api, { fetchAll } from '@/api'
import { useScoresStore } from '@/stores/scores'
import { useAuth } from '@/composables/useAuth'
import { useFavourites } from '@/composables/useFavourites'
import LoginModal from '@/components/LoginModal.vue'

const route = useRoute()
const router = useRouter()
const store = useScoresStore()

const { isLoggedIn } = useAuth()
const { isFavourite, toggle, loadFavourites } = useFavourites()
const showLogin = ref(false)

const teamId = route.params.id
const team = ref(null)
const loading = ref(true)
const players = ref([])
const playersLoading = ref(false)
const standings = ref([])
const standingsLoading = ref(false)
const activeTab = ref('Matches')
const tabs = ['Matches', 'Players', 'Standings']

// Hall from first home match
const teamHall = computed(() => {
  const m = store.matches.find(m => m.homeTeamId === Number(teamId) && m.hall)
  return m?.hall ?? null
})

// Matches for this team
const teamMatches = computed(() => {
  const id = Number(teamId)
  return store.matches
    .filter(m => m.homeTeamId === id || m.awayTeamId === id)
    .map(m => {
      const isHome = m.homeTeamId === id
      const myScore  = isHome ? m.homeScore : m.awayScore
      const oppScore = isHome ? m.awayScore : m.homeScore
      const result = m.status === 'finished' && myScore != null
        ? (myScore > oppScore ? 'W' : 'L')
        : null
      return {
        id: m.id,
        matchDate: m.matchDate,
        opponent: isHome ? m.awayTeam : m.homeTeam,
        opponentLogo: isHome ? m.awayTeamLogo : m.homeTeamLogo,
        homeAway: isHome ? 'Home' : 'Away',
        score: myScore != null && oppScore != null ? `${myScore} – ${oppScore}` : '—',
        result,
        status: m.status,
        time: m.time,
      }
    })
    .sort((a, b) => new Date(b.matchDate) - new Date(a.matchDate))
})

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function loadPlayers() {
  playersLoading.value = true
  try {
    players.value = await fetchAll('players/', { team: teamId })
  } catch {
    players.value = []
  } finally {
    playersLoading.value = false
  }
}

async function loadStandings() {
  standingsLoading.value = true
  try {
    // Find league from team's matches
    const id = Number(teamId)
    const match = store.matches.find(m => m.homeTeamId === id || m.awayTeamId === id)
    if (!match) { standingsLoading.value = false; return }

    // Get most recent season
    const seasonsRes = await api.get('seasons/')
    const seasons = seasonsRes.data.results ?? []
    const season = seasons[seasons.length - 1]
    if (!season) { standingsLoading.value = false; return }

    const raw = await fetchAll('league-teams/', { league: match.leagueId, season: season.id })
    standings.value = raw
      .map(lt => ({
        id: lt.id,
        team: lt.team,
        win: lt.win,
        loss: lt.loss,
        pct: ((lt.win / ((lt.win + lt.loss) || 1)) * 100).toFixed(1) + '%',
      }))
      .sort((a, b) => b.win / ((b.win + b.loss) || 1) - a.win / ((a.win + a.loss) || 1))
  } catch {
    standings.value = []
  } finally {
    standingsLoading.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get(`teams/${teamId}/`)
    team.value = data
  } catch {
    team.value = null
  } finally {
    loading.value = false
  }

  if (!store.matches.length) await store.fetchMatches()
  await Promise.all([loadPlayers(), loadStandings(), loadFavourites()])
})
</script>
