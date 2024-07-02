import './assets/main.css'
import '../node_modules/primeflex/primeflex.scss';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import axios from 'axios'
import VueAxios from 'vue-axios'

import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';

import App from './App.vue'
import router from './router'

import { createYmaps } from 'vue-yandex-maps';

import HighchartsVue from 'highcharts-vue';

import Menubar from 'primevue/menubar';
import 'primeicons/primeicons.css'

import ToastService from 'primevue/toastservice';

// import loadDataPlugin from './plugins/loadData'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueAxios, axios)
app.provide('axios', app.config.globalProperties.axios)  // provide 'axios'

app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});

app.use(HighchartsVue)
app.use(ToastService);

app.use(createYmaps({
    apikey: '8cfd01cf-5ac2-4cc0-baa5-ea9e5af226da',
  }));

// app.use('loadDataPlugin', loadDataPlugin)

app.component('app-menubar', Menubar)

app.mount('#app')
