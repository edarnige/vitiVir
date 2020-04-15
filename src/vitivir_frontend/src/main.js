import Vue from "vue";
import App from "./App.vue";
import router from './router'
import BootstrapVue from "bootstrap-vue";

import MaterialKit from "./plugins/material-kit";

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
