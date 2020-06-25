<template>
  <div class="wrapper">
    <div class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout">
          <div
            class="md-layout-item md-size-33 md-small-size-66 md-xsmall-size-100 md-medium-size-40 mx-auto"
          >
            <!-- <login-card header-color="primary"> -->
            <!-- <login-card class="md-card-header-primary"> -->
            <login-card>
              <h4 slot="title" class="card-title">Sign up</h4>
              <p slot="description" class="description">A request to create an account will be sent. Check your email for updates.</p>

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
              <md-field class="md-form-group" slot="inputs">
                <!-- <md-icon>face</md-icon> -->
                <label>Confirm password...</label>
                <md-input id="passwordConfirmed" v-model="passwordConfirmed" type="password" required></md-input>
              </md-field>
              <md-button slot="footer" class="md-simple md-primary md-lg" v-on:click="signup"> <!-- redirect to landing -->
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
      passwordConfirmed: '',
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
    signup(){
      //Create account with is_activated = false
      if(this.password == this.passwordConfirmed){
        axios.post(`${process.env.VUE_APP_API_HOST}/users/manageusers/`,{
          email: this.email,
          password: this.password,
        })
        .then(res => {
          console.log("signed up", res),
          this.$router.push('/login')
        })
        .catch(err => console.log(err));
      }
      else{
        console.log("Passwords do not match")
      }

      //Send email to request account, suepruser must switch is_active on 
      const data = {
        'email': this.email,
      }
      axios.post(`${process.env.VUE_APP_API_HOST}/api/request_account/`, data)
      .then(res=>{
        console.log(res)
        alert('Request sent');
      })
      .catch(err =>console.log(err));
      

    },
  }

  };
// };
</script>

<style lang="css"></style>
