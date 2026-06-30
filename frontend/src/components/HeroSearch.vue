<template>
  <main class="mx-auto flex w-full max-w-7xl flex-col items-center px-4 pb-2 pt-8 sm:pt-10 md:px-8">

    <Transition name="title-fade" mode="out-in">
      <h1 :key="activeTab"
        class="mb-6 text-center text-[38px] font-extrabold leading-none sm:mb-8 sm:text-[52px]"
        :class="activeTab === 'Live' ? 'text-[#ef4444]' : 'text-[#f1f5f9]'">
        {{ titleByTab }}
      </h1>
    </Transition>

    <!-- Filter tabs -->
    <div class="scrollbar-hide mb-6 flex w-full max-w-[600px] items-center justify-center gap-2 overflow-x-auto pb-1">
      <button v-for="tab in searchTabs" :key="tab.label" @click="selectTab(tab)"
        class="flex shrink-0 items-center gap-2 rounded-full border px-4 py-2.5 text-[14px] font-semibold transition md:text-[15px] cursor-pointer"
        :class="activeTab === tab.label
          ? 'border-[#00d4aa] bg-[#00d4aa]/10 text-[#00d4aa]'
          : 'border-[#1e293b] bg-[#1e293b] text-white hover:border-[#334155] hover:text-[#94a3b8]'">
        <component :is="tab.icon" class="h-4 w-4 shrink-0 stroke-[2.2]" />
        <span>{{ tab.label }}</span>
      </button>
    </div>

    <!-- Search bar -->
    <div class="relative w-full max-w-[720px]" ref="searchWrapperRef">
      <div
        class="flex w-full items-center rounded-full border p-[5px] duration-200 sm:p-[6px]"
        :class="searchOpen
          ? 'rounded-b-none rounded-t-[28px] border-b-transparent border-[#334155] bg-[#1e293b]'
          : 'border-[#1e293b] bg-[#1e293b] shadow-[0_2px_12px_rgba(0,0,0,0.3)]'">
        <div class="flex min-w-0 flex-1 items-center gap-2 px-4 md:gap-3 md:px-5">
          <Search class="h-5 w-5 shrink-0 text-[#64748b] sm:h-6 sm:w-6" />
          <input ref="searchInputRef" type="text" v-model="searchQuery"
            :placeholder="placeholderByTab"
            class="w-full border-none bg-transparent text-[15px] text-[#f1f5f9] outline-none placeholder:text-[#64748b] sm:text-[17px]"
            @focus="openSearch" @input="onInput" @keydown.escape="closeSearch"
            @keydown.enter="handleSubmit" />
          <button v-if="searchQuery" @click="clearSearch"
            class="flex h-6 w-6 shrink-0 cursor-pointer items-center justify-center rounded-full bg-[#334155] transition hover:bg-[#475569]">
            <X class="h-3.5 w-3.5 text-[#94a3b8]" />
          </button>
        </div>
        <button @click="handleSubmit"
          class="shrink-0 cursor-pointer rounded-full bg-[#00d4aa] px-5 py-3 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] sm:px-8 sm:py-3.5 sm:text-[16px]">
          Search
        </button>
      </div>

      <!-- Dropdown -->
      <Transition name="search-dropdown">
        <div v-if="searchOpen"
          class="absolute left-0 right-0 top-full z-50 max-h-[400px] overflow-y-auto rounded-b-[28px] border border-t-0 border-[#334155] bg-[#1e293b] shadow-[0_12px_30px_rgba(0,0,0,0.4)]">
          <div class="mx-5 mt-3 h-px bg-[#334155]" />

          <div v-if="!searchQuery && store.liveCount > 0"
            @click="goLive"
            class="flex cursor-pointer items-center gap-4 px-5 py-3 transition-colors hover:bg-[#0f172a]">
            <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#ef4444]/10">
              <span class="h-3 w-3 animate-pulse rounded-full bg-[#ef4444]" />
            </div>
            <div>
              <p class="text-[14px] font-semibold text-[#f1f5f9]">
                {{ store.liveCount }} Live now
              </p>
              <p class="text-[12px] text-[#64748b]">Jump to live matches</p>
            </div>
          </div>

          <div v-if="!searchQuery" class="px-5 pb-1 pt-2">
            <span class="text-[11px] font-semibold uppercase tracking-wider text-[#64748b]">Leagues</span>
          </div>

          <div v-if="isSearching" class="px-5 py-5 text-center text-[13px] text-[#64748b]">
            Searching...
          </div>

          <template v-else-if="suggestions.length">
            <div v-for="item in suggestions" :key="item.id"
              @click="selectSuggestion(item)"
              class="flex cursor-pointer items-center gap-4 px-5 py-3 transition-colors hover:bg-[#0f172a]">
              <div class="flex h-11 w-11 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-[#0f172a]">
                <img v-if="item.logo" :src="item.logo" :alt="item.name"
                  class="h-8 w-8 object-contain" @error="(e) => e.target.style.display='none'" />
                <span v-else class="text-lg">{{ item.flag }}</span>
              </div>
              <div class="flex min-w-0 flex-col">
                <span class="truncate text-[14px] font-semibold text-[#f1f5f9]">{{ item.name }}</span>
                <span class="truncate text-[12px] text-[#64748b]">{{ item.subtitle }}</span>
              </div>
              <span v-if="item.isLive"
                class="ml-auto flex shrink-0 items-center gap-1 rounded-full bg-[#ef4444]/10 px-2 py-0.5 text-[11px] font-bold text-[#ef4444]">
                <span class="h-1.5 w-1.5 animate-pulse rounded-full bg-[#ef4444]" />
                LIVE
              </span>
            </div>
          </template>

          <div v-else-if="searchQuery && !isSearching"
            class="px-5 py-6 text-center text-[13px] text-[#64748b]">
            No results for "{{ searchQuery }}"
          </div>

          <div class="h-2" />
        </div>
      </Transition>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, X, LayoutGrid, Radio, Clock, CheckSquare } from 'lucide-vue-next'
