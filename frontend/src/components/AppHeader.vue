<template>
  <header ref="headerRef" class="sticky top-0 z-50 overflow-x-clip bg-[#0f172a] duration-300"
    :class="isScrolled ? 'shadow-[0_4px_24px_rgba(0,0,0,0.4)]' : 'shadow-[0_2px_8px_rgba(0,0,0,0.2)]'">

    <div
      class="mx-auto flex w-full max-w-[1280px] flex-wrap items-center gap-x-3 gap-y-3 px-4 duration-300 sm:px-6 md:flex-nowrap md:gap-4 md:px-8"
      :class="isScrolled ? 'py-2' : 'py-3 md:py-4'">

      <!-- Logo -->
      <div class="flex min-w-0 items-center" :class="!isScrolled ? 'flex-1' : 'flex-1 md:flex-none md:shrink-0'">
        <RouterLink to="/" class="flex items-center gap-2.5">
          <div
            class="flex items-center justify-center duration-300"
            :class="isScrolled ? 'h-7 w-7 text-2xl md:h-8 md:w-8 md:text-3xl' : 'h-9 w-9 text-3xl md:text-4xl'">
            🏀
          </div>
          <span
            class="font-extrabold tracking-tight text-white duration-300"
            :class="isScrolled ? 'text-base md:text-lg' : 'text-xl md:text-2xl'">
            BasketScore
          </span>
        </RouterLink>
      </div>

      <!-- Search bar — slides in when scrolled -->
      <Transition name="search-slide">
        <div v-if="isScrolled"
          class="relative order-3 w-full md:order-none md:w-auto md:shrink md:basis-[280px] lg:basis-[320px]"
          ref="searchRef">
          <div
            class="flex w-full items-center gap-2 rounded-3xl border px-4 py-2 duration-200 sm:px-5"
            :class="searchOpen
              ? 'rounded-b-none border-b-transparent border-[#334155] bg-[#1e293b]'
              : 'border-[#1e293b] bg-[#1e293b] shadow-[0_2px_8px_rgba(0,0,0,0.2)]'">
            <Search class="h-4 w-4 shrink-0 text-[#64748b]" />
            <input ref="searchInputRef" type="text" v-model="searchQuery"
              placeholder="Search teams, leagues..."
              class="min-w-0 flex-1 border-none bg-transparent text-[14px] text-[#f1f5f9] outline-none placeholder:text-[#64748b]"
              @focus="openSearch" @input="onSearchInput" @keydown.escape="closeSearch"
              @keydown.enter="handleSearchSubmit" />
            <button v-if="searchQuery" @click="clearSearch"
              class="flex h-5 w-5 shrink-0 cursor-pointer items-center justify-center rounded-full bg-[#334155] transition hover:bg-[#475569]">
              <X class="h-3 w-3 text-[#94a3b8]" />
            </button>
          </div>

          <!-- Dropdown results -->
          <Transition name="search-dropdown">
            <div v-if="searchOpen"
              class="absolute left-0 right-0 top-full z-50 max-h-[340px] overflow-y-auto rounded-b-2xl border border-t-0 border-[#334155] bg-[#1e293b] shadow-[0_12px_30px_rgba(0,0,0,0.4)]">
              <div class="mx-4 mt-2 h-px bg-[#334155]" />

              <div v-if="!searchQuery" class="px-4 pb-1 pt-2">
                <span class="text-[11px] font-semibold uppercase tracking-wider text-[#64748b]">Popular leagues</span>
              </div>

              <template v-if="filteredSuggestions.length">
                <div v-for="item in filteredSuggestions" :key="item.id + item.type"
                  @click="selectSuggestion(item)"
                  class="flex cursor-pointer items-center gap-3 px-4 py-2.5 transition-colors hover:bg-[#0f172a]">
                  <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-[#0f172a] text-lg overflow-hidden">
                    <img v-if="item.logo" :src="item.logo" class="h-7 w-7 object-contain"
                      @error="(e) => { e.target.style.display='none'; e.target.nextSibling && (e.target.nextSibling.style.display='inline') }" />
                    <span v-if="!item.logo">{{ item.flag }}</span>
                  </div>
                  <div class="flex min-w-0 flex-1 flex-col">
                    <span class="truncate text-[14px] font-semibold text-[#f1f5f9]">{{ item.name }}</span>
                    <span class="truncate text-[12px] text-[#64748b]">
                      {{ item.type === 'player' ? '👤 Player' : item.type === 'team' ? '🏀 Team' : item.subtitle }}
                    </span>
                  </div>
                  <span v-if="item.type === 'match' && item.status === 'live'"
                    class="ml-auto flex items-center gap-1 rounded-full bg-[#ef4444]/10 px-2 py-0.5 text-[11px] font-bold text-[#ef4444]">
                    <span class="h-1.5 w-1.5 animate-pulse rounded-full bg-[#ef4444]" />
                    LIVE
                  </span>
                </div>
              </template>

              <div v-else-if="searchQuery"
                class="px-4 py-5 text-center text-[13px] text-[#64748b]">
                No results for "{{ searchQuery }}"
              </div>

              <div class="h-2" />
            </div>
          </Transition>
        </div>
      </Transition>

      <!-- Nav -->
      <nav
        class="order-3 flex w-full min-w-0 flex-wrap items-center justify-center gap-1 md:order-none md:w-auto md:flex-nowrap lg:gap-1"
        :class="isScrolled ? 'md:justify-start' : 'md:flex-1 md:justify-center'">
        <RouterLink to="/"
          class="rounded-full px-3 py-2 text-[15px] font-semibold transition-colors lg:px-4 lg:text-[16px]"
          :class="$route.path === '/' ? 'text-[#00d4aa]' : 'text-[#94a3b8] hover:bg-[#1e293b] hover:text-white'">
          Scores
        </RouterLink>
        <RouterLink to="/standings"
          class="rounded-full px-3 py-2 text-[15px] font-semibold transition-colors lg:px-4 lg:text-[16px]"
          :class="$route.path.startsWith('/standings') ? 'text-[#00d4aa]' : 'text-[#94a3b8] hover:bg-[#1e293b] hover:text-white'">
          Standings
        </RouterLink>
      </nav>

      <!-- Right side -->
      <div class="ml-auto flex min-w-0 shrink-0 items-center gap-2 sm:gap-3"
        :class="!isScrolled ? 'md:flex-1 md:justify-end' : ''">

        <!-- Favourites -->
        <button @click="goToFavourites"
          class="group flex cursor-pointer items-center gap-2 rounded-full border border-[#1e293b] px-4 py-2 text-[14px] font-semibold text-[#f1f5f9] transition hover:border-[#334155] hover:bg-[#1e293b] sm:px-5 sm:py-2.5 sm:text-[15px]">
          <Heart class="h-4 w-4 text-[#f1f5f9] transition-colors group-hover:fill-red-500 group-hover:text-red-500" />
          Favourites
        </button>

        <!-- User dropdown / Sign in -->
        <template v-if="isLoggedIn">
          <div class="relative" ref="dropdownRef">
            <button @click="dropdownOpen = !dropdownOpen"
              class="flex items-center gap-2 rounded-full border border-[#1e293b] px-3 py-2 text-[14px] font-semibold text-[#f1f5f9] transition hover:border-[#334155] hover:bg-[#1e293b]">
              <UserCircle class="h-5 w-5 text-[#94a3b8]" />
              <span class="hidden max-w-[120px] truncate sm:block">{{ user?.username }}</span>
              <ChevronDown class="h-4 w-4 text-[#64748b] transition-transform duration-200"
                :class="dropdownOpen ? 'rotate-180' : ''" />
            </button>

            <Transition name="dropdown">
              <div v-if="dropdownOpen"
                class="absolute right-0 top-[calc(100%+8px)] z-50 w-48 rounded-2xl border border-[#1e293b] bg-[#0f172a] py-2 shadow-[0_8px_30px_rgba(0,0,0,0.4)]">
                <button @click="dropdownOpen = false; router.push('/profile')"
                  class="flex w-full items-center gap-3 px-4 py-2.5 text-[14px] text-[#94a3b8] transition hover:bg-[#1e293b] hover:text-white">
                  <User class="h-4 w-4" /> Profile
                </button>
                <button v-if="isAdmin" @click="dropdownOpen = false; router.push('/admin')"
                  class="flex w-full items-center gap-3 px-4 py-2.5 text-[14px] text-[#00d4aa] transition hover:bg-[#1e293b]">
                  <ShieldCheck class="h-4 w-4" /> Admin Panel
                </button>
                <div class="my-1 border-t border-[#1e293b]" />
                <button @click="logout"
                  class="flex w-full items-center gap-3 px-4 py-2.5 text-[14px] text-red-400 transition hover:bg-[#1e293b]">
                  <LogOut class="h-4 w-4" /> Sign out
                </button>
              </div>
            </Transition>
          </div>
        </template>

        <button v-else @click="showLogin = true"
          class="cursor-pointer rounded-full bg-[#00d4aa] px-4 py-2 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] sm:px-5 sm:py-2.5 sm:text-[15px]">
          Sign In
        </button>
      </div>
    </div>

    <!-- League filter tabs -->
    <Transition name="tabs-drop">
      <div v-if="showLeagueTabs" class="border-t border-[#1e293b] bg-[#0f172a]">
        <div
          class="scrollbar-hide mx-auto flex w-full max-w-[1280px] items-center gap-1 overflow-x-auto overscroll-x-contain px-4 sm:px-6 md:px-6 ">
          <button
            v-for="tab in leagueTabs" :key="tab.id"
            @click="setLeague(tab.id)"
            class="flex shrink-0 items-center gap-2 border-b-2 px-3 py-3 text-[14px] font-semibold whitespace-nowrap transition-colors cursor-pointer"
            :class="store.activeLeague === tab.id
              ? 'border-[#00d4aa] text-[#00d4aa]'
              : 'border-transparent text-[#64748b] hover:border-[#334155] hover:text-[#94a3b8]'">
            <img v-if="tab.logo" :src="tab.logo" :alt="tab.label"
              class="h-5 w-5 shrink-0 object-contain"
              @error="(e) => e.target.style.display='none'" />
            <span v-else class="text-base leading-none">{{ tab.flag }}</span>
            <span>{{ tab.label }}</span>
          </button>
        </div>
      </div>
    </Transition>
  </header>

  <LoginModal v-model="showLogin" />

  <!-- Toast -->
  <Teleport to="body">
    <Transition name="toast">
      <div v-if="toastMsg"
        class="fixed top-6 left-1/2 z-100 -translate-x-1/2 rounded-xl border border-[#334155] bg-red-500 px-5 py-3 text-[14px] font-semibold text-[#f1f5f9] shadow-2xl">
        {{ toastMsg }}
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import {
  Search, X, ChevronDown, UserCircle, User, Heart, LogOut, ShieldCheck,
} from 'lucide-vue-next'
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useScoresStore } from '@/stores/scores'
import { useAuth } from '@/composables/useAuth'
import LoginModal from '@/components/LoginModal.vue'
import api from '@/api'

