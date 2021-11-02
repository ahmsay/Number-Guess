import DefaultLayout from '~/layouts/Default.vue'
import Vuetify from 'vuetify'
import "vuetify/dist/vuetify.min.css"

export default function (Vue, { appOptions }) {
  // Set default layout as a global component
  Vue.use(Vuetify);
  appOptions.vuetify = new Vuetify({
    theme: {
      themes: {
        dark: {
          background: '#35495e',
          card: '#48627c'
        }
      }
    }
  });
  Vue.component('Layout', DefaultLayout);
}