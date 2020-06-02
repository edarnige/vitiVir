<template>
  <div class="blast-result">
    <div id="div-selectQuery">
      <b-form-group
        v-if="jsonData"
        label-size="sm"
        label="Results for"
        label-for="selectQuery"
        horizontal
      >
        <b-form-select
          id="selectQuery"
          v-model="selectedQuery"
          size="sm"
          :options="queries"
        ></b-form-select>
      </b-form-group>
    </div>
    <blast-graphics
      v-if="jsonData"
      :json-data="jsonData"
      :query="selectedQuery"
      @selectAlignment="selectAlignment"
    ></blast-graphics>
    <!--@onRowClick redirect to entry detail -->
    <blast-table
      v-if="jsonData"
      :json-data="jsonData"
      :query="selectedQuery"
      :db="db"
      :db-type="dbType"
      selection-button-text="Download selected sequences (fasta)"
      button-action-label="alignment"
      @onRowClick="selectAlignment" 
      @clickActionOnSelect="openFastaWindow"
      @launchAction="selectAlignment"
    ></blast-table>
    <b-modal ref="modal-align" ok-only size="xl" hide-header-close :title="titleModal">
      <blast-alignment
        v-if="jsonData && subject"
        ref="blast-alignment"
        :json-data="jsonData"
        :query="selectedQuery"
        :db-type="dbType"
        :subject="subject"
      ></blast-alignment>
    </b-modal>
    <b-modal
      id="modal-get-fasta"
      ref="modal-get-fasta"
      title="Get fasta sequences"
      @ok="getFastaSequences"
    >
      <form v-show="showBoundForm" ref="formFasta" @submit.stop.prevent="getFastaSequences">
        <b-form-group
          invalid-feedback="Must be a positive integer"
          :state="lbState"
          label="Number of bases upstream"
          label-for="lb-input"
        >
          <b-form-input
            id="lb-input"
            v-model="lbFasta"
            type="number"
            :state="lbState"
            required
          ></b-form-input>
        </b-form-group>
        <b-form-group
          invalid-feedback="Must be a positive integer"
          :state="ubState"
          label="Number of bases downstream"
          label-for="ub-input"
        >
          <b-form-input
            id="ub-input"
            v-model="ubFasta"
            type="number"
            :state="ubState"
            required
          ></b-form-input>
        </b-form-group>
      </form>
    </b-modal>
  </div>
</template>

<script>
import BlastGraphics from '@/views/components/blast/BlastGraphics.vue';
import BlastTable from '@/views/components/blast/BlastTable.vue';
import BlastAlignment from '@/views/components/blast/BlastAlignment.vue';

// import Vue from 'vue';

var blastParser = require('biojs-io-blast');

export default {
  name: 'BlastResult',
  components: {
    BlastGraphics,
    BlastTable,
    BlastAlignment,
  },
  props: {
    db: { type: String, default: null },
    dbType: { type: String, default: null },
    res: { type: String, default: null },
    urlResult: { type: String, default: null },
  },
  data: function() {
    return {
      subject: '',
      tooltip: 'Click on a row to display the alignment',
      lbFasta: 0,
      ubFasta: 0,
      selectedIds: [],
      selectedQueryProxy: null,
    };
  },

  computed: {
    showBoundForm() {
      console.log('change dbType :' + this.dbType);
      return this.dbType == 'genomic';
    },
    lbState() {
      const reg = /^\d+$/;
      return reg.test(this.lbFasta);
    },
    ubState() {
      const reg = /^\d+$/;
      return reg.test(this.ubFasta);
    },
    jsonData() {
      if (this.res != null && typeof this.res !== undefined) return blastParser.parse(this.res);
      else return {};
    },
    titleModal() {
      return this.selectedQuery + ' vs ' + this.subject;
    },
    currentIteration() {
      if (typeof this.jsonData !== undefined) {
        return this.jsonData.iterations.find(i => i['query-def'] == this.selectedQuery);
      } else {
        return {};
      }
    },
    selectedQuery: {
      get: function() {
        let val;
        if (this.selectedQueryProxy == null) {
          val = this.queries.length > 0 ? this.queries[0].value : null;
        } else {
          val = this.selectedQueryProxy;
        }
        return val;
      },
      set: function(val) {
        this.selectedQueryProxy = val;
      },
    },
    queries: function() {
      return this.jsonData.iterations
        ? this.jsonData.iterations
            .map(it => it['query-def'])
            .filter((v, i, a) => a.indexOf(v) === i)
            .map(q => ({ value: q, text: q }))
        : [];
    },
    // selectedQuery: {
    //   get: function() {
    //     let val = this.queries.length > 0 ? this.queries[0].value : null;
    //     // this.query = val;
    //     return val;
    //   },
    //   set: function() {},
    // },
    // queries: function() {
    //   return this.jsonData.iterations
    //     ? this.jsonData.iterations
    //         .map(it => it['query-def'])
    //         .filter((v, i, a) => a.indexOf(v) === i)
    //         .map(q => ({ value: q, text: q }))
    //     : [];
    // },
  },
  methods: {
    changeQuery: function(v) {
      this.query = v;
    },
    openFastaWindow(ids) {
      this.selectedIds = ids;
      this.$refs['modal-get-fasta'].show();
    },
    /**
     * Take into acoount nb of bases upstream
     * and downstream indicated in the form
     */
    getLimitsHsps(a_hsps, len) {
      // On recupere les froms et les to
      let a_froms = a_hsps.map(h => h['hit-from']);
      let a_tos = a_hsps.map(h => h['hit-to']);

      let min = Math.min(...a_froms) - this.lbFasta;

      min = min < 1 ? 1 : min;

      let max = parseInt(Math.max(...a_tos)) + parseInt(this.ubFasta);

      max = max > len ? len : max;

      return [min, max];
    },
    getHitTarget(id) {
      let hit = this.currentIteration.hits.filter(h => h.id == id)[0];
      return hit;
    },
    getLimitsTarget(id) {
      let hit = this.getHitTarget(id);
      let a_from_to = this.getLimitsHsps(hit.hsps, hit.len);
      return a_from_to;
    },
    getFastaSequences() {
      //write fasta format
      let str = ''
      if (this.jsonData.iterations && this.selectedQuery !== "") {
        this.jsonData.iterations.forEach(iteration => {
          let queryId = iteration["query-def"];
          if (queryId === this.selectedQuery) {
            iteration.hits.forEach(hit =>{
              if(this.selectedIds.includes(hit.id)){
                str += ">" + hit.id +"\n" + hit.hsps[0].hseq + "\n"; //I think there is always only 1 hsps?
              }
            })
          }
        })
      }
      //download fasta file
      var fileURL = window.URL.createObjectURL(new Blob([str]));
      var fileLink = document.createElement('a');
      fileLink.href = fileURL;
      fileLink.setAttribute('download', 'sequences.fasta');
      document.body.appendChild(fileLink);
      fileLink.click();
    },

    selectAlignment(acc) {
      this.subject = acc;
      this.$refs['modal-align'].show();
      // Vue.nextTick(() => {
      //   this.$refs['blast-alignment'].$el.scrollIntoView();
      // });
    },
  },
};
</script>
<style scoped>
.blast-result {
  margin: 50px 0 50px 0;
}
</style>