const LEAGUE_FLAGS = { 'NBA': '🇺🇸', 'Euroleague': '🇪🇺' }

const store = useScoresStore()
const router = useRouter()
const route = useRoute()

// ── Toast  
const toastMsg = ref('')
let toastTimer = null
function showToast(msg) {
  toastMsg.value = msg
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toastMsg.value = '' }, 3000)
}

function goToFavourites() {
  if (isLoggedIn.value) {
    router.push('/favourites')
  } else {
    showToast('Must be logged in to access favourites!')
  }
}

// ── Auth  
const showLogin = ref(false)
const dropdownOpen = ref(false)
const dropdownRef = ref(null)

async function logout() {
  dropdownOpen.value = false
  await logoutUser()
  router.push('/')
}

// ── Scroll 
const isScrolled = ref(false)
const headerRef = ref(null)
const handleScroll = () => { isScrolled.value = window.scrollY > 120; if (searchOpen.value) closeSearch() }

// ── Search  
const searchQuery = ref('')
const searchOpen = ref(false)
const searchRef = ref(null)
const searchInputRef = ref(null)
const playerSuggestions = ref([])
let playerSearchTimer = null

const allSuggestions = computed(() => {
  const leagueSuggestions = store.leagues.map(l => ({
    id: 'league-' + l.id,
    type: 'league',
    leagueId: String(l.id),
    name: l.name,
    subtitle: l.name === 'NBA' ? 'USA · National Basketball Association' : 'Europe · EuroLeague Basketball',
    logo: l.logo ?? null,
    flag: LEAGUE_FLAGS[l.name] ?? '🏀',
  }))

  const teamMap = new Map()
  for (const m of store.matches) {
    if (!teamMap.has(m.homeTeamId)) {
      teamMap.set(m.homeTeamId, {
        id: 'team-' + m.homeTeamId, type: 'team',
        teamId: m.homeTeamId, name: m.homeTeam,
        logo: m.homeTeamLogo, subtitle: m.league, flag: m.leagueFlag,
      })
    }
    if (!teamMap.has(m.awayTeamId)) {
      teamMap.set(m.awayTeamId, {
        id: 'team-' + m.awayTeamId, type: 'team',
        teamId: m.awayTeamId, name: m.awayTeam,
        logo: m.awayTeamLogo, subtitle: m.league, flag: m.leagueFlag,
      })
    }
  }

  const live = store.matches
    .filter(m => m.status === 'live')
    .map(m => ({
      id: 'match-' + m.id, type: 'match', matchId: m.id,
      name: `${m.homeTeam} vs ${m.awayTeam}`,
      subtitle: m.league, flag: m.leagueFlag, logo: null,
    }))

  return [...live, ...leagueSuggestions, ...teamMap.values()]
})

