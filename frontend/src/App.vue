<template>
  <div class="flex min-h-screen flex-col bg-[#111827]">
    <AppHeader />
    <div class="flex-1">
      <RouterView />
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import { useScoresStore } from '@/stores/scores'
import { useAuth } from '@/composables/useAuth'

const store = useScoresStore()
const { loadUser } = useAuth()

onMounted(async () => {
  await loadUser()
  store.init()
})
</script>
