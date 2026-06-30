<template>
  <div class="overflow-hidden rounded-xl border border-[#1e293b] bg-[#111827]">
    <!-- Header -->
    <div class="flex items-center gap-3 bg-[#0f172a] px-6 py-4">
      <img v-if="leagueLogo" :src="leagueLogo" :alt="leagueName" class="h-8 w-8 object-contain"
        @error="(e) => e.target.style.display='none'" />
      <span class="text-lg font-bold text-[#f1f5f9]">{{ leagueName }}</span>
    </div>

    <!-- Scrollable table area -->
    <div class="overflow-x-auto">
      <!-- Column labels -->
      <div class="grid grid-cols-[auto_1fr_repeat(4,auto)] gap-x-4 border-t border-[#1e293b] bg-[#0f172a]/50 px-4 py-3 min-w-85 sm:px-6">
        <span class="w-7 text-center text-[12px] font-semibold uppercase tracking-wider text-[#f1f5f9]">#</span>
        <span class="text-[12px] font-semibold uppercase tracking-wider text-[#f1f5f9]">Team</span>
        <span class="w-10 text-center text-[12px] font-semibold uppercase tracking-wider text-[#f1f5f9]">GP</span>
        <span class="w-10 text-center text-[12px] font-semibold uppercase tracking-wider text-[#f1f5f9]">W</span>
        <span class="w-10 text-center text-[12px] font-semibold uppercase tracking-wider text-[#f1f5f9]">L</span>
        <span class="w-16 text-center text-[12px] font-semibold uppercase tracking-wider text-[#f1f5f9]">Win%</span>
      </div>

      <!-- Rows -->
      <div
        v-for="row in rows" :key="row.pos"
        @click="router.push(`/team/${row.id}`)"
        class="grid grid-cols-[auto_1fr_repeat(4,auto)] items-center gap-x-4 border-t border-[#1e293b]/60 px-4 py-3.5 transition hover:bg-[#1e293b]/40 min-w-85 sm:px-6 cursor-pointer">
        <span class="flex h-7 w-7 items-center justify-center rounded-[5px] text-[13px] font-bold" :class="posClass(row.pos)">{{ row.pos }}.</span>

        <div class="flex min-w-0 items-center gap-2 sm:gap-3">
          <img v-if="row.logo" :src="row.logo" :alt="row.name" class="h-6 w-6 sm:h-8 sm:w-8 shrink-0 object-contain"
            @error="(e) => e.target.style.display='none'" />
          <span class="truncate text-[14px] sm:text-[15px] font-medium text-[#f1f5f9]">{{ row.name }}</span>
        </div>

        <span class="w-10 text-center text-[14px] font-bold text-[#f1f5f9]">{{ row.p }}</span>
        <span class="w-10 text-center text-[14px] font-bold text-[#f1f5f9]">{{ row.w }}</span>
        <span class="w-10 text-center text-[14px] font-bold text-[#f1f5f9]">{{ row.l }}</span>
        <span class="w-16 text-center text-[15px] font-bold text-[#f1f5f9]">{{ row.pct }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps({
  rows: { type: Array, default: () => [] },
  leagueName: { type: String, default: '' },
  leagueLogo: { type: String, default: null },
})


function posClass(pos) {
  if (pos <= 8) return 'bg-[#00d4aa] text-[#0f172a]'
  if (pos <= 12) return 'bg-[#00d4aa]/25 text-[#00d4aa]'
  return 'text-[#fff]'
}
</script>
