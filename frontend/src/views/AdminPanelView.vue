<template>
  <div class="mx-auto max-w-[1280px] px-4 py-10 sm:px-6 md:px-8">
    <h1 class="mb-6 text-2xl font-extrabold text-[#f1f5f9]">Admin Panel</h1>

    <!-- Tab navigation -->
    <div class="mb-8 overflow-x-auto">
      <div class="flex gap-1 rounded-xl bg-[#1e293b] p-1 w-fit whitespace-nowrap">
        <button v-for="tab in tabs" :key="tab.key" @click="activeTab = tab.key"
          class="flex items-center gap-2 rounded-lg px-4 py-2 text-sm font-semibold transition cursor-pointer"
          :class="activeTab === tab.key ? 'bg-[#0f172a] text-[#f1f5f9] shadow' : 'text-white hover:text-[#94a3b8]'">
          <component :is="tab.icon" class="h-4 w-4" />
          {{ tab.label }}
        </button>
      </div>
    </div>

    <!-- Feedback -->
    <div v-if="error" class="mb-4 rounded-xl bg-red-500/10 px-4 py-2.5 text-sm text-red-400">{{ error }}</div>
    <div v-if="success" class="mb-4 rounded-xl bg-[#00d4aa]/10 px-4 py-2.5 text-sm text-[#00d4aa]">{{ success }}</div>

    <!-- ── USERS ── -->
    <div v-if="activeTab === 'users'">
      <div class="mb-6 flex items-center gap-3">
        <div class="relative flex-1 max-w-sm">
          <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#475569]" />
          <input v-model="userQuery" type="text" placeholder="Search by username or email..."
            class="w-full rounded-xl border border-[#1e293b] bg-[#0f172a] pl-9 pr-4 py-2.5 text-[14px] text-[#f1f5f9] outline-none focus:border-[#00d4aa] transition placeholder:text-[#475569]"
            @input="debouncedFetchUsers" />
        </div>
      </div>

      <div class="overflow-x-auto rounded-2xl border border-[#1e293b]">
        <table class="w-full text-[14px]">
          <thead>
            <tr class="border-b border-[#1e293b] bg-[#0f172a] text-left">
              <th class="px-4 py-3 font-semibold text-white">Username</th>
              <th class="px-4 py-3 font-semibold text-white">Email</th>
              <th class="px-4 py-3 font-semibold text-white">Joined</th>
              <th class="px-4 py-3 font-semibold text-white">Status</th>
              <th class="px-4 py-3 font-semibold text-white">Role</th>
              <th class="px-4 py-3 font-semibold text-white">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="usersLoading">
              <td colspan="6" class="px-4 py-8 text-center text-[#475569]">Loading...</td>
            </tr>
            <tr v-else-if="!users.length">
              <td colspan="6" class="px-4 py-8 text-center text-[#475569]">No users found.</td>
            </tr>
            <tr v-for="u in users" :key="u.id"
              class="border-b border-[#1e293b] bg-[#0f172a] transition hover:bg-[#1e293b]">
              <td class="px-4 py-3 font-semibold text-[#f1f5f9]">{{ u.username }}</td>
              <td class="px-4 py-3 text-[#94a3b8]">{{ u.email }}</td>
              <td class="px-4 py-3 text-[#64748b]">{{ formatDate(u.date_joined) }}</td>
              <td class="px-4 py-3">
                <span class="rounded-full px-2.5 py-1 text-[11px] font-bold"
                  :class="u.is_active ? 'bg-[#22c55e]/10 text-[#22c55e]' : 'bg-red-500/10 text-red-400'">
                  {{ u.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <span class="rounded-full px-2.5 py-1 text-[11px] font-bold"
                  :class="u.is_staff ? 'bg-[#00d4aa]/10 text-[#00d4aa]' : 'bg-[#1e293b] text-[#475569]'">
                  {{ u.is_staff ? 'Admin' : 'User' }}
                </span>
              </td>
              <td class="px-4 py-3">
                <button @click="deleteTarget = u"
                  class="rounded-lg border border-[#334155] px-2.5 py-1 text-[12px] font-semibold text-red-400 transition hover:border-red-400 cursor-pointer">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-if="userTotalPages > 1" class="mt-4 flex items-center justify-center gap-2">
        <button @click="userPage--; fetchUsers()" :disabled="userPage === 1"
          class="rounded-lg border border-[#1e293b] px-3 py-1.5 text-[13px] text-[#94a3b8] transition hover:border-[#334155] disabled:opacity-30">
          Previous
        </button>
        <span class="text-[13px] text-[#64748b]">{{ userPage }} / {{ userTotalPages }}</span>
        <button @click="userPage++; fetchUsers()" :disabled="userPage === userTotalPages"
          class="rounded-lg border border-[#1e293b] px-3 py-1.5 text-[13px] text-[#94a3b8] transition hover:border-[#334155] disabled:opacity-30">
          Next
        </button>
      </div>
    </div>

    <!-- ── TEAMS (add to league) ── -->
    <div v-else-if="activeTab === 'teams'">
      <div class="rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6 max-w-1280px">
        <h2 class="mb-5 text-[15px] font-bold text-[#f1f5f9]">Add Team to League</h2>
        <form @submit.prevent="submitLeagueTeam" class="flex flex-col gap-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">League</label>
            <select v-model="ltForm.league_id" required class="admin-select">
              <option value="" disabled>Select league</option>
              <option v-for="l in refData.leagues" :key="l.id" :value="l.id">{{ l.name }}</option>
            </select>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Team</label>
            <select v-model="ltForm.team_id" required class="admin-select">
              <option value="" disabled>Select team</option>
              <option v-for="t in refData.teams" :key="t.id" :value="t.id">{{ t.name }}</option>
            </select>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Season</label>
            <select v-model="ltForm.season_id" required class="admin-select">
              <option value="" disabled>Select season</option>
              <option v-for="s in refData.seasons" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-3">
            <div class="flex flex-col gap-1.5">
              <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Wins</label>
              <input v-model.number="ltForm.win" type="number" min="0" class="admin-input" placeholder="0" />
            </div>
            <div class="flex flex-col gap-1.5">
              <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Losses</label>
              <input v-model.number="ltForm.loss" type="number" min="0" class="admin-input" placeholder="0" />
            </div>
          </div>
          <button type="submit" :disabled="ltSubmitting"
            class="mt-1 w-full cursor-pointer rounded-xl bg-[#00d4aa] py-2.5 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] disabled:opacity-50">
            {{ ltSubmitting ? 'Adding...' : 'Add to League' }}
          </button>
        </form>
      </div>
    </div>

    <!-- ── MATCHES ── -->
    <div v-else-if="activeTab === 'matches'">
      <div class="flex flex-col gap-8 max-w-1280px">
        <div class="rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6">
          <h2 class="mb-5 text-[15px] font-bold text-[#f1f5f9]">Create Match</h2>
          <form @submit.prevent="submitMatch" class="flex flex-col gap-4">
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Home Team</label>
                <select v-model="matchForm.home_team_id" required class="admin-select">
                  <option value="" disabled>Select</option>
                  <option v-for="t in refData.teams" :key="t.id" :value="t.id">{{ t.name }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Away Team</label>
                <select v-model="matchForm.away_team_id" required class="admin-select">
                  <option value="" disabled>Select</option>
                  <option v-for="t in refData.teams" :key="t.id" :value="t.id">{{ t.name }}</option>
                </select>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">League</label>
                <select v-model="matchForm.league_id" required class="admin-select">
                  <option value="" disabled>Select</option>
                  <option v-for="l in refData.leagues" :key="l.id" :value="l.id">{{ l.name }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Season</label>
                <select v-model="matchForm.season_id" required class="admin-select">
                  <option value="" disabled>Select</option>
                  <option v-for="s in refData.seasons" :key="s.id" :value="s.id">{{ s.name }}</option>
                </select>
              </div>
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Status</label>
                <select v-model="matchForm.status_id" required class="admin-select">
                  <option value="" disabled>Select</option>
                  <option v-for="s in refData.statuses" :key="s.id" :value="s.id">{{ s.name }}</option>
                </select>
              </div>
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Hall (optional)</label>
                <select v-model="matchForm.hall_id" class="admin-select">
                  <option :value="null">— None —</option>
                  <option v-for="h in refData.halls" :key="h.id" :value="h.id">{{ h.name }}</option>
                </select>
              </div>
            </div>
            <div class="flex flex-col gap-1.5">
              <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Date & Time</label>
              <input v-model="matchForm.match_date" type="datetime-local" required class="admin-input" />
            </div>
            <div class="grid grid-cols-2 gap-3">
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Home Score</label>
                <input v-model.number="matchForm.home_score" type="number" min="0" class="admin-input" placeholder="—" />
              </div>
              <div class="flex flex-col gap-1.5">
                <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Away Score</label>
                <input v-model.number="matchForm.away_score" type="number" min="0" class="admin-input" placeholder="—" />
              </div>
            </div>
            <button type="submit" :disabled="matchSubmitting"
              class="mt-1 w-full cursor-pointer rounded-xl bg-[#00d4aa] py-2.5 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] disabled:opacity-50">
              {{ matchSubmitting ? 'Creating...' : 'Create Match' }}
            </button>
          </form>
        </div>

        <div class="rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6">
          <h2 class="mb-4 text-[15px] font-bold text-[#f1f5f9]">Recent Matches</h2>
          <div v-if="!refData.recentMatches.length" class="py-8 text-center text-[13px] text-[#475569]">
            No matches yet.
          </div>
          <div v-for="m in refData.recentMatches" :key="m.id"
            class="flex items-center justify-between border-b border-[#1e293b]/60 py-2.5 last:border-0">
            <div class="min-w-0 flex-1">
              <p class="truncate text-[13px] font-semibold text-[#f1f5f9]">
                {{ m.home_team?.name }} vs {{ m.away_team?.name }}
              </p>
              <p class="text-[12px] text-[#64748b]">{{ m.league?.name }} · {{ formatDate(m.match_date) }}</p>
            </div>
            <span class="ml-3 shrink-0 rounded-full px-2 py-0.5 text-[11px] font-bold"
              :class="m.status?.name?.toLowerCase() === 'live'
                ? 'bg-red-500/10 text-red-400'
                : 'bg-[#1e293b] text-[#64748b]'">
              {{ m.status?.name }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- ── STATS ── -->
    <div v-else-if="activeTab === 'stats'">
      <div class="rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6 max-w-1280px">
        <h2 class="mb-5 text-[15px] font-bold text-[#f1f5f9]">Add Player Stats</h2>
        <form @submit.prevent="submitStats" class="flex flex-col gap-4">
          <div class="flex flex-col gap-1.5">
            <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Match</label>
            <select v-model="statsForm.match_id" required class="admin-select">
              <option value="" disabled>Select match</option>
              <option v-for="m in refData.recentMatches" :key="m.id" :value="m.id">
                {{ m.home_team?.name }} vs {{ m.away_team?.name }} ({{ formatDate(m.match_date) }})
              </option>
            </select>
          </div>
          <div class="flex flex-col gap-1.5">
            <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">Player</label>
            <select v-model="statsForm.player_id" required class="admin-select">
              <option value="" disabled>Select player</option>
              <option v-for="p in refData.players" :key="p.id" :value="p.id">
                {{ p.first_name }} {{ p.last_name }} ({{ p.team?.name ?? '—' }})
              </option>
            </select>
          </div>
          <div class="grid grid-cols-3 gap-3">
            <div v-for="field in statFields" :key="field.key" class="flex flex-col gap-1.5">
              <label class="text-[12px] font-semibold uppercase tracking-wider text-[#64748b] pl-[5.6px]">{{ field.label }}</label>
              <input v-model.number="statsForm[field.key]" type="number" min="0" class="admin-input" placeholder="0" />
            </div>
          </div>
          <button type="submit" :disabled="statsSubmitting"
            class="mt-1 w-full cursor-pointer rounded-xl bg-[#00d4aa] py-2.5 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] disabled:opacity-50">
            {{ statsSubmitting ? 'Saving...' : 'Save Stats' }}
          </button>
        </form>
      </div>
    </div>

    <!-- Delete user modal -->
    <Teleport to="body">
      <Transition name="backdrop">
        <div v-if="deleteTarget" class="fixed inset-0 z-[60] flex items-center justify-center p-4">
          <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="deleteTarget = null" />
          <div class="relative z-10 w-full max-w-sm rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6 shadow-2xl">
            <h3 class="mb-2 text-[16px] font-bold text-[#f1f5f9]">Delete user?</h3>
            <p class="mb-6 text-[14px] text-[#64748b]">
              This will permanently delete <strong class="text-[#f1f5f9]">{{ deleteTarget?.username }}</strong>. This action cannot be undone.
            </p>
            <div class="flex gap-3">
              <button @click="deleteTarget = null"
                class="flex-1 cursor-pointer rounded-xl border border-[#334155] py-2.5 text-[14px] font-semibold text-[#94a3b8] transition hover:bg-[#1e293b]">
                Cancel
              </button>
              <button @click="deleteUser" :disabled="deleting"
                class="flex-1 cursor-pointer rounded-xl bg-red-500 py-2.5 text-[14px] font-bold text-white transition hover:bg-red-600 disabled:opacity-50">
                {{ deleting ? 'Deleting...' : 'Delete' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Users, Trophy, Calendar, BarChart2 } from 'lucide-vue-next'
import { useAuth } from '@/composables/useAuth'
import { fetchAll } from '@/api'
import {
  adminGetUsers, adminDeleteUser,
  adminCreateLeagueTeam, adminCreateMatch, adminCreatePlayerStats,
} from '@/api'

const { isAdmin } = useAuth()
const router = useRouter()

const activeTab = ref('users')
const tabs = [
  { key: 'users',   label: 'Users',   icon: Users },
  { key: 'teams',   label: 'Teams',   icon: Trophy },
  { key: 'matches', label: 'Matches', icon: Calendar },
  { key: 'stats',   label: 'Stats',   icon: BarChart2 },
]

const error = ref('')
const success = ref('')
function showSuccess(msg) {
  success.value = msg; error.value = ''
  setTimeout(() => { success.value = '' }, 3000)
}
function showError(msg) {
  error.value = msg; success.value = ''
}

// ── Reference data  
const refData = reactive({
  leagues: [], teams: [], seasons: [], statuses: [],
  halls: [], players: [], recentMatches: [], leagueTeams: [],
})

async function loadRefData() {
  const [leagues, teams, seasons, statuses, halls, players, matches, leagueTeams] = await Promise.all([
    fetchAll('leagues/'),
    fetchAll('teams/'),
    fetchAll('seasons/'),
    fetchAll('status/'),
    fetchAll('halls/'),
    fetchAll('players/'),
    fetchAll('matches/'),
    fetchAll('league-teams/'),
  ])
  refData.leagues = leagues
  refData.teams = teams
  refData.seasons = seasons
  refData.statuses = statuses
  refData.halls = halls
  refData.players = players
  refData.recentMatches = matches.slice(0, 50)
  refData.leagueTeams = leagueTeams.slice(0, 20)
}

// ── Users  
const users = ref([])
const usersLoading = ref(true)
const userQuery = ref('')
const userPage = ref(1)
const userTotalPages = ref(1)
const deleteTarget = ref(null)
const deleting = ref(false)

let debounceTimer = null
function debouncedFetchUsers() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { userPage.value = 1; fetchUsers() }, 300)
}

async function fetchUsers() {
  usersLoading.value = true
  try {
    const data = await adminGetUsers({ q: userQuery.value, page: userPage.value })
    users.value = data.results
    userTotalPages.value = Math.ceil(data.count / (data.results.length || 20)) || 1
  } catch {
    showError('Failed to load users.')
  } finally {
    usersLoading.value = false
  }
}

async function deleteUser() {
  deleting.value = true
  try {
    await adminDeleteUser(deleteTarget.value.id)
    users.value = users.value.filter(u => u.id !== deleteTarget.value.id)
    deleteTarget.value = null
    showSuccess('User deleted.')
  } catch {
    showError('Failed to delete user.')
  } finally {
    deleting.value = false
  }
}

// ── League Teams form  
const ltForm = reactive({ league_id: '', team_id: '', season_id: '', win: 0, loss: 0 })
const ltSubmitting = ref(false)

async function submitLeagueTeam() {
  ltSubmitting.value = true
  try {
    const entry = await adminCreateLeagueTeam({ ...ltForm })
    refData.leagueTeams.unshift(entry)
    Object.assign(ltForm, { league_id: '', team_id: '', season_id: '', win: 0, loss: 0 })
    showSuccess('Team added to league.')
  } catch {
    showError('Failed to add team to league.')
  } finally {
    ltSubmitting.value = false
  }
}

// ── Match form  
const matchForm = reactive({
  home_team_id: '', away_team_id: '', league_id: '', season_id: '',
  status_id: '', hall_id: null, match_date: '', home_score: null, away_score: null,
})
const matchSubmitting = ref(false)

async function submitMatch() {
  matchSubmitting.value = true
  try {
    const payload = { ...matchForm }
    if (!payload.home_score && payload.home_score !== 0) payload.home_score = null
    if (!payload.away_score && payload.away_score !== 0) payload.away_score = null
    const created = await adminCreateMatch(payload)
    refData.recentMatches.unshift(created)
    Object.assign(matchForm, {
      home_team_id: '', away_team_id: '', league_id: '', season_id: '',
      status_id: '', hall_id: null, match_date: '', home_score: null, away_score: null,
    })
    showSuccess('Match created.')
  } catch {
    showError('Failed to create match.')
  } finally {
    matchSubmitting.value = false
  }
}

// ── Stats form  
const statFields = [
  { key: 'points',       label: 'PTS' },
  { key: 'rebounds',     label: 'REB' },
  { key: 'assists',      label: 'AST' },
  { key: 'steals',       label: 'STL' },
  { key: 'blocks',       label: 'BLK' },
  { key: 'turnovers',    label: 'TO' },
  { key: 'fouls',        label: 'PF' },
  { key: 'minutes_played', label: 'MIN' },
  { key: 'fg_made',      label: 'FGM' },
  { key: 'fg_attempted', label: 'FGA' },
  { key: 'three_pt_made',      label: '3PM' },
  { key: 'three_pt_attempted', label: '3PA' },
  { key: 'ft_made',      label: 'FTM' },
  { key: 'ft_attempted', label: 'FTA' },
]

const statsForm = reactive({
  match_id: '', player_id: '',
  points: null, rebounds: null, assists: null, steals: null, blocks: null,
  turnovers: null, fouls: null, minutes_played: null,
  fg_made: null, fg_attempted: null,
  three_pt_made: null, three_pt_attempted: null,
  ft_made: null, ft_attempted: null,
})
const statsSubmitting = ref(false)
const recentStats = ref([])

async function submitStats() {
  statsSubmitting.value = true
  try {
    const created = await adminCreatePlayerStats({ ...statsForm })
    recentStats.value.unshift(created)
    const mid = statsForm.match_id
    Object.assign(statsForm, {
      match_id: mid, player_id: '',
      points: null, rebounds: null, assists: null, steals: null, blocks: null,
      turnovers: null, fouls: null, minutes_played: null,
      fg_made: null, fg_attempted: null,
      three_pt_made: null, three_pt_attempted: null,
      ft_made: null, ft_attempted: null,
    })
    showSuccess('Stats saved.')
  } catch {
    showError('Failed to save stats.')
  } finally {
    statsSubmitting.value = false
  }
}

function formatDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  if (!isAdmin.value) { router.push('/'); return }
  await Promise.all([fetchUsers(), loadRefData()])
})
</script>

<style scoped>
.admin-select,
.admin-input {
  width: 100%;
  border-radius: 0.75rem;
  border: 1px solid #1e293b;
  background-color: #111827;
  padding: 0.625rem 0.75rem;
  font-size: 14px;
  color: #f1f5f9;
  outline: none;
  transition: border-color 0.2s;
}
.admin-select:focus,
.admin-input:focus {
  border-color: #00d4aa;
}
.backdrop-enter-active,
.backdrop-leave-active { transition: opacity 0.2s ease; }
.backdrop-enter-from,
.backdrop-leave-to { opacity: 0; }
</style>