const filteredSuggestions = computed(() => {
  if (!searchQuery.value.trim()) return allSuggestions.value.filter(s => s.type === 'league')
  const q = searchQuery.value.toLowerCase()
  const static_ = allSuggestions.value.filter(s => s.name.toLowerCase().includes(q))
  const players = playerSuggestions.value.map(p => ({
    id: 'player-' + p.id, type: 'player', playerId: p.id,
    name: `${p.first_name} ${p.last_name}`,
    subtitle: p.team?.name ?? '',
    logo: p.image_url ?? null, flag: '👤',
  }))
  return [...static_, ...players].slice(0, 10)
})

async function fetchPlayers(q) {
  if (q.length < 2) { playerSuggestions.value = []; return }
  try {
    const { data } = await api.get('players/', { params: { search: q } })
    playerSuggestions.value = (data.results ?? []).slice(0, 5)
  } catch {
    playerSuggestions.value = []
  }
}

function openSearch() { searchOpen.value = true }
function closeSearch() { searchOpen.value = false; playerSuggestions.value = [] }
function clearSearch() { searchQuery.value = ''; playerSuggestions.value = []; searchOpen.value = true; searchInputRef.value?.focus() }
function onSearchInput() {
  searchOpen.value = true
  clearTimeout(playerSearchTimer)
  playerSearchTimer = setTimeout(() => fetchPlayers(searchQuery.value.trim()), 300)
}

