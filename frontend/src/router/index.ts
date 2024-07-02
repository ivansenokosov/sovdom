import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import { useUserStore } from '@/stores/user'

const checkAuth = (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
  const userStore = useUserStore()
  if (!userStore.userId) {
    next({name: 'auth'}) // Если пользователь не авторизован, то отправляеи на страницу авторизации
  } else {
    next() // Пусть идёт, куда хотел
  }
}


const routes : RouteRecordRaw [] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue')
  },
  {
    path: '/achievements',
    name: 'achievements',
    component: () => import('@/views/ListAchievements.vue')
  },
  {
    path: '/auth',
    name: 'auth',
    component: () => import('@/views/AuthView.vue')
  },
  {
    path: '/add_achievement',
    name: 'add_achievement',
    component: () => import('@/views/CreateAchievements.vue'),
  },
  {
    path: '/edit_achievement/:id',
    name: 'edit_achievement',
    component: () => import('@/views/EditAchievement.vue'),
    props: true,
  },
  {
    path: '/delete_achievement/:id',
    name: 'delete_achievement',
    component: () => import('@/views/DeleteAchievement.vue'),
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes
})

export default router
