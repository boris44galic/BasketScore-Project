<template>
  <RouterLink
    :to="`/match/${match.id}`"
    class="group flex cursor-pointer items-center gap-4 border-b border-[#1e293b]/60 px-4 py-3.5 transition-colors hover:bg-[#1e293b] last:border-0">

    <!-- Time / Status -->
    <div class="w-16 shrink-0 text-center">
      <template v-if="match.status === 'live'">
        <span class="inline-flex items-center justify-center gap-1 text-sm font-bold text-[#ef4444]">
          <span class="h-2 w-2 shrink-0 animate-pulse rounded-full bg-[#ef4444] mr-1" />
          {{ match.quarter ? `${match.quarter} ${match.clock}` : 'LIVE' }}
        </span>
      </template>
      <template v-else-if="match.status === 'finished'">
        <span class="text-sm font-medium text-[#64748b]">Final</span>
      </template>
      <template v-else-if="match.status === 'postponed'">
        <span class="text-sm font-medium text-[#ef4444]">PST</span>
      </template>
      <template v-else>
        <span class="text-sm font-medium text-[#94a3b8]">{{ match.time }}</span>
      </template>
    </div>

    <!-- Teams -->
    <div class="flex min-w-0 flex-1 flex-col gap-1">
      <!-- Home -->
      <div class="flex items-center justify-between gap-2">
        <div class="flex min-w-0 items-center gap-2.5">
          <div class="flex h-7 w-7 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#1e293b]">
            <img v-if="match.homeTeamLogo" :src="match.homeTeamLogo" :alt="match.homeTeam"
              class="h-6 w-6 object-contain" @error="(e) => e.target.style.display='none'" />
          </div>
          <span class="truncate text-[15px]"
            :class="isHomeWinner ? 'font-semibold text-[#f1f5f9]' : 'text-[#94a3b8]'">
            {{ match.homeTeam }}
          </span>
        </div>
        <span class="w-10 shrink-0 text-right text-[15px] font-bold tabular-nums"
          :class="scoreClass('home')">
          {{ match.homeScore ?? '' }}
        </span>
      </div>

      <!-- Away -->
      <div class="flex items-center justify-between gap-2">
        <div class="flex min-w-0 items-center gap-2.5">
          <div class="flex h-7 w-7 shrink-0 items-center justify-center overflow-hidden rounded-full bg-[#1e293b]">
            <img v-if="match.awayTeamLogo" :src="match.awayTeamLogo" :alt="match.awayTeam"
              class="h-6 w-6 object-contain" @error="(e) => e.target.style.display='none'" />
          </div>
          <span class="truncate text-[15px]"
            :class="isAwayWinner ? 'font-semibold text-[#f1f5f9]' : 'text-[#94a3b8]'">
            {{ match.awayTeam }}
          </span>
        </div>
        <span class="w-10 shrink-0 text-right text-[15px] font-bold tabular-nums"
          :class="scoreClass('away')">
          {{ match.awayScore ?? '' }}
        </span>
      </div>
    </div>

    <ChevronRight class="h-4 w-4 shrink-0 text-[#334155] transition group-hover:text-[#64748b]" />
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronRight } from 'lucide-vue-next'

const props = defineProps({ match: Object })

const isFinished = computed(() => props.match.status === 'finished')

const isHomeWinner = computed(() =>
  isFinished.value &&
  props.match.homeScore !== null && props.match.awayScore !== null &&
  props.match.homeScore > props.match.awayScore
)
const isAwayWinner = computed(() =>
  isFinished.value &&
  props.match.homeScore !== null && props.match.awayScore !== null &&
  props.match.awayScore > props.match.homeScore
)

function scoreClass(side) {
  if (props.match.status === 'live') return 'text-[#ef4444]'
  if (isFinished.value) {
    if (side === 'home') return isHomeWinner.value ? 'text-[#f1f5f9]' : 'text-[#64748b]'
    if (side === 'away') return isAwayWinner.value ? 'text-[#f1f5f9]' : 'text-[#64748b]'
  }
  return 'text-[#94a3b8]'
}
</script>
