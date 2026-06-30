import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import MatchDetailView from '@/views/MatchDetailView.vue'
import StandingsView from '@/views/StandingsView.vue'
import { useAuth } from '@/composables/useAuth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomeView },
    { path: '/match/:id', component: MatchDetailView },
    { path: '/player/:id', component: () => import('@/views/PlayerDetailView.vue') },
    { path: '/team/:id', component: () => import('@/views/TeamDetailView.vue') },
    { path: '/standings', component: StandingsView },
    {
      path: '/profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/favourites',
      component: () => import('@/views/FavouritesView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/admin',
      component: () => import('@/views/AdminPanelView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
    },
  ],
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach(async (to) => {
  const hasToken = !!localStorage.getItem('access')
  if (to.meta.requiresAuth && !hasToken) return { path: '/' }
  if (to.meta.requiresAdmin) {
    const { isAdmin, user, loadUser } = useAuth()
    if (!user.value) await loadUser()
    if (!isAdmin.value) return { path: '/' }
  }
  return true
})

export default router
