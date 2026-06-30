<template>
  <div class="mx-auto max-w-[1280px] px-4 py-6 md:px-8">
    <RouterLink to="/"
      class="mb-6 inline-flex items-center gap-2 text-sm text-[#64748b] transition hover:text-[#94a3b8]">
      <ChevronLeft class="h-4 w-4" /> Back to scores
    </RouterLink>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div class="h-48 animate-pulse rounded-2xl bg-[#1e293b]" />
      <div class="h-64 animate-pulse rounded-xl bg-[#1e293b]" />
    </div>

    <template v-else-if="player">
      <!-- Player card -->
      <div class="mb-4 rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6">
        <div class="flex flex-col items-center gap-5 sm:flex-row sm:items-start">
          <!-- Avatar -->
          <div class="flex h-28 w-28 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#1e293b]">
            <img v-if="player.image_url" :src="player.image_url" :alt="fullName"
              class="h-full w-full object-cover" @error="(e) => e.target.style.display='none'" />
            <span v-else class="text-4xl font-bold text-[#64748b]">{{ initials }}</span>
          </div>

          <!-- Info -->
          <div class="flex-1 text-center sm:text-left">
            <h1 class="text-2xl font-extrabold text-white">{{ fullName }}</h1>
            <div class="mt-1 flex flex-wrap items-center justify-center gap-2 sm:justify-start">
              <span class="rounded-full bg-[#1e293b] px-3 py-1 text-[13px] font-semibold text-[#00d4aa]">
                {{ player.position?.name ?? '—' }}
              </span>
              <span v-if="player.team" class="flex items-center gap-1.5 text-[14px] text-[#94a3b8]">
                <img v-if="player.team.logo" :src="player.team.logo" class="h-5 w-5 object-contain"
                  @error="(e) => e.target.style.display='none'" />
                {{ player.team.name }}
              </span>
            </div>

            <!-- Characteristics grid -->
            <div class="mt-5 grid grid-cols-2 gap-3 sm:grid-cols-5">
              <div v-for="stat in characteristics" :key="stat.label"
                class="flex flex-col items-center rounded-xl bg-[#1e293b] px-3 py-3">
                <span class="text-[11px] font-semibold uppercase tracking-wider text-[#64748b]">{{ stat.label }}</span>
                <span class="mt-1 text-[17px] font-bold text-white">{{ stat.value }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats by match -->
      <div class="rounded-xl border border-[#1e293b] bg-[#111827]">
        <div class="border-b border-[#1e293b] px-5 py-4">
          <h2 class="text-[15px] font-bold text-white">Stats by Match</h2>
        </div>

        <div v-if="statsLoading" class="p-5 space-y-2">
          <div v-for="i in 6" :key="i" class="h-10 animate-pulse rounded bg-[#1e293b]" />
        </div>

        <div v-else-if="!statRows.length" class="px-5 py-12 text-center text-[#64748b]">
          No match stats available for this player.
        </div>

        <div v-else class="overflow-x-auto">
          <table class="w-full text-[14px]">
            <thead>
              <tr class="border-b border-[#1e293b] text-left">
                <th class="px-5 py-3 font-semibold text-white">Date</th>
                <th class="px-4 py-3 font-semibold text-white">Opponent</th>
                <th class="px-4 py-3 text-center font-semibold text-white">Result</th>
                <th class="px-4 py-3 text-center font-semibold text-white">MIN</th>
                <th class="px-4 py-3 text-center font-semibold text-white">PTS</th>
                <th class="px-4 py-3 text-center font-semibold text-white">REB</th>
                <th class="px-4 py-3 text-center font-semibold text-white">AST</th>
                <th class="px-4 py-3 text-center font-semibold text-white">STL</th>
                <th class="px-4 py-3 text-center font-semibold text-white">BLK</th>
                <th class="px-4 py-3 text-center font-semibold text-white">PF</th>
                <th class="px-4 py-3 text-center font-semibold text-white">TO</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in statRows" :key="row.id"
                class="border-b border-[#1e293b]/50 transition hover:bg-[#1e293b]/40 last:border-0">
                <td class="px-5 py-3 text-[#94a3b8]">{{ row.date }}</td>
                <td class="px-4 py-3">
                  <RouterLink :to="`/match/${row.matchId}`"
                    class="flex items-center gap-2 text-[#f1f5f9] hover:text-[#00d4aa] transition-colors">
                    <img v-if="row.opponentLogo" :src="row.opponentLogo" class="h-5 w-5 object-contain"
                      @error="(e) => e.target.style.display='none'" />
                    <span class="font-semibold">{{ row.opponent }}</span>
                  </RouterLink>
                </td>
                <td class="px-4 py-3 text-center">
                  <span class="rounded bg-[#1e293b] px-2 py-0.5 text-[13px] font-bold tabular-nums text-white">
                    {{ row.result }}
                  </span>
                </td>
                <td class="px-4 py-3 text-center text-[#94a3b8]">{{ row.min ?? '—' }}</td>
                <td class="px-4 py-3 text-center text-[17px] font-bold text-white">{{ row.pts ?? '—' }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.reb ?? '—' }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.ast ?? '—' }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.stl ?? '—' }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.blk ?? '—' }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.pf ?? '—' }}</td>
                <td class="px-4 py-3 text-center text-white">{{ row.tov ?? '—' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <div v-else class="py-20 text-center text-[#64748b]">
      <p class="text-lg font-semibold text-[#94a3b8]">Player not found</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronLeft } from 'lucide-vue-next'
import api, { fetchAll } from '@/api'
import { useScoresStore } from '@/stores/scores'

const route = useRoute()
const store = useScoresStore()

const player = ref(null)
const loading = ref(true)
const rawStats = ref([])
const statsLoading = ref(false)

const fullName = computed(() =>
  player.value ? `${player.value.first_name} ${player.value.last_name}` : ''
)

const initials = computed(() => {
  if (!player.value) return ''
  return `${player.value.first_name[0]}${player.value.last_name[0]}`
})

const characteristics = computed(() => {
  const p = player.value
  if (!p) return []
  const age = p.date_of_birth
    ? Math.floor((Date.now() - new Date(p.date_of_birth)) / (365.25 * 24 * 3600 * 1000))
    : null
  return [
    { label: 'Height',   value: p.height_cm   ? `${p.height_cm} cm`   : '—' },
    { label: 'Weight',   value: p.weight_kg   ? `${p.weight_kg} kg`   : '—' },
    { label: 'Wingspan', value: p.wingspan_cm ? `${p.wingspan_cm} cm` : '—' },
    { label: 'Age',      value: age ?? '—' },
    { label: 'Nation',   value: p.nationality?.name ?? '—' },
  ]
})

const statRows = computed(() => {
  if (!player.value) return []
  const teamId = player.value.team?.id

  return rawStats.value.map(s => {
    const match = store.matches.find(m => m.id === s.match)
    if (!match) return null

    const isHome = match.homeTeamId === teamId
    const opponent     = isHome ? match.awayTeam     : match.homeTeam
    const opponentLogo = isHome ? match.awayTeamLogo : match.homeTeamLogo
    const myScore  = isHome ? match.homeScore : match.awayScore
    const oppScore = isHome ? match.awayScore : match.homeScore
    const result = (myScore != null && oppScore != null)
      ? `${myScore} – ${oppScore}`
      : '—'

    return {
      id: s.id,
      matchId: match.id,
      date: new Date(match.matchDate).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
      opponent,
      opponentLogo,
      result,
      min: s.minutes_played,
      pts: s.points,
      reb: s.rebounds,
      ast: s.assists,
      stl: s.steals,
      blk: s.blocks,
      pf:  s.fouls,
      tov: s.turnovers,
    }
  }).filter(Boolean).sort((a, b) => new Date(b.date) - new Date(a.date))
})

onMounted(async () => {
  const id = route.params.id
  try {
    const { data } = await api.get(`players/${id}/`)
    player.value = data
  } catch {
    player.value = null
  } finally {
    loading.value = false
  }

  statsLoading.value = true
  try {
    if (!store.matches.length) await store.fetchMatches()
    rawStats.value = await fetchAll('player-stats/', { player: id })
  } catch {
    rawStats.value = []
  } finally {
    statsLoading.value = false
  }
})
</script>
