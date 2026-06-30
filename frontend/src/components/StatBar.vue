<template>
  <div class="py-2.5">
    <span class="mb-1 block text-center text-[12.5px] font-semibold uppercase tracking-wider text-white">{{ label }}</span>
    <div class="flex items-center gap-2">
      <span class="w-8 shrink-0 text-right text-sm font-bold text-white mr-2">{{ home }}</span>
      <div class="flex flex-1 h-1.5 overflow-hidden rounded-full">
        <div class="h-full rounded-l-full bg-[#00d4aa] transition-all duration-500" :style="{ width: homePercent + '%' }" />
        <div class="h-full rounded-r-full bg-[#ef4444] transition-all duration-500" :style="{ width: awayPercent + '%' }" />
      </div>
      <span class="w-8 shrink-0 text-left text-sm font-bold text-white ml-2">{{ away }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({ home: Number, away: Number, label: String })

const total = computed(() => (props.home || 0) + (props.away || 0))
const homePercent = computed(() => total.value ? ((props.home / total.value) * 100) : 50)
const awayPercent = computed(() => 100 - homePercent.value)
</script>
