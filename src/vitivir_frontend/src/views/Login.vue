<template>
  <div class="wrapper">
    <div class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout"> <!-- @submit.prevent="login"> -->
          <div
            class="md-layout-item md-size-33 md-small-size-66 md-xsmall-size-100 md-medium-size-40 mx-auto"
          >

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
              <md-button slot="footer" class="md-simple md-success md-lg" v-on:click="login()"> 
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

export default {
  components: {
    LoginCard
  },
  bodyClass: "login-page",

  data() {
    return {
      email: '',
      password: '',
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
        let token = res.data.token;
        console.log("logged in", res);
        this.$store.commit('setToken',token) //change token value
        this.getUser(this.email)
        this.$router.push('/search');
        //location.reload(); //to show correct navbar buttons...
        console.log(this.$store.state.token)
      })
      .catch(err => {
        console.log(err);
        this.$store.state.token = null;
      })
    },

    getUser(email){
      axios.get("http://0.0.0.0:9000/users/manageusers/"+"?email="+email)
      .then(res=> {
        console.log(res.data.results[0].email,res.data.results[0].can_verify)
        let can_verify = res.data.results[0].can_verify
        this.$store.commit('setVerify', can_verify)
      })

  }

  }
}

</script>

<style lang="css">

</style>
