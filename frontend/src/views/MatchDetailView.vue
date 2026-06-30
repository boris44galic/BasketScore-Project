<template>
  <div class="mx-auto max-w-[1280px] px-4 py-6 md:px-8">
    <RouterLink to="/"
      class="mb-6 inline-flex items-center gap-2 text-sm text-[#64748b] transition hover:text-[#94a3b8]">
      <ChevronLeft class="h-4 w-4" /> Back to scores
    </RouterLink>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div class="h-48 animate-pulse rounded-2xl bg-[#1e293b]" />
      <div class="h-10 animate-pulse rounded-xl bg-[#1e293b]" />
      <div class="h-64 animate-pulse rounded-xl bg-[#1e293b]" />
    </div>

    <template v-else-if="match">
      <!-- Score card -->
      <div class="mb-4 rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6">
        <div class="mb-5 flex items-center justify-center gap-2">
          <img v-if="match.leagueLogo" :src="match.leagueLogo" alt="" class="h-7 w-7 object-contain"
            @error="(e) => e.target.style.display='none'" />
          <span class="text-sm font-semibold uppercase tracking-wider text-[#94a3b8]">
            {{ match.leagueCountry }} · {{ match.league }}
          </span>
        </div>

        <div class="flex items-center justify-between gap-4">
          <!-- Home -->
          <div class="flex flex-1 flex-col items-center gap-2">
            <div class="flex items-center gap-30 pr-37" >
              <button @click="isLoggedIn ? toggle(match.homeTeamId) : (showLogin = true)"
                class="cursor-pointer rounded-full p-1.5 transition hover:bg-[#1e293b]"
                :class="isFavourite(match.homeTeamId) ? 'text-red-500' : 'text-[#475569] hover:text-red-400'">
                <Heart class="h-6 w-6" :class="isFavourite(match.homeTeamId) ? 'fill-red-500' : ''" />
              </button>
              <RouterLink :to="`/team/${match.homeTeamId}`"
                class="flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-[#1e293b] transition hover:ring-2 hover:ring-[#00d4aa]">
                <img v-if="match.homeTeamLogo" :src="match.homeTeamLogo" :alt="match.homeTeam"
                  class="h-12 w-12 object-contain" @error="(e) => e.target.style.display='none'" />
                <span v-else class="text-2xl">🏀</span>
              </RouterLink>
            </div>
            <span class="text-center text-sm font-bold text-[#f1f5f9]">{{ match.homeTeam }}</span>
          </div>

          <!-- Score -->
          <div class="flex shrink-0 flex-col items-center">
            <div class="flex items-center gap-4">
              <span class="text-5xl font-black tabular-nums" :class="scoreTextClass">
                {{ match.homeScore ?? '-' }}
              </span>
              <span class="text-2xl font-black text-white">:</span>
              <span class="text-5xl font-black tabular-nums" :class="scoreTextClass">
                {{ match.awayScore ?? '-' }}
              </span>
            </div>
            <div class="mt-4 flex items-center gap-2 rounded-full px-4 py-1.5" :class="statusBadgeClass">
              <span v-if="match.status === 'live'" class="h-2 w-2 animate-pulse rounded-full bg-[#ef4444]" />
              <span class="text-sm font-bold text-white">{{ statusLabel }}</span>
            </div>
            <p v-if="match.hall" class="mt-2 flex items-center gap-1.5 pt-3 text-s font-medium text-[#94a3b8]">
              <MapPin class="h-3.5 w-3.5 shrink-0" />
              {{ match.hall }}
            </p>          
          </div>

          <!-- Away -->
          <div class="flex flex-1 flex-col items-center gap-2">
            <div class="flex items-center gap-30 pl-37">
              <RouterLink :to="`/team/${match.awayTeamId}`"
                class="flex h-16 w-16 items-center justify-center overflow-hidden rounded-full bg-[#1e293b] transition hover:ring-2 hover:ring-[#00d4aa]">
                <img v-if="match.awayTeamLogo" :src="match.awayTeamLogo" :alt="match.awayTeam"
                  class="h-12 w-12 object-contain" @error="(e) => e.target.style.display='none'" />
                <span v-else class="text-2xl">🏀</span>
              </RouterLink>
              <button @click="isLoggedIn ? toggle(match.awayTeamId) : (showLogin = true)"
                class="cursor-pointer rounded-full p-1.5 transition hover:bg-[#1e293b]"
                :class="isFavourite(match.awayTeamId) ? 'text-red-500' : 'text-[#475569] hover:text-red-400'">
                <Heart class="h-6 w-6" :class="isFavourite(match.awayTeamId) ? 'fill-red-500' : ''" />
              </button>
            </div>
            <span class="text-center text-sm font-bold text-[#f1f5f9]">{{ match.awayTeam }}</span>
          </div>
        </div>
      </div>

      <!-- Tabs -->
      <div class="mb-4 flex gap-1 rounded-xl bg-[#1e293b] p-1">
        <button v-for="tab in tabs" :key="tab" @click="activeTab = tab"
          class="flex-1 rounded-lg py-2 text-sm font-semibold transition"
          :class="activeTab === tab ? 'bg-[#0f172a] text-[#f1f5f9] shadow' : 'text-[#64748b] hover:text-[#94a3b8]'">
          {{ tab }}
        </button>
      </div>

      <!-- Stats tab -->
      <div v-if="activeTab === 'Stats'"
        class="rounded-xl border border-[#1e293b] bg-[#111827] p-5">
        <!-- Guest gate -->
        <div v-if="!isLoggedIn" class="flex flex-col items-center justify-center py-14 gap-4">
          <Lock class="h-10 w-10 text-[#334155]" />
          <p class="text-[15px] font-semibold text-[#94a3b8]">You need to be logged in to see stats</p>
          <button @click="showLogin = true"
            class="cursor-pointer rounded-full bg-[#00d4aa] px-6 py-2.5 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0]">
            Sign In
          </button>
        </div>
        <template v-else>
          <div v-if="statsLoading" class="space-y-3">
            <div v-for="i in 6" :key="i" class="h-8 animate-pulse rounded bg-[#1e293b]" />
          </div>
          <template v-else-if="matchStats.length">
            <div class="mb-4 flex items-center justify-between">
              <span class="text-sm font-bold text-[#f1f5f9] ml-3 mt-3">{{ match.homeTeam }}</span>
              <span class="text-xs font-semibold uppercase tracking-wider">Match Stats</span>
              <span class="text-sm font-bold text-[#f1f5f9] mr-3 mt-3">{{ match.awayTeam }}</span>
            </div>
            <StatBar v-for="s in matchStats" :key="s.label" v-bind="s" />
          </template>
          <p v-else class="text-center text-sm text-white">No stats available</p>
        </template>
      </div>

      <!-- Lineups tab -->
      <div v-else-if="activeTab === 'Lineups'"
        class="rounded-xl border border-[#1e293b] bg-[#111827]">
        <!-- Guest gate -->
        <div v-if="!isLoggedIn" class="flex flex-col items-center justify-center py-14 gap-4">
          <Lock class="h-10 w-10 text-[#334155]" />
          <p class="text-[15px] font-semibold text-[#94a3b8]">You need to be logged in to see lineups</p>
          <button @click="showLogin = true"
            class="cursor-pointer rounded-full bg-[#00d4aa] px-6 py-2.5 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0]">
            Sign In
          </button>
        </div>
        <template v-else>
        <div v-if="lineupsLoading" class="p-5 space-y-2">
          <div v-for="i in 8" :key="i" class="h-10 animate-pulse rounded bg-[#1e293b]" />
        </div>
        <template v-else>
          <!-- Filter bar -->
          <div class="flex items-center justify-center gap-2 border-b border-[#1e293b] p-3">
            <button v-for="f in lineupFilters" :key="f.key" @click="lineupFilter = f.key"
              class="cursor-pointer rounded-lg px-3 py-1.5 text-[14px] font-semibold transition"
              :class="lineupFilter === f.key
                ? 'bg-[#0f172a] text-[#f1f5f9]'
                : 'text-[#64748b] hover:text-[#94a3b8]'">
              {{ f.label }}
            </button>
          </div>

          <!-- Table -->
          <div class="overflow-x-auto">
            <table class="w-full text-[15px]">
              <thead>
                <tr class="border-b border-[#1e293b] text-left">
                  <th class="px-5 py-3 text-[15px] font-semibold pl-9">Player</th>
                  <th class="px-4 py-3 text-center text-[13px]  ">MIN</th>
                  <th class="px-4 py-3 text-center text-[13px]  ">PTS</th>
                  <th class="px-4 py-3 text-center text-[13px] ">REB</th>
                  <th class="px-4 py-3 text-center text-[13px]  ">AST</th>
                  <th class="px-4 py-3 text-center text-[13px]  ">STL</th>
                  <th class="px-4 py-3 text-center text-[13px]  ">BLK</th>
                  <th class="px-4 py-3 text-center text-[13px]  ">PF</th>
                  <th class="px-4 py-3 text-center text-[13px] ">TO</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="!lineupRows.length">
                  <td colspan="9" class="px-5 py-10 text-center text-[#475569]">No lineup data...</td>
                </tr>
                <tr v-for="p in lineupRows" :key="p.id"
                  class="border-b border-[#1e293b]/50 transition hover:bg-[#1e293b]/40 last:border-0">
                  <td class="px-5 py-3">
                    <div class="flex items-center gap-3">
                      <span class="h-2.5 w-2.5 shrink-0 rounded-full"
                        :class="p.teamName === match.homeTeam ? 'bg-[#00d4aa]' : 'bg-[#f59e0b]'" />
                      <div class="flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#1e293b]">
                        <img v-if="p.image_url" :src="p.image_url" :alt="p.name"
                          class="h-full w-full object-cover" @error="(e) => e.target.style.display='none'" />
                        <span v-else class="text-[11px] font-bold text-[#64748b]">{{ p.initials }}</span>
                      </div>
                      <div class="min-w-0">
                        <RouterLink :to="`/player/${p.id}`"
                          class="truncate text-[15px] font-semibold text-[#f1f5f9] hover:text-[#00d4aa] transition-colors">
                          {{ p.name }}
                        </RouterLink>
                        <p class="text-[12px] text-[#6f7d91]">{{ p.pos }}
                          <span v-if="p.starter" class="ml-1 font-bold text-[#00d4aa]">S</span>
                        </p>
                      </div>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-center ">{{ p.min ?? '—' }}</td>
                  <td class="px-4 py-3 text-center text-[17px] font-bold text-[#f1f5f9]">{{ p.pts ?? '—' }}</td>
                  <td class="px-4 py-3 text-center  ">{{ p.reb ?? '—' }}</td>
                  <td class="px-4 py-3 text-center  ">{{ p.ast ?? '—' }}</td>
                  <td class="px-4 py-3 text-center  ">{{ p.stl ?? '—' }}</td>
                  <td class="px-4 py-3 text-center  ">{{ p.blk ?? '—' }}</td>
                  <td class="px-4 py-3 text-center  ">{{ p.pf ?? '—' }}</td>
                  <td class="px-4 py-3 text-center  ">{{ p.tov ?? '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Legend -->
          <div class="flex items-center gap-4 border-t border-[#1e293b] px-4 py-2.5">
            <div class="flex items-center gap-1.5 text-[11px] text-[#475569]">
              <span class="h-2 w-2 rounded-full bg-[#00d4aa]" /> {{ match.homeTeam }}
            </div>
            <div class="flex items-center gap-1.5 text-[11px] text-[#475569]">
              <span class="h-2 w-2 rounded-full bg-[#f59e0b]" /> {{ match.awayTeam }}
            </div>
            <span class="text-[11px] text-[#475569]">· <span class="font-bold text-[#00d4aa]">S</span> = Starter</span>
          </div>
        </template>
      </template>
      </div>

      <!-- H2H tab -->
      <div v-else-if="activeTab === 'H2H'"
        class="rounded-xl border border-[#1e293b] bg-[#111827] p-5">
        <div v-if="h2hLoading" class="space-y-2">
          <div v-for="i in 5" :key="i" class="h-10 animate-pulse rounded bg-[#1e293b]" />
        </div>
        <template v-else-if="h2hMatches.length">
          <h3 class="mb-4 text-sm font-bold text-[#f1f5f9] text-center">Head to Head</h3>
          <div v-for="g in h2hMatches" :key="g.id"
            class="flex items-center gap-3 border-t border-[#1e293b]/60 py-2 first:border-0 pt-5">

            <span class="flex-1 truncate text-right text-[16px]">{{ g.home }}</span>
            <span class="shrink-0 rounded bg-[#1e293b] px-2 py-0.5 text-[14px] font-bold tabular-nums text-[#f1f5f9]">
              {{ g.score }}
            </span>
            <span class="flex-1 truncate text-[16px]">{{ g.away }}</span>           
           </div>
        </template>
        <p v-else class="text-center text-sm text-[#64748b]">No previous meetings found</p>
      </div>
    </template>

    <div v-else class="py-20 text-center text-[#64748b]">
      <p class="text-lg font-semibold text-[#94a3b8]">Match not found</p>
    </div>
  </div>

  <LoginModal v-model="showLogin" />
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronLeft, Heart, MapPin, Lock } from 'lucide-vue-next'
import { useScoresStore } from '@/stores/scores'
import StatBar from '@/components/StatBar.vue'
import LoginModal from '@/components/LoginModal.vue'
import { fetchAll } from '@/api'
import { useAuth } from '@/composables/useAuth'
import { useFavourites } from '@/composables/useFavourites'

const route = useRoute()
const store = useScoresStore()
const { isLoggedIn } = useAuth()
const showLogin = ref(false)
const { isFavourite, toggle, loadFavourites } = useFavourites()

const loading = ref(false)
const statsLoading = ref(false)
const lineupsLoading = ref(false)
const h2hLoading = ref(false)
const activeTab = ref('Stats')
const tabs = ['Stats', 'Lineups', 'H2H']

// Match from store (already fetched on app init)
const match = computed(() => {
  const m = store.getMatchById(route.params.id)
  return m ?? null
})

// ── Computed display  
const scoreTextClass = computed(() =>
  match.value?.status === 'live' ? 'text-[#ef4444]' : 'text-[#f1f5f9]'
)

const statusLabel = computed(() => {
  const m = match.value
  if (!m) return ''
  if (m.status === 'live') return m.quarter ? `${m.quarter} ${m.clock}` : 'LIVE'
  if (m.status === 'finished') return 'Final'
  if (m.status === 'scheduled') return m.time
  return m.status
})

const statusBadgeClass = computed(() => {
  const s = match.value?.status
  if (s === 'live') return 'bg-[#ef4444]/10 border border-[#ef4444]/30 text-[#ef4444]'
  if (s === 'finished') return 'bg-[#1e293b] border border-[#2d3748] text-[#64748b]'
  return 'bg-[#1e293b] border border-[#2d3748] text-[#94a3b8]'
})

// ── Stats  
const rawStats = ref([])

const matchStats = computed(() => {
  if (!rawStats.value.length || !match.value) return []

  const home = rawStats.value.filter(s => s.player.team?.name === match.value.homeTeam)
  const away = rawStats.value.filter(s => s.player.team?.name === match.value.awayTeam)

  const sum = (arr, key) => arr.reduce((t, s) => t + (s[key] ?? 0), 0)

  return [
    { label: 'Points',    home: sum(home, 'points'),    away: sum(away, 'points') },
    { label: 'Rebounds',  home: sum(home, 'rebounds'),  away: sum(away, 'rebounds') },
    { label: 'Assists',   home: sum(home, 'assists'),   away: sum(away, 'assists') },
    { label: 'Steals',    home: sum(home, 'steals'),    away: sum(away, 'steals') },
    { label: 'Blocks',    home: sum(home, 'blocks'),    away: sum(away, 'blocks') },
    { label: 'Turnovers', home: sum(home, 'turnovers'), away: sum(away, 'turnovers') },
    { label: 'Fouls',     home: sum(home, 'fouls'),     away: sum(away, 'fouls') },
  ]
})

async function loadStats(matchId) {
  statsLoading.value = true
  try {
    rawStats.value = await fetchAll('player-stats/', { match: matchId })
  } catch (e) {
    console.error('loadStats:', e)
  } finally {
    statsLoading.value = false }
}

// ── Lineups  
const rawLineups = ref([])
const lineupFilter = ref('all')
const lineupFilters = computed(() => [
  { key: 'home', label: match.value?.homeTeam ?? 'Home' },
  { key: 'all',  label: 'All' },
  { key: 'away', label: match.value?.awayTeam ?? 'Away' },
])

function buildPlayerWithStats(entry) {
  const p = entry.player
  const stats = rawStats.value.find(s => s.player?.id === p.id)
  return {
    id: p.id,
    name: `${p.first_name} ${p.last_name}`,
    initials: `${p.first_name[0]}${p.last_name[0]}`,
    pos: p.position?.name ?? '',
    image_url: p.image_url ?? null,
    teamName: p.team?.name ?? '',
    starter: entry.starter,
    min: stats?.minutes_played ?? null,
    pts: stats?.points ?? null,
    reb: stats?.rebounds ?? null,
    ast: stats?.assists ?? null,
    stl: stats?.steals ?? null,
    blk: stats?.blocks ?? null,
    pf:  stats?.fouls ?? null,
    tov: stats?.turnovers ?? null,
  }
}

const lineupRows = computed(() => {
  const homeTeam = match.value?.homeTeam
  const awayTeam = match.value?.awayTeam
  let entries = rawLineups.value
  if (lineupFilter.value === 'home') entries = entries.filter(e => e.player.team?.name === homeTeam)
  else if (lineupFilter.value === 'away') entries = entries.filter(e => e.player.team?.name === awayTeam)
  return entries
    .map(buildPlayerWithStats)
    .sort((a, b) => (b.pts ?? -1) - (a.pts ?? -1))
})

async function loadLineups(matchId) {
  lineupsLoading.value = true
  try {
    rawLineups.value = await fetchAll('player-match-status/', { match: matchId })
  } catch (e) {
    console.error('loadLineups:', e)
  } finally {
    lineupsLoading.value = false }
}

// ── H2H 
const h2hMatches = ref([])

async function loadH2H() {
  if (!match.value) return
  h2hLoading.value = true
  try {
    // Find past meetings between the same two teams in the store
    const homeTeamName = match.value.homeTeam
    const awayTeamName = match.value.awayTeam
    const past = store.matches.filter(m =>
      m.id !== match.value.id &&
      m.status === 'finished' &&
      ((m.homeTeam === homeTeamName && m.awayTeam === awayTeamName) ||
       (m.homeTeam === awayTeamName && m.awayTeam === homeTeamName))
    ).slice(0, 5)

    h2hMatches.value = past.map(m => ({
      id: m.id,
      date: new Date(m.matchDate).toLocaleDateString('en-GB', { month: 'short', year: 'numeric' }),
      home: m.homeTeam,
      away: m.awayTeam,
      score: `${m.homeScore} – ${m.awayScore}`,
    }))
  } finally {
    h2hLoading.value = false
  }
}

// ── Watchers  
watch(activeTab, (tab) => {
  if (!match.value) return
  if (tab === 'Stats' && !rawStats.value.length) loadStats(match.value.id)
  if (tab === 'Lineups' && !rawLineups.value.length) loadLineups(match.value.id)
  if (tab === 'H2H' && !h2hMatches.value.length) loadH2H()
})

watch(match, (m) => {
  if (m) {
    loadStats(m.id)
  }
}, { immediate: true })

onMounted(() => {
  if (!store.matches.length) store.fetchMatches()
  loadFavourites()
})
</script>
