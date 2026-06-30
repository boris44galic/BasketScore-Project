<template>
  <div class="mb-3 overflow-hidden rounded-xl border border-[#1e293b] bg-[#111827]">
    <div
      class="flex cursor-pointer items-center gap-3 bg-[#0f172a] px-4 py-2.5 transition hover:bg-[#1a2332]"
      @click="collapsed = !collapsed">

      <div class="flex h-7 w-7 shrink-0 items-center justify-center overflow-hidden rounded-lg bg-[#1e293b]">
        <img v-if="group.leagueLogo" :src="group.leagueLogo" :alt="group.league"
          class="h-5 w-5 object-contain" @error="(e) => e.target.style.display='none'" />
        <span v-else class="text-base">{{ group.leagueFlag }}</span>
      </div>

      <div class="flex min-w-0 flex-1 flex-col">
        <!--  <span class="text-xs font-medium uppercase tracking-wider text-[#64748b]">{{ group.leagueCountry }}</span>
-->
        <span class="truncate text-sm font-semibold text-[#f1f5f9]">{{ group.league }}</span>
      </div>

      <div class="flex shrink-0 items-center gap-2">
        <RouterLink
          :to="`/standings?league=${group.leagueId}`"
          @click.stop
          class="text-xs font-medium text-[#00d4aa] transition hover:text-[#00bfa0]">
          Table
        </RouterLink>
        <ChevronDown
          class="h-4 w-4 text-[#64748b] transition-transform duration-200"
          :class="collapsed ? 'rotate-180' : ''" />
      </div>
    </div>

    <Transition name="collapse">
      <div v-if="!collapsed">
        <MatchRow v-for="match in group.matches" :key="match.id" :match="match" />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import MatchRow from './MatchRow.vue'

defineProps({ group: Object })
const collapsed = ref(false)
</script>

<style scoped>
.collapse-enter-active,
.collapse-leave-active { transition: opacity 0.15s ease; }
.collapse-enter-from,
.collapse-leave-to { opacity: 0; }
</style>
