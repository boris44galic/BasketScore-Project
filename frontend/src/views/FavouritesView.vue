<template>
  <div class="mx-auto max-w-[1280px] px-4 py-10 sm:px-6 md:px-8">
    <h1 class="mb-8 text-2xl font-extrabold text-[#f1f5f9]">Favourite Teams</h1>

    <!-- Loading -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 3" :key="i" class="h-40 animate-pulse rounded-2xl bg-[#1e293b]" />
    </div>

    <!-- Empty state -->
    <div v-else-if="!favouriteTeams.length"
      class="flex flex-col items-center justify-center rounded-2xl border border-[#1e293b] bg-[#0f172a] py-20 text-center">
      <div class="mb-4 text-5xl">❤️</div>
      <p class="text-[18px] font-semibold text-white">No favourite teams yet</p>
      <p class="mt-1 text-[16px] text-[#475569]">Track your favourite teams and never miss a match!</p>
      <RouterLink to="/"
        class="mt-6 rounded-full bg-[#1e293b] px-9 py-4.5 text-[14px] font-bold text-white transition hover:bg-[#00bfa0] hover:text-[#0f172a]">
        Browse matches
      </RouterLink>
    </div>

    <!-- Team sections -->
    <div v-else class="space-y-10">
      <section v-for="fav in favouriteTeams" :key="fav.team.id">

        <!-- Team header -->
        <div class="mb-3 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center overflow-hidden rounded-full bg-[#1e293b]">
              <img v-if="fav.team.logo" :src="fav.team.logo" :alt="fav.team.name"
                class="h-8 w-8 object-contain" @error="(e) => e.target.style.display='none'" />
              <span v-else class="text-lg">🏀</span>
            </div>
            <span class="text-lg font-extrabold text-[#f1f5f9]">{{ fav.team.name }}</span>
          </div>
          <button @click="unfollow(fav.team.id)"
            class="flex cursor-pointer items-center gap-1.5 rounded-full border border-[#334155] px-3 py-1.5 text-xs font-semibold text-red-400 transition hover:border-red-500/40 hover:bg-red-500/10">
            <Heart class="h-5.5 w-5.5 fill-red-500" />
            Unfollow
          </button>
        </div>

        <!-- Matches for this team -->
        <div v-if="matchesForTeam(fav.team.id).length"
          class="overflow-hidden rounded-xl border border-[#1e293b] bg-[#111827]">
          <MatchRow v-for="match in matchesForTeam(fav.team.id)" :key="match.id" :match="match" />
        </div>
        <div v-else
          class="rounded-xl border border-[#1e293b] bg-[#0f172a] px-6 py-8 text-center text-[13px] text-[#64748b]">
          No matches found for {{ fav.team.name }}
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Heart } from 'lucide-vue-next'
import { useScoresStore } from '@/stores/scores'
import { useFavourites } from '@/composables/useFavourites'
import MatchRow from '@/components/MatchRow.vue'

const store = useScoresStore()
const { favouriteTeams, loadFavourites, toggle } = useFavourites()

const loading = ref(true)

function matchesForTeam(teamId) {
  return store.matches.filter(
    m => m.homeTeamId === teamId || m.awayTeamId === teamId
  )
}

async function unfollow(teamId) {
  await toggle(teamId)
}

onMounted(async () => {
  if (!store.matches.length) await store.fetchMatches()
  await loadFavourites()
  loading.value = false
})
</script>
