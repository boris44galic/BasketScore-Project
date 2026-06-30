<template>
  <section class="mx-auto mt-6 w-full max-w-[1280px] px-4 md:px-8">
    <!-- Loading  -->
    <div v-if="loading"
      class="h-[320px] animate-pulse rounded-2xl bg-[#1e293b] md:h-[420px] md:rounded-3xl" />

    <div v-else-if="scorers.length" class="relative overflow-hidden rounded-2xl md:rounded-3xl"
      :style="{ background: `linear-gradient(135deg, ${current.bgFrom} 0%, ${current.bgTo} 100%)` }"
      style="transition: background 0.7s ease">

      <!-- Slides track -->
      <div class="flex transition-transform duration-700 ease-in-out"
        :style="{ transform: `translateX(-${activeSlide * 100}%)` }">

        <div v-for="player in scorers" :key="player.id"
          class="flex min-w-0 flex-[0_0_100%] flex-col items-stretch md:flex-row">

          <!-- ── Left: visual panel ── -->
          <div class="relative mx-3 mt-3 flex h-[240px] shrink-0 flex-col overflow-hidden rounded-2xl md:m-4 md:h-[360px] md:w-[52%]"
            :style="{ background: `linear-gradient(145deg, ${player.bgFrom}cc 0%, ${player.bgTo} 100%)` }">

            <!-- Decorative circles -->
            <div class="pointer-events-none absolute inset-0 overflow-hidden">
              <div class="absolute -right-16 -top-16 h-64 w-64 rounded-full opacity-10"
                :style="{ background: player.accent }" />
              <div class="absolute -bottom-10 -left-10 h-48 w-48 rounded-full opacity-[0.08]"
                :style="{ background: player.accent }" />
              <div class="absolute right-10 top-10 h-32 w-32 rounded-full border-2 opacity-10"
                :style="{ borderColor: player.accent }" />
            </div>

            <!-- Player image or initials -->
            <div class="flex flex-1 items-center justify-center">
              <img v-if="player.imageUrl"
                :src="player.imageUrl" :alt="player.name"
                class="h-48 w-48 rounded-full object-cover object-top shadow-2xl md:h-64 md:w-64"
                style="box-shadow: 0 8px 40px rgba(0,0,0,0.5)"
                @error="(e) => e.target.style.display = 'none'" />
              <span v-else
                class="select-none font-black leading-none opacity-40"
                :style="{ fontSize: '120px', color: player.accent }">
                {{ player.initials }}
              </span>
            </div>

            <!-- Bottom tag -->
            <div class="absolute bottom-3 left-3 flex items-center gap-2">
              <span class="rounded-full px-3 py-1 text-xs font-bold text-white/90"
                :style="{ background: `${player.accent}30`, border: `1px solid ${player.accent}60` }">
                {{ player.teamShort }}
              </span>
              <span class="rounded-full px-3 py-1 text-xs font-bold text-white/90"
                :style="{ background: `${player.accent}30`, border: `1px solid ${player.accent}60` }">
                {{ player.pos }}
              </span>
            </div>
          </div>

          <!-- ── Right: text panel ── -->
          <div class="flex min-h-[220px] flex-1 flex-col justify-center px-6 pb-10 pt-5 md:min-h-0 md:px-10 md:pb-0 md:pt-0">

            <span class="mb-3 inline-flex w-fit items-center gap-1.5 rounded-full px-3 py-1 text-[11px] font-bold uppercase tracking-wider"
              :style="{ background: `${player.accent}20`, color: player.accent }">
              🏀 Season Leader
            </span>

            <h2 class="text-[28px] font-extrabold leading-tight text-white md:text-[40px]">
              {{ player.name }}
            </h2>
            <p class="mt-1 text-[14px] pl-1 font-semibold text-white/50">{{ player.team }}</p>

            <!-- Stats row -->
            <div class="mt-10 flex items-center gap-4 md:gap-6">
              <div v-for="stat in player.stats" :key="stat.label" class="flex flex-col items-center">
                <span class="text-[26px] font-black leading-none text-white md:text-[34px]">
                  {{ stat.val }}
                </span>
                <span class="mt-0.5 text-[11px] font-bold uppercase tracking-wider"
                  :style="{ color: player.accent }">
                  {{ stat.label }}
                </span>
              </div>

              <!-- FG percent -->
              <div v-if="player.fg > 0" class="ml-2 hidden flex-col gap-1 md:flex">
                <span class="text-[11px] font-bold uppercase tracking-wider text-white/40">FG%</span>
                <div class="flex items-center gap-2">
                  <div class="h-1.5 w-20 overflow-hidden rounded-full bg-white/15">
                    <div class="h-full rounded-full transition-all duration-700"
                      :style="{ width: `${player.fg}%`, background: player.accent }" />
                  </div>
                  <span class="text-sm font-bold text-white">{{ player.fg }}%</span>
                </div>
              </div>
            </div>

            <p class="mt-7 text-[16px] text-white/40 md:text-[14px]">
              {{ player.gamesPlayed }} games played this season
            </p>

          </div>
        </div>
      </div>

      <!-- Navigation dots -->
      <div class="absolute bottom-4 left-1/2 flex -translate-x-1/2 items-center gap-2">
        <button v-for="i in scorers.length" :key="i - 1" @click="goTo(i - 1)"
          class="rounded-full transition-all duration-300"
          :class="activeSlide === i - 1
            ? 'h-2 w-6 bg-white'
            : 'h-2 w-2 bg-white/30 hover:bg-white/50'" />
      </div>

      <!-- Arrows -->
      <button @click="prev"
        class="absolute left-3 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-full bg-black/30 text-white backdrop-blur-sm transition hover:bg-black/50 md:left-5">
        <ChevronLeft class="h-5 w-5" />
      </button>
      <button @click="next"
        class="absolute right-3 top-1/2 flex h-9 w-9 -translate-y-1/2 items-center justify-center rounded-full bg-black/30 text-white backdrop-blur-sm transition hover:bg-black/50 md:right-5">
        <ChevronRight class="h-5 w-5" />
      </button>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { fetchPages } from '@/api'

