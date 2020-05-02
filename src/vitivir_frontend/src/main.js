import Vue from "vue";
import App from "./App.vue";
import router from './router'
import Vuex from 'vuex'
//import BootstrapVue from "bootstrap-vue";

import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

import MaterialKit from "./plugins/material-kit";

Vue.config.productionTip = false;

Vue.use(MaterialKit);
Vue.use(Vuex)


const store = new Vuex.Store({
  state: {
    token: null,
  },
  mutations: {
    setToken (state, token) {
      state.token = token
    }
  }
})

const NavbarStore = {
  showNavbar: false
};

Vue.mixin({
  data() {
    return {
      NavbarStore
    };
  }
});

new Vue({
  router,
  store:store,
  render: h => h(App)
}).$mount("#app");
