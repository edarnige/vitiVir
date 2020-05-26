<template>
<div class="wrapper">
  <div>
    <b-container id="blast"><!-- <b-container v-if="authenticated"> -->
      <h2>Search by Blast</h2>
      <h4>Select an organism and enter a query sequence</h4>
      <div role="tablist">
        <b-card no-body class="text-left mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-btn v-b-toggle.form-panel block href="#" variant="info">Blast form</b-btn>
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
                <b-col md="12" lg="6">
                  <Tree
                    ref="tree"
                    multiple
                    :data="tree_data"
                    show-checkbox
                    allow-batch
                    @changedbtype="changeDbType"
                  />
                </b-col>
                <b-col md="12" lg="6">
                  <b-card bg-variant="light">
                    <blast-form
                      ref="blast-form"
                      :default-program="form.program"
                      :default-filter="form.filter"
                      :default-evalue="form.evalue"
                      :default-db="form.db"
                      :default-matrix="form.matrix"
                      :default-word-size="form.wordSize"
                      :default-max-nb-alignments="form.maxNbAlignments"
                      :default-sequences="form.sequences"
                      :db-type="dbType"
                      @changedbtypeinput="changeDbTypeInput"
                    ></blast-form>

                    <b-button variant="outline-primary" size="sm" @click="setExample"
                      >Example</b-button
                    >
                    <b-button type="submit" variant="primary">Blast</b-button>
                    <b-button type="reset" variant="danger">Reset</b-button>
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
        <b-card v-if="urlBlastResult" no-body class="text-left mb-1">
          <b-card-header header-tag="header" class="p-1" role="tab">
            <b-btn v-b-toggle.res-panel block href="#" variant="info">Results</b-btn>
          </b-card-header>
          <b-collapse id="res-panel" v-model="showRes" accordion="res-accordion" role="tabpanel">
            <blast-result
              :url-result="urlBlastResult"
              :db="aliasDb"
              :db-type="form.db"
              :res="res"
            ></blast-result>
          </b-collapse>
        </b-card>
      </div>
    </b-container>
    <!-- <b-alert v-else show variant="danger">You must be logged to access this function</b-alert> -->
  </div>
</div> 
</template>

<script>
import Tree from '@/views/components/Tree.vue';
import Vue from 'vue';
import BlastResult from '@/views/components/blast/BlastResult.vue';
import BlastForm from '@/views/components/blast/BlastForm.vue';

export default {
  name: 'Blast',
  components: {
    Tree,
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
      dbType: '',
      form: {
        program: 'blastn',
        filter: true,
        evalue: 1e-10,
        db: 'CDS',
        matrix: 'BLOSUM62',
        wordSize: null,
        maxNbAlignments: null,
        sequences: '',
        speciesIds: '',
      },
      example: {
        program: 'blastp',
        filter: true,
        evalue: 1e-10,
        db: 'protein',
        matrix: 'BLOSUM62',
        wordSize: null,
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
        speciesIds: '312,54',
      },

      programs: [
        { text: 'blastn', value: 'blastn' },
        { text: 'blastp', value: 'blastp' },
        { text: 'blastx', value: 'blastx' },
        { text: 'tblastn', value: 'tblastn' },
        { text: 'tblastx', value: 'tblastx' },
      ],
      matrices: [
        { text: 'BLOSUM45', value: 'BLOSUM45' },
        { text: 'BLOSUM50', value: 'BLOSUM50' },
        { text: 'BLOSUM62', value: 'BLOSUM62' },
        { text: 'BLOSUM80', value: 'BLOSUM80' },
        { text: 'BLOSUM90', value: 'BLOSUM90' },
        { text: 'PAM250', value: 'PAM250' },
        { text: 'PAM30', value: 'PAM30' },
        { text: 'PAM70', value: 'PAM70' },
      ],
      dbTypes: [
        { text: 'CDS', value: 'CDS' },
        { text: 'genomic', value: 'genomic' },
        { text: 'protein', value: 'protein' },
      ],
      urlBlastResult: '',
      aliasDb: '',
      errorMessage: 'Error',
      variant: 'danger',
      dismissSecs: 3,
      dismissCountDown: 0,
    };
  },

  computed: {
    tree_data: function() {
      return this.$store.getters.getTreeData;
    },
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

        let a_selected = this.$refs.tree.getSelected();
        finalForm.speciesIds = a_selected.map(x => x.id).join();
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
              this.aliasDb = resp.body.aliasDb;
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
        filter: true,
        evalue: 1e-10,
        db: 'CDS',
        matrix: 'BLOSUM62',
        wordSize: null,
        maxNbAlignments: null,
        sequences: '',
        speciesIds: '',
      });
      this.$refs.tree.setSelected([]);
      this.$refs.tree.filterTreeBySelected();
    },
    setExample() {
      this.form = Object.assign({}, this.form, this.example);

      let n = this.$refs.tree.setSelected(['312', '54']);
      this.$refs.tree.filterTreeBySelected();
      this.errorMessage = `${n} species have been selected`;
      this.variant = 'success';
      this.showAlert();
    },
    changeDbTypeInput(val) {
      this.$set(this.form, 'db', val);
    },
    changeDbType(val) {
      this.dbType = val;
    },
  },
};
</script>
<style scoped>
#blast {
  padding-top: 100px;
}

button {
  margin: 10px;
}


</style>