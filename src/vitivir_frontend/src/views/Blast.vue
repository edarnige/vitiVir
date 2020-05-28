<template>
<div class="wrapper">
  <div>
    <b-container id="blast"><!-- <b-container v-if="authenticated"> -->
        <div class="row">
            <div class="col">
                <h2>Search by Blast</h2>
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
    <!-- <b-alert v-else show variant="danger">You must be logged to access this function</b-alert> -->
  </div>
</div> 
</template>

<script>
import Vue from 'vue';
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
        program: 'tblastn',
        evalue: 1e-10,
        maxNbAlignments: null,
        sequences: `>test sequence 1
MEYGGGLVADGGVFGPMVGGGGGDQADIIEELLGEGC
WIEASENSLMAMQQTTPQSQYMSNNNNIPMGMGEGDH
FNHHHHHHPHPHHQMECTAPAANHDDQQESGFVVGKR
WWIGPRANPGPTTSVKERLVVAVGYLKEYTKNSSNNV
LIQIWVPMRRRSALIHTQNHYLQQESSSAPVSVNPNM
NVHVRFFRSHDYPRHQQQQQYGSLLALPVFERGSGTC
LGVIEFVISNQTLINYRPQLDHLSNALEAVDFRSSHN
MNIPQAVKVFEELYEAAVNEIMEVLASVCKTHNLPLA
LTWAPCLQQQQGGGKGSSGASGCGVSTMSCCISTVDS
ACYVGDMDVLGFQEACSEYHLFNGQGIVGTAFTTTKP
CFAIDITAFSKSEYPLAHHANMFGLHAAVAIPLRSVY
TGSAADFVLEFFLPKDCRDTEQQKQMLNSLSLVVQQA
CRSLHLHVVMDDNNNNNMNDNNSSADHDHDQFTFPTT
NSYMPSSASEPLSQVDAVSGCSTKDTSSSCSWIAHMM
EAQNKGKGVSVSLEYLQEPKEEFKVTTCNWDREREDN
VFSEFGQVLQQQQHDQSSNSRASVVSVEAGEESPGAC
GRRSSSSSSGRKSGDKRRTKAEKTISLPVLRQYFAGS
LKDAAKSIGVCPTTLKRICRQHGITRWPSRKIKKVGH
SLKKLQLVIDSVQGAEGAIQIGSFYASFPELSNATAN
GGDGNDNSNNSFYNNNHGDGIVTSLKSPPSACSQTHA
GNKLPMTTTTAINHHHVVMTENPTGAPLGVDHAFMHA
SNINIQDYHQLQEDLDTKQLLLHFNNNNQILPPRPTV
AWNNNNSSSSTLLERGAFRVKATFADEKIRFSLQAMW
GFRDLQLEIARRFNLTDMNNLVLKYLDDEGEWVVLSC
DADLEECKDLHTSSHTRTIRLSLFQASPLNLPNTFRN
SSSSSPSS
>test sequence 2
VKVFEELYEAAVNEIMEVLASVCKTHNLPLALTWAPC
LQQQQGGGKGSSGASGCGVSTMSCCISTVDSACYVGD
MDVLGFQEACSEYHLFNGQGIVGTAFTTTKPCFAIDI
TAFSKSEYPLAHHANMFGLHAAVAIPLRSVYTGSAAD
FVLEFFLPKDCRDTEQQKQMLNSLSLVVQQACRSLHL
HVVMDDNNNNNMNDNNSSADHDHDQFTFPTTNSYMPS
SASEPLSQVDAVSGCSTKDTSSSCSWIAHMMEAQNKG
KGVSVSLEYLQEPKEEFKVTTCNWDREREDNVFSEFG
QVLQQQQHDQSSNSRASVVSVEAGEESPGACGRRSSS
SSSGRKSGDKRRTKAEKTISLPVLRQYFAGSLKDAAK
SIGVCPTTLKRICRQHGITRWPSRKIKKVGHSLKKLQ
LVIDSVQGAEGAIQIGS`,
        //speciesIds: '312,54',
      },

      programs: [
        { text: 'blastn', value: 'blastn' }, //remove
        { text: 'blastp', value: 'blastp' },
        { text: 'blastx', value: 'blastx' },
        { text: 'tblastn', value: 'tblastn' }, //remove
        { text: 'tblastx', value: 'tblastx' }, //remove
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
      event.preventDefault();

      let blastForm = this.$refs['blast-form'].form;

      if (this.$refs['blast-form'].isValid()) {
        let finalForm = Object.assign({}, blastForm);
        finalForm.login = this.$store.getters.getLogin;
        finalForm.token = this.$store.getters.getToken;

        let loader = this.$loading.show({
          // Optional parameters
          container: null,
          canCancel: false,
          loader: 'dots',
        });
        Vue.http.post('api/blast', finalForm).then(
          // eslint-disable-next-line arrow-parens
          resp => {
            var success = resp.body.success;
            if (success === false) {
              this.errorMessage = resp.body.message;
              this.showAlert();
            } else {
              this.urlBlastResult = resp.body.url;
              // TODO : à enlever
              this.res = resp.body.res;
              if (resp.body.url === undefined || resp.body.url === '') {
                this.errorMessage = 'No result';
                this.showAlert();
              } else {
                this.showForm = false;
              }
            }
            loader.hide();
          },
          () => {
            loader.hide();
            this.errorMessage = 'Server error';
            this.showAlert();
          }
        );
      }
    },
    onReset() {
      event.preventDefault();
      this.showExample = false;
      this.form = Object.assign({}, this.form, {
        program: 'blastn',
        evalue: 1e-10,
        maxNbAlignments: null,
        sequences: '',
        //speciesIds: '',
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



</style>