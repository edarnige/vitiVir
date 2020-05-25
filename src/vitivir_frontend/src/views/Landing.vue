<template>
  <div class="wrapper">
    <parallax class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout">
          <div
            class="md-layout-item md-size-50 md-small-size-70 md-xsmall-size-100"
          >
            <h1 class="title">VitiVir Database</h1>
            <h4 id="subtitle">
              A web mining tool to analyze the phytovirus and mycovirus diversity of grapevine. 
              Login to access the search utility.
            </h4>
            <br />
            <md-button
              class="md-primary md-lg"
              @click="canSearch()"
              >Search</md-button>
            <p id="photo-cred">
            Photo by Dario Krejci
            </p>
          </div>
        </div>
      </div>
    </parallax>
    <div class="main main-raised">
      <div class="section">
        <div class="container">
          <div class="md-layout">
            <div
              class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto text-center"
            >
              <h2 class="title text-center">About the database</h2>
              <h5 class="description">
                Data from NCBI's publically available SRA as well as data from project InViCeb 
                were analyzed via the VirAnnot pipeline, and the results can be explored here. 
                VirAnnot was developped by Marie Lefebvre and Sebastian Thiel within the plant virology etiology team. VirAnnot is a bioinformatic 
                resource for the automatic classification of viral OTUs. Mycovir... INVICEB...
              </h5>
            </div>
          </div>
          <div class="features text-center">
            <div class="md-layout">
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                  <i class="fas fa-viruses"></i>
                  <h4 class="info-title">Virus data</h4>
                  <p>
                    All kinds of viruses phyto myco phage. viri viruses virus
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                    <i class="fas fa-user-check"></i>
                  <h4 class="info-title">Verified Users</h4>
                  <p>
                    Database access is restricted to INRAE UMR 1332 researchers 
                    and MYCOVIR partners. Only MYCOVIR project directors can verify
                    taxonomy, host organism, and virus type. 
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                  <i class="fas fa-file-upload"></i>
                  <h4 class="info-title">BLASTX portal</h4>
                  <p>
                    Upload a fasta file to undergo BLASTX....
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="section section-contacts">
        <div class="container">
          <div class="md-layout">
            <div class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto">
              <h2 class="text-center title">Contact</h2>
              <h4 class="text-center description">
                Feel free to reach out with any comments or questions. We will get back 
                to you as soon as possible.
              </h4>
              <form class="contact-form">
                <div class="md-layout">
                  <div class="md-layout-item md-size-50">
                    <md-field>
                      <label>Your Name</label>
                      <md-input v-model="name" type="text"></md-input>
                    </md-field>
                  </div>
                  <div class="md-layout-item md-size-50">
                    <md-field>
                      <label>Your Email</label>
                      <md-input v-model="email" type="email"></md-input>
                    </md-field>
                  </div>
                </div>
                <md-field maxlength="5">
                  <label>Your Message</label>
                  <md-textarea v-model="message"></md-textarea>
                </md-field>
                <div class="md-layout">
                  <div class="md-layout-item md-size-33 mx-auto text-center">
                    <md-button class="md-primary">Send Message</md-button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  bodyClass: "landing-page",
  props: {
    header: {
      type: String,
      default: require("@/assets/img/vineyard.jpeg")
    },
    teamImg1: {
      type: String,
      default: require("@/assets/img/faces/avatar.jpg")
    },
    teamImg2: {
      type: String,
      default: require("@/assets/img/faces/christian.jpg")
    },
    teamImg3: {
      type: String,
      default: require("@/assets/img/faces/kendall.jpg")
    }
  },

  data() {
    return {
      name: null,
      email: null,
      message: null,
    };
  },

  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  },

  methods: {
    canSearch(){
      if(this.$store.state.token != null){
        this.$router.push('/search')
      }
      else{
        this.$router.push('/login')
      }
    },
  }
};
</script>

<style lang="scss" scoped>
.md-card-actions.text-center {
  display: flex;
  justify-content: center !important;
}
.contact-form {
  margin-top: 30px;
}
.md-has-textarea + .md-layout {
  margin-top: 15px;
}
.fa-viruses{
  color: #f57c00;
  font-size: 3em;
}
.fa-user-check{
  color: #4caf50;
  font-size: 3em;
}
.fa-file-upload{
  color: #2196f3;
  font-size: 3em;
}
#subtitle{
  font-weight: bold;
  text-shadow: 2px 2px 3px rgba(0,0,0,0.3);
}
#photo-cred{
  padding-top:30px;
  font-size: 0.5em;
}

</style>
