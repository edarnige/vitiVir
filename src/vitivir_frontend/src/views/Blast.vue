<template>
<div class="wrapper">
  <div>
    <b-container id="blast" v-if="$store.state.token"><!-- <b-container v-if="authenticated"> -->
        <div class="row">
            <div class="col">
                <h2>Search by Blast</h2>
                <h4>Run your query against VitiVir sequences</h4>
                <div role="tablist">
                    <b-card no-body class="text-left mb-1">
                    <b-card-header id="header" header-tag="header" class="p-1" role="tab">
                        <b-btn class="form-header" v-b-toggle.form-panel block variant="success" >Blast form</b-btn>
                    </b-card-header>
                    <b-collapse
                        id="form-panel"
                        v-model="showForm"
                        visible
                        accordion="form-accordion"
                        role="tabpanel"
                    >
                        <b-form @submit="onSubmit" @reset="onReset">
                        <b-row>
                            <b-col >
                            <b-card bg-variant="light">
                                <blast-form
                                ref="blast-form"
                                :default-program="form.program"
                                :default-evalue="form.evalue"
                                :default-max-nb-alignments="form.maxNbAlignments"
                                :default-sequences="form.sequences"
                                ></blast-form>

                                <b-button class="submit-button" variant="outline-primary" size="sm" @click="setExample"
                                >Example</b-button
                                >
                                <b-button class="submit-button" type="submit" variant="primary">Blast</b-button>
                                <b-button class="submit-button" type="reset" variant="danger">Reset</b-button>
                                <b-alert
                                dismissible
                                :show="dismissCountDown"
                                :variant="variant"
                                @dismissed="dismissCountDown = 0"
                                @dismiss-count-down="countDownChanged"
                                >{{ errorMessage }}</b-alert
                                >
                            </b-card>
                            </b-col>
                        </b-row>
                        </b-form>
                    </b-collapse>
                    </b-card>
                    <b-card  v-if="urlBlastResult" no-body class="text-left mb-1"> <!-- remove v-if to see -->
                    <b-card-header header-tag="header" class="p-1" role="tab">
                        <b-btn class="form-header" v-b-toggle.res-panel block variant="success">Results</b-btn>
                    </b-card-header>
                    <b-collapse id="res-panel" v-model="showRes" accordion="res-accordion" role="tabpanel">
                        <blast-result
                        :url-result="urlBlastResult"
                        :res="res"
                        ></blast-result>
                    </b-collapse>
                    </b-card>
                </div>
            </div>
        </div>
    </b-container>
    <b-alert class="alert" v-else show variant="danger">You must be logged in to access the blast function</b-alert>
  </div>
</div> 
</template>

<script>
import axios from 'axios';
import BlastResult from '@/views/components/blast/BlastResult.vue';
import BlastForm from '@/views/components/blast/BlastForm.vue';

export default {
  name: 'Blast',
  components: {
    BlastResult,
    BlastForm,
  },
  props: {
    header: {
      type: String,
      default: require("@/assets/img/vineyard.jpeg")
      }
   },
  data() {
    return {
      showExample: false,
      res: '', // TODO : à enlever
      showForm: true,
      form: {
        program: 'blastn',
        evalue: 1e-10,
        maxNbAlignments: null,
        sequences: '',
        //speciesIds: '',
      },
      example: {
        program: 'blastn',
        evalue: 1e-10,
        maxNbAlignments: null,
        sequences: `>test sequence 1
GGCTAAGACCATAACTCCATTAACTATCGGCTTGGGCA
TTGGACTGGTTCTACACTTCTTGAGAAAGTCTAATCTG
CCATATTCAGGTGACAATATTCATCAGTTTCCACACGG
AGGGCATTATAGGGACGGCACAAAGAGTATAACCTATT
GTGGTCCTAGGCAGTCATTCCCAAGTTCAGGGATATTT
GGTCAGTCA
>test sequence 2
GGCTAAGACCATAACTCCATTAACTATCGGCTTGGGCA
TTGGACTGGTTCTACACTTCTTGAGAAAGTCTAATCTG
CCATATTCAGGTGACAATATTCACCAGTTTCCACACGG
AGGGCATTATAGGGACGGCACAAAGAGTATAACCTATT
GTGGTCCTAGGCA
`,
      },

      programs: [
        { text: 'blastn', value: 'blastn' }, 
        { text: 'tblastn', value: 'tblastn' }, 
        { text: 'tblastx', value: 'tblastx' }, 
      ],
      urlBlastResult: '',
      errorMessage: 'Error',
      variant: 'danger',
      dismissSecs: 3,
      dismissCountDown: 0,
    };
  },

  computed: {
    showRes: {
      get: function() {
        return !this.showForm;
      },
      set: function(newValue) {
        this.showForm = !newValue;
      },
    },
    authenticated: function() {
      return this.$store.getters.isLoggedIn;
    },
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert() {
      this.dismissCountDown = this.dismissSecs;
    },
    onSubmit(event) {

        console.log(process.env.VUE_APP_API_HOST, process.env) //testing environment
      event.preventDefault();

      let blastForm = this.$refs['blast-form'].form;

      if (this.$refs['blast-form'].isValid()) {
        let finalForm = Object.assign({}, blastForm);
        // finalForm.login = this.$store.getters.getLogin;
        // finalForm.token = this.$store.getters.getToken;

        /*let loader = this.$loading.show({
          // Optional parameters
          container: null,
          canCancel: false,
          loader: 'dots',
        });*/
        axios.post("http://0.0.0.0:9000/api/blast/", finalForm,{//`${process.env.VUE_APP_API_HOST}/api/blast/`
            headers: {
                'Authorization': 'Token ' + this.$store.state.token
            }
            })
            .then( 
          // eslint-disable-next-line arrow-parens
          
          resp => {
            const xml = resp.data;
            console.log(xml)
            const success = true;
            
            if (success === false) {
              this.errorMessage = resp.body.message;
              this.showAlert();
            } else {
              //this.urlBlastResult = resp.body.url; //get xml url? 
              this.urlBlastResult = 'http://google.com' //why are we using this?
              // TODO : à enlever
              this.res = xml;
              if (resp.data=== undefined || resp.data === '') { //I use the xml so it's never empty...
                this.errorMessage = 'No result';
                this.showAlert();
              } else {
                this.showForm = false;
              }
            }
            // loader.hide();
          },
          () => {
            // loader.hide();
            this.errorMessage = 'Server error';
            this.showAlert();
          }
        );
      }
    },
    onReset() {
        console.log("resetingg")
      //event.preventDefault(); //prevents reset?? 
      this.showExample = false;
      this.form = Object.assign({}, this.form, { //not displayed...
        program: 'blastn',
        evalue: 1e-10,
        maxNbAlignments: null,
        sequences: '',
      });
    },
    setExample() {
      this.form = Object.assign({}, this.form, this.example);
      this.variant = 'success';
      this.showAlert();
    },

  },
};
</script>
<style scoped>
#blast {
  padding-top: 100px;
}
.form-header {
    color: white;
    background-color: #4a148c;
}
.submit-button{
    margin: 10px;
}
.alert{
    padding-top: 100px;
}

</style>