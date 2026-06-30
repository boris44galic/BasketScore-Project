<template>
  <!-- Hero sections -->
  <HeroSearch />
  <HeroCarousel class="mb-4" />

  <div class="mx-auto max-w-7xl px-4 pb-8 md:px-8">
    <div class="flex gap-6">

      <!-- Main content -->
      <div class="min-w-0 flex-1">
        <!-- Date strip 
        <div class="scrollbar-hide mb-4 flex items-center gap-1 overflow-x-auto">
          <button
            v-for="d in dateStrip" :key="d.key"
            @click="activeDate = d.key"
            class="flex shrink-0 flex-col items-center rounded-lg px-3 py-2 text-xs font-semibold transition"
            :class="activeDate === d.key
              ? 'border border-[#00d4aa]/30 bg-[#00d4aa]/10 text-[#00d4aa]'
              : 'text-[#64748b] hover:bg-[#1e293b] hover:text-[#94a3b8]'">
            <span class="text-[10px] uppercase">{{ d.day }}</span>
            <span class="text-base font-bold">{{ d.date }}</span>
          </button>
        </div>
        -->

        <!-- Match count -->
        <div class="mb-3 flex items-center justify-between">
          <span class="text-xs font-semibold text-[#64748b] uppercase tracking-wider">
            {{ store.groupedMatches.reduce((a, g) => a + g.matches.length, 0) }} matches
          </span>
        </div>

        <!-- Match list -->
        <template v-if="allMatches.length">
          <div class="overflow-hidden rounded-xl border border-[#1e293b] bg-[#111827]">
            <MatchRow v-for="match in allMatches" :key="match.id" :match="match" />
          </div>
        </template>
        <div v-else class="py-16 text-center text-[#64748b]">
          <div class="mb-3 text-4xl">🏀</div>
          <p class="text-lg font-semibold text-[#94a3b8]">No matches found</p>
          <p class="mt-1 text-sm">Try a different filter or league</p>
        </div>
      </div>

      <!-- Right sidebar -->
      <aside class="hidden w-68 shrink-0 lg:block pt-7">
        <div class="sticky top-24">

          <!-- Today's highlights -->
          <div class="overflow-hidden rounded-xl border border-[#1e293b] bg-[#111827]">
            <div class="bg-[#0f172a] px-4 py-3">
              <span class="text-sm font-bold text-[#f1f5f9]">Today's Highlights</span>
            </div>
            <div
              v-for="(h, i) in highlights" :key="i"
              class="flex cursor-pointer items-center gap-3 border-t border-[#1e293b]/60 px-4 py-3 transition hover:bg-[#1e293b]/40">
              <span class="text-xl">{{ h.icon }}</span>
              <div class="min-w-0 flex-1">
                <p class="truncate text-xs font-semibold text-[#f1f5f9]">{{ h.title }}</p>
                <p class="text-xs text-[#64748b]">{{ h.subtitle }}</p>
              </div>
            </div>
          </div>

        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useScoresStore } from '@/stores/scores'
import MatchRow from '@/components/MatchRow.vue'
import HeroSearch from '@/components/HeroSearch.vue'
import HeroCarousel from '@/components/HeroCarousel.vue'

const store = useScoresStore()
const activeDate = ref('today')

const allMatches = computed(() =>
  store.groupedMatches.flatMap(g => g.matches)
)

const today = new Date()
const dateStrip = computed(() => {
  const days = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
  const result = []
  for (let i = -3; i <= 3; i++) {
    const d = new Date(today)
    d.setDate(d.getDate() + i)
    result.push({
      key: i === 0 ? 'today' : d.toISOString().split('T')[0],
      day: i === 0 ? 'TODAY' : days[d.getDay()],
      date: d.getDate(),
    })
  }
  return result
})

const highlights = [
  { icon: '🏀', title: "Dončić drops 50-pt triple-double", subtitle: 'Dallas 128 – 112 LA Lakers · NBA' },
  { icon: '💥', title: "Jokić wins MVP again",             subtitle: 'Third consecutive MVP award' },
  { icon: '🏆', title: "Celtics dominate East",            subtitle: 'Boston 55-15 · Best record in NBA' },
  { icon: '🌍', title: "Real Madrid clinch EuroLeague top", subtitle: 'R. Madrid 78 – 75 CSKA · Q4 final' },
]
</script>

<style scoped>
.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }
</style>