import { useScoresStore } from '@/stores/scores'
import api from '@/api'

const store = useScoresStore()
const router = useRouter()

// ── Tabs  
const searchTabs = computed(() => [
  { label: 'All Games',  icon: LayoutGrid,  filter: 'all',       liveCount: 0 },
  { label: 'Live',       icon: Radio,       filter: 'live',      liveCount: store.liveCount },
  { label: 'Scheduled',  icon: Clock,       filter: 'scheduled', liveCount: 0 },
  { label: 'Finished',    icon: CheckSquare, filter: 'finished',  liveCount: 0 },
])

const activeTab = ref('All Games')

function selectTab(tab) {
  activeTab.value = tab.label
  store.activeFilter = tab.filter
}

const titleByTab = computed(() => {
  switch (activeTab.value) {
    case 'Live':      return '🔴 Live Now'
    case 'Scheduled': return 'Upcoming Games'
    case 'Results':   return 'Latest Results'
    default:          return "Tonight's Basketball"
  }
})

const placeholderByTab = computed(() => {
  switch (activeTab.value) {
    case 'Live':      return 'Search live games or leagues...'
    case 'Scheduled': return 'Search upcoming games...'
    case 'Results':   return 'Search results by team...'
    default:          return 'Teams, leagues, players...'
  }
})

// ── Search start values
const searchQuery = ref('')
const searchOpen = ref(false)
const searchWrapperRef = ref(null)
const searchInputRef = ref(null)
const isSearching = ref(false)
const playerResults = ref([])
let debounce = null

// leagues
const defaultSuggestions = computed(() =>
  store.leagues.map(l => ({
    id: 'l-' + l.id,
    type: 'league',
    leagueId: String(l.id),
    name: l.name,
    subtitle: l.name === 'NBA' ? 'USA · National Basketball Association' : 'Europe · EuroLeague Basketball',
    flag: l.name === 'NBA' ? '🇺🇸' : '🇪🇺',
    logo: l.logo,
    isLive: false,
  }))
)

