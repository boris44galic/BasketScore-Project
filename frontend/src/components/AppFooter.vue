<template>
  <footer class="mt-auto border-t border-[#1e293b] bg-[#0f172a]">
    <div class="mx-auto w-full max-w-[1280px] px-4 py-10 sm:px-6 md:px-8">

      <div class="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">

        <!-- Brand -->
        <div class="flex flex-col items-center gap-3 sm:items-start">
          <RouterLink to="/" class="flex items-center gap-2.5">
            <span class="text-3xl">🏀</span>
            <span class="text-xl font-extrabold tracking-tight text-white">BasketScore</span>
          </RouterLink>
          <p class="text-center text-[13px] leading-relaxed text-[#64748b] sm:text-left">
            Live scores, standings and stats for basketball leagues— all in one place.
          </p>
        </div>

        <!-- Navigation -->
        <div class="flex flex-col items-center gap-3 sm:items-start">
          <h3 class="text-[11px] font-bold uppercase tracking-widest text-[#64748b]">Navigation</h3>
          <RouterLink to="/"
            class="text-[14px] text-[#94a3b8] transition-colors hover:text-[#00d4aa]">
            Scores
          </RouterLink>
          <RouterLink to="/standings"
            class="text-[14px] text-[#94a3b8] transition-colors hover:text-[#00d4aa]">
            Standings
          </RouterLink>
          <RouterLink to="/favourites"
            class="text-[14px] text-[#94a3b8] transition-colors hover:text-[#00d4aa]">
            Favourites
          </RouterLink>
        </div>

        <!-- Leagues -->
        <div class="flex flex-col items-center gap-3 sm:items-start">
          <h3 class="text-[11px] font-bold uppercase tracking-widest text-[#64748b]">Leagues</h3>
          <button
            v-for="league in quickLeagues" :key="league.id"
            @click="selectLeague(league.id)"
            class="flex items-center gap-2 text-[14px] text-[#94a3b8] transition-colors hover:text-[#00d4aa] cursor-pointer">
            <img v-if="league.logo" :src="league.logo" :alt="league.name"
              class="h-5 w-5 object-contain" />
            <span>{{ league.name }}</span>
          </button>
        </div>

        <!-- Support -->
        <div class="flex flex-col items-center gap-3 sm:items-start">
          <h3 class="text-[11px] font-bold uppercase tracking-widest text-[#64748b]">Support</h3>
          <a href="mailto:support@basketscore.com"
            class="text-[14px] text-[#94a3b8] transition-colors hover:text-[#00d4aa]">
            Contact us
          </a>
          <RouterLink to="/profile"
            class="text-[14px] text-[#94a3b8] transition-colors hover:text-[#00d4aa]">
            My account
          </RouterLink>
        </div>
      </div>

      <!-- Bottom bar -->
      <div class="mt-8 flex flex-col items-center justify-between gap-3 border-t border-[#1e293b] pt-6 sm:flex-row">
        <p class="text-[12px] text-[#475569]">
          &copy; {{ year }} BasketScore. All rights reserved.
        </p>
        <p class="text-[12px] text-[#334155]">
          Data updated in real time &middot; NBA &middot; EuroLeague
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useScoresStore } from '@/stores/scores'

const store = useScoresStore()
const router = useRouter()

const year = new Date().getFullYear()

const quickLeagues = computed(() =>
  store.leagues.map(l => ({
    id: String(l.id),
    name: l.name,
    logo: l.logo ?? null,
  }))
)

function selectLeague(id) {
  store.activeLeague = id
  router.push('/')
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>
