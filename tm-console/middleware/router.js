import { $axios } from '~/utils/api';
export default async ({ store, route, redirect }) => {
  console.log(route)
  if (route.name !== 'login' && route.name !== 'bad-connection') {
    try {
      const response = await $axios.get('/api/user/auth/')
    } catch (error) {
      redirect('login')
    }
  }
}