const suggestions = computed(() => {
  if (!searchQuery.value.trim()) return defaultSuggestions.value

  const q = searchQuery.value.toLowerCase()

  // Teams from store  
  const teamMap = new Map()
  for (const m of store.matches) {
    if (m.homeTeam.toLowerCase().includes(q) && !teamMap.has(m.homeTeamId)) {
      teamMap.set(m.homeTeamId, {
        id: 't-' + m.homeTeamId, type: 'team', teamId: m.homeTeamId,
        name: m.homeTeam, subtitle: m.league, logo: m.homeTeamLogo, flag: m.leagueFlag, isLive: false,
      })
    }
    if (m.awayTeam.toLowerCase().includes(q) && !teamMap.has(m.awayTeamId)) {
      teamMap.set(m.awayTeamId, {
        id: 't-' + m.awayTeamId, type: 'team', teamId: m.awayTeamId,
        name: m.awayTeam, subtitle: m.league, logo: m.awayTeamLogo, flag: m.leagueFlag, isLive: false,
      })
    }
  }

  // Live matches
  const matchSuggestions = store.matches
    .filter(m => m.status === 'live' && (
      m.homeTeam.toLowerCase().includes(q) || m.awayTeam.toLowerCase().includes(q)
    ))
    .slice(0, 3)
    .map(m => ({
      id: 'm-' + m.id, type: 'match', matchId: m.id,
      name: `${m.homeTeam} vs ${m.awayTeam}`,
      subtitle: `${m.league} · LIVE`,
      flag: m.leagueFlag, logo: m.leagueLogo, isLive: true,
    }))

  const playerSuggestions = playerResults.value.slice(0, 4).map(p => ({
    id: 'p-' + p.id, type: 'player', playerId: p.id,
    name: `${p.first_name} ${p.last_name}`,
    subtitle: `${p.team?.name ?? ''} · ${p.position?.name ?? ''}`,
    flag: '👤', logo: p.image_url, isLive: false,
  }))

  return [...teamMap.values(), ...matchSuggestions, ...playerSuggestions].slice(0, 8)
})

async function searchPlayers(q) {
  isSearching.value = true
  try {
    const res = await api.get('players/', { params: { search: q } })
    playerResults.value = res.data.results ?? []
  } catch { playerResults.value = [] }
  finally { isSearching.value = false }
}

function onInput() {
  searchOpen.value = true
  playerResults.value = []
  clearTimeout(debounce)
  if (!searchQuery.value.trim()) return
  debounce = setTimeout(() => searchPlayers(searchQuery.value.trim()), 300)
}

function openSearch() { searchOpen.value = true }
function closeSearch() { searchOpen.value = false }
function clearSearch() { searchQuery.value = ''; playerResults.value = []; searchInputRef.value?.focus() }

function goLive() {
  closeSearch()
  selectTab({ label: 'Live', filter: 'live' })
}

function selectSuggestion(item) {
  searchQuery.value = ''
  playerResults.value = []
  closeSearch()
  if (item.type === 'match')  { router.push(`/match/${item.matchId}`); return }
  if (item.type === 'league') { store.activeLeague = item.leagueId; return }
  if (item.type === 'team')   { router.push(`/team/${item.teamId}`); return }
  if (item.type === 'player') { router.push(`/player/${item.playerId}`); return }
}

function handleSubmit() {
  const first = suggestions.value[0]
  if (first) { selectSuggestion(first); return }
  closeSearch()
}

function handleClickOutside(e) {
  if (searchWrapperRef.value && !searchWrapperRef.value.contains(e.target)) closeSearch()
}

onMounted(() => document.addEventListener('mousedown', handleClickOutside))
onUnmounted(() => { document.removeEventListener('mousedown', handleClickOutside); clearTimeout(debounce) })
</script>

<style scoped>
.title-fade-enter-active,
.title-fade-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.title-fade-enter-from,
.title-fade-leave-to { opacity: 0; transform: translateY(-8px); }

.search-dropdown-enter-active { transition: opacity 0.15s ease, transform 0.15s ease; }
.search-dropdown-leave-active { transition: opacity 0.1s ease, transform 0.1s ease; }
.search-dropdown-enter-from,
.search-dropdown-leave-to { opacity: 0; transform: translateY(-4px); }

.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