function selectSuggestion(item) {
  searchQuery.value = ''
  playerSuggestions.value = []
  closeSearch()
  if (item.type === 'match')  { router.push(`/match/${item.matchId}`); return }
  if (item.type === 'league') { store.activeLeague = item.leagueId; router.push('/'); return }
  if (item.type === 'team')   { router.push(`/team/${item.teamId}`); return }
  if (item.type === 'player') { router.push(`/player/${item.playerId}`); return }
}

function handleSearchSubmit() {
  const q = searchQuery.value.trim()
  if (!q) return
  const first = filteredSuggestions.value[0]
  if (first) { selectSuggestion(first); return }
  closeSearch()
}

// ── League tabs 
const showLeagueTabs = computed(() => route.path === '/')

const leagueTabs = computed(() => {
  const all = { id: 'all', label: 'All', logo: null, flag: '🏀', liveCount: store.liveCount }
  const fromApi = store.leagues.map(l => ({
    id: String(l.id),
    label: l.name,
    logo: l.logo ?? null,
    flag: LEAGUE_FLAGS[l.name] ?? '🏀',
    liveCount: store.matches.filter(m => m.leagueId === String(l.id) && m.status === 'live').length,
  }))
  return [all, ...fromApi]
})

function setLeague(id) {
  store.activeLeague = id
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// ── Click outside  s
const handleClickOutside = (e) => {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target)) dropdownOpen.value = false
  if (searchRef.value && !searchRef.value.contains(e.target)) closeSearch()
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
  document.addEventListener('mousedown', handleClickOutside)
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('mousedown', handleClickOutside)
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(12px);
}

.search-slide-enter-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.search-slide-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.search-slide-enter-from,
.search-slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.tabs-drop-enter-active,
.tabs-drop-leave-active {
  transition: opacity 0.2s ease, max-height 0.25s ease;
  max-height: 60px;
  overflow: hidden;
}
.tabs-drop-enter-from,
.tabs-drop-leave-to {
  opacity: 0;
  max-height: 0;
}

.backdrop-enter-active,
.backdrop-leave-active {
  transition: opacity 0.25s ease;
}
.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}

.search-dropdown-enter-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.search-dropdown-leave-active {
  transition: opacity 0.1s ease, transform 0.1s ease;
}
.search-dropdown-enter-from,
.search-dropdown-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