defineEmits(['viewScorers'])

const loading = ref(true)
const scorers = ref([])
const activeSlide = ref(0)
const current = computed(() => scorers.value[activeSlide.value] ?? { bgFrom: '#1e293b', bgTo: '#0f172a', accent: '#00d4aa' })


const PALETTE = [
  { bgFrom: '#1d428a', bgTo: '#0a1428', accent: '#c4a535' },
  { bgFrom: '#00471b', bgTo: '#001a0a', accent: '#eee1c6' },
  { bgFrom: '#007ac1', bgTo: '#003050', accent: '#ef3b24' },
  { bgFrom: '#552583', bgTo: '#1e0a35', accent: '#fdb927' },
  { bgFrom: '#ce1141', bgTo: '#4a0015', accent: '#ffffff' },
]

async function loadTopScorers() {
  try {
    const stats = await fetchPages('player-stats/', 10)

    // Aggregate by player id
    const map = new Map()
    for (const s of stats) {
      const pid = s.player.id
      if (!map.has(pid)) {
        map.set(pid, {
          id: pid,
          name: `${s.player.first_name} ${s.player.last_name}`,
          team: s.player.team?.name ?? '',
          teamShort: s.player.team?.name?.split(' ').pop() ?? '',
          pos: s.player.position?.name ?? '',
          imageUrl: s.player.image_url ?? null,
          initials: `${s.player.first_name[0]}${s.player.last_name[0]}`,
          points: 0, rebounds: 0, assists: 0,
          fgMade: 0, fgAttempted: 0,
          games: 0,
        })
      }
      const p = map.get(pid)
      p.points += s.points ?? 0
      p.rebounds += s.rebounds ?? 0
      p.assists += s.assists ?? 0
      p.fgMade += s.fg_made ?? 0
      p.fgAttempted += s.fg_attempted ?? 0
      p.games++
    }

    // top 5 by avg points
    const top5 = [...map.values()]
      .filter(p => p.games >= 2)
      .sort((a, b) => (b.points / b.games) - (a.points / a.games))
      .slice(0, 5)

    scorers.value = top5.map((p, i) => {
      const colors = PALETTE[i % PALETTE.length]
      const ppg = (p.points / p.games).toFixed(1)
      const rpg = (p.rebounds / p.games).toFixed(1)
      const apg = (p.assists / p.games).toFixed(1)
      const fg = p.fgAttempted > 0
        ? Math.round((p.fgMade / p.fgAttempted) * 100)
        : 0
      return {
        ...p, ...colors,
        gamesPlayed: p.games,
        fg,
        stats: [
          { val: ppg, label: 'PPG' },
          { val: rpg, label: 'RPG' },
          { val: apg, label: 'APG' },
        ],
      }
    })
  } catch (e) {
    console.error('loadTopScorers:', e)
  } finally {
    loading.value = false
  }
}

function goTo(i) { activeSlide.value = i; resetInterval() }
function next() { if (!scorers.value.length) return; activeSlide.value = (activeSlide.value + 1) % scorers.value.length; resetInterval() }
function prev() { if (!scorers.value.length) return; activeSlide.value = (activeSlide.value - 1 + scorers.value.length) % scorers.value.length; resetInterval() }

let interval = null
function resetInterval() { clearInterval(interval); interval = setInterval(next, 6000) }
onMounted(() => { loadTopScorers(); interval = setInterval(next, 6000) })
onUnmounted(() => clearInterval(interval))
</script>
