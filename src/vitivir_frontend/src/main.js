import Vue from "vue";
import App from "./App.vue";
import router from './router'
import BootstrapVue from "bootstrap-vue";

import '@fortawesome/fontawesome-free/css/all.css'
import '@fortawesome/fontawesome-free/js/all.js'

import MaterialKit from "./plugins/material-kit";
// import 'vue-material-design-icons/styles.css';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);

Vue.use(MaterialKit);



import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-vue/dist/bootstrap-vue.css"


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
  render: h => h(App)
}).$mount("#app");
