<template>
  <div class="mx-auto max-w-7xl px-4 py-8 sm:px-6 md:px-8">
    <h1 class="mb-6 text-xl font-extrabold text-[#f1f5f9]">Standings</h1>

    <!-- Controls row -->
    <div class="mb-6 flex flex-col gap-4">
      <!-- League selector -->
      <div class="flex flex-wrap gap-2">
        <button
          v-for="league in store.leagues" :key="league.id"
          @click="activeLeagueId = league.id"
          class="flex cursor-pointer items-center gap-2 rounded-lg px-3 py-2 text-sm font-semibold transition"
          :class="activeLeagueId === league.id
            ? 'border border-[#00d4aa]/30 bg-[#00d4aa]/10 text-[#00d4aa]'
            : 'bg-[#1e293b] text-[#64748b] hover:text-[#94a3b8]'">
          <img v-if="league.logo" :src="league.logo" :alt="league.name" class="h-5 w-5 object-contain"
            @error="(e) => e.target.style.display='none'" />
          <span>{{ league.name }}</span>
        </button>
      </div>

      <!-- Season selector -->
      <div class="relative" ref="seasonDropdownRef">
        <button
          @click="seasonOpen = !seasonOpen"
          class="flex cursor-pointer items-center gap-2 rounded-lg border border-[#1e293b] bg-[#1e293b] px-3 py-2 text-sm font-semibold text-[#f1f5f9] transition hover:bg-[#263348]">
          {{ activeSeason?.name ?? 'Season' }}
          <ChevronDown class="h-4 w-4 text-[#64748b] transition-transform duration-200" :class="seasonOpen ? 'rotate-180' : ''" />
        </button>
        <Transition name="dropdown">
          <div v-if="seasonOpen"
            class="absolute right-0 top-[calc(100%+6px)] z-50 min-w-[140px] overflow-hidden rounded-lg border border-[#334155] bg-[#0f172a] shadow-xl">
            <button
              v-for="s in seasons" :key="s.id"
              @click="activeSeasonId = s.id; seasonOpen = false"
              class="flex w-full cursor-pointer items-center px-4 py-2.5 text-sm font-semibold transition hover:bg-[#1e293b]"
              :class="activeSeasonId === s.id ? 'text-[#00d4aa]' : 'text-[#94a3b8]'">
              {{ s.name }}
            </button>
          </div>
        </Transition>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-2">
      <div v-for="i in 8" :key="i" class="h-10 animate-pulse rounded-lg bg-[#1e293b]" />
    </div>

    <StandingsTable v-else-if="rows.length" :rows="rows" :leagueName="activeName" :leagueLogo="activeLogo" />

    <div v-else class="py-16 text-center text-[#64748b]">No standings data...</div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { ChevronDown } from 'lucide-vue-next'
import { useScoresStore } from '@/stores/scores'
import StandingsTable from '@/components/StandingsTable.vue'
import { fetchAll } from '@/api'
import api from '@/api'


const store = useScoresStore()
const route = useRoute()

const activeLeagueId = ref(null)
const activeSeasonId = ref(null)
const rawStandings = ref([])
const seasons = ref([])
const loading = ref(false)
const seasonOpen = ref(false)
const seasonDropdownRef = ref(null)

const activeSeason = computed(() => seasons.value.find(s => s.id === activeSeasonId.value) ?? null)

const handleClickOutside = (e) => {
  if (seasonDropdownRef.value && !seasonDropdownRef.value.contains(e.target)) seasonOpen.value = false
}

async function loadSeasons() {
  const res = await api.get('seasons/')
  seasons.value = res.data.results ?? []
  if (seasons.value.length && !activeSeasonId.value) {
    activeSeasonId.value = seasons.value[seasons.value.length - 1].id
  }
}

watch(() => store.leagues, (leagues) => {
  if (!activeLeagueId.value && leagues.length) {
    const fromQuery = route.query.league ? Number(route.query.league) : null
    activeLeagueId.value = fromQuery ?? leagues[0].id
  }
}, { immediate: true })

watch([activeLeagueId, activeSeasonId], ([leagueId, seasonId]) => {
  if (leagueId && seasonId) loadStandings(leagueId, seasonId)
})

async function loadStandings(leagueId, seasonId) {
  loading.value = true
  try {
    rawStandings.value = await fetchAll('league-teams/', { league: leagueId, season: seasonId })
  } catch (e) {
    console.error('loadStandings:', e)
  } finally {
    loading.value = false
  }
}

const activeName = computed(() =>
  store.leagues.find(l => l.id === activeLeagueId.value)?.name ?? ''
)
const activeLogo = computed(() =>
  store.leagues.find(l => l.id === activeLeagueId.value)?.logo ?? null
)

const rows = computed(() =>
  [...rawStandings.value]
    .sort((a, b) => {
      const pctA = a.win / (a.win + a.loss || 1)
      const pctB = b.win / (b.win + b.loss || 1)
      return pctB - pctA
    })
    .map((s, i) => ({
      pos: i + 1,
      id: s.team.id,
      name: s.team.name,
      logo: s.team.logo,
      p: s.win + s.loss,
      w: s.win,
      l: s.loss,
      pct: ((s.win / (s.win + s.loss || 1)) * 100).toFixed(1) + '%',
    }))
)

onMounted(async () => {
  if (!store.leagues.length) store.fetchLeagues()
  await loadSeasons()
  document.addEventListener('mousedown', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<style scoped>
.dropdown-enter-active, .dropdown-leave-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.dropdown-enter-from, .dropdown-leave-to { opacity: 0; transform: translateY(-6px); }
</style>
