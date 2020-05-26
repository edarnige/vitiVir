import Vue from "vue";
import VueProgressBar from 'vue-progressbar'
import App from "./App.vue";
import router from './router'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate'
import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue)

import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

import MaterialKit from "./plugins/material-kit";

Vue.config.productionTip = false;

Vue.use(MaterialKit);
Vue.use(Vuex)


const store = new Vuex.Store({
  plugins: [createPersistedState({
    storage: window.sessionStorage, //this means token is visible in session storage...
  })],  
  state: {
    token: null,
    can_verify: false,
    search_q: '?',
    sample:'',
    host_organism:'',
    virus_type:'',
    taxonomy:'',
    description:'',
    verified: '',
    exclude_vitis: '',
    start_date: '',
    end_date: '',
    ordering: ''
  },
  mutations: {
    setToken (state, token) {
      state.token = token
    },
    setVerify(state, can_verify){
      state.can_verify = can_verify //reset at logout
    },
    setSearch(state, search_q){
      state.search_q = search_q
    },
    allQParams(state, {
      sample, host_organism, virus_type, taxonomy, 
      description, verified, exclude_vitis, 
      start_date, end_date, ordering
    }){
      state.sample = sample
      state.host_organism = host_organism
      state.virus_type = virus_type
      state.taxonomy = taxonomy
      state.description = description
      state.verified = verified
      state.exclude_vitis = exclude_vitis
      state.start_date = start_date
      state.end_date = end_date
      state.ordering = ordering
      //page?
    }
  },
  actions: {
    setQParams({commit},{sample, host_organism, virus_type, taxonomy, description, verified, exclude_vitis, start_date, end_date, ordering}){
      commit('allQParams',{sample, host_organism, virus_type, taxonomy, description, verified, exclude_vitis, start_date, end_date, ordering})
    }


  }

})

const NavbarStore = {
  showNavbar: false
};

//Progress bar options
const options = {
  color: '#00a33c',
  failedColor: '#874b4b',
  thickness: '10px',
  transition: {
    speed: '0.2s',
    opacity: '0.6s',
    termination: 300
  },
  autoRevert: true,
  location: 'top',
  inverse: false
}

Vue.use(VueProgressBar, options)

Vue.mixin({
  data() {
    return {
      NavbarStore
    };
  }
});

export default new Vue({
  router,
  store:store,
  render: h => h(App)
}).$mount("#app");
