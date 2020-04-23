<template>
  <div class="wrapper">
    <div class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout"> <!-- @submit.prevent="login"> -->
          <div
            class="md-layout-item md-size-33 md-small-size-66 md-xsmall-size-100 md-medium-size-40 mx-auto"
          >
            <!-- <login-card header-color="green"> -->
            <login-card>
              <h4 slot="title" class="card-title">Login</h4>
              <p slot="description" class="description"></p>
              <md-field class="md-form-group" slot="inputs">
                <!-- <md-icon>email</md-icon> -->
                <label>Email...</label>
                <md-input id="email" v-model="email" type="email" required></md-input>
              </md-field>
              <md-field class="md-form-group" slot="inputs">
                <!-- <md-icon>lock_outline</md-icon> -->
                <label>Password...</label>
                <md-input id="password" v-model="password" type="password" required></md-input>
              </md-field>
              <md-button slot="footer" class="md-simple md-success md-lg" v-on:click="login"> 
                Login
              </md-button>
              <md-button slot="footer" class="md-simple md-primary md-lg" @click="$router.push('/signup');"> 
                Request account
              </md-button>
            </login-card>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { LoginCard } from "@/components";
import axios from 'axios'; //backend server needs to be running
//import Vue from "vue";

export default {
  components: {
    LoginCard
  },
  bodyClass: "login-page",

  data() {
    return {
      email: '',
      password: '',
      token: localStorage.getItem('user-token') || null,
    };
  },

  props: {
    header: {
      type: String,
      default: require("@/assets/img/vineyard.jpeg")
    }
  },

  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  },

  methods:{
    login(){
      axios.post("http://0.0.0.0:9000/users/login/", {
        username: this.email,
        password: this.password,
      })
      .then(res => {
        this.token = res.data.token;
        console.log("logged in", res);
        localStorage.setItem('user-token', this.token);
        this.$router.push('/search')
        //this.$router.push({path:'/search', header: {'Authorization': 'Token '+ this.token}});
      })
      .catch(err => {
        console.log(err);
        localStorage.removeItem('user-token');
    })
  },

  }
}

</script>

<style lang="css">

</style>
