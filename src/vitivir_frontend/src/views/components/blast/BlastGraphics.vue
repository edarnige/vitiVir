<template>
  <div id="alignments-container">
    <div id="alignments-container-header">
      <div class="legend-title">Legend for alignment {{modeLabel}}</div>
      <blast-legend :mode="mode"></blast-legend>
      <blast-query-bar :length="queryLength" :text="query"></blast-query-bar>
    </div>
    <div id="alignments-bars">
      <svg width="100%">
        <alignment-bar
          v-for="hsp in hsps"
          :key="hsp.id"
          :accession="hsp['accession']"
          :rowNumber="hsp['row-number']"
          :score="hsp['bit-score']"
          :evalue="hsp['evalue']"
          :queryLength="hsp['query-length']"
          :alignmentLength="hsp['length']"
          :alignmentPos="hsp['query-from']"
          :def="hsp['def']"
          :mode="mode"
          v-on:click.native="selectAlignment(hsp['accession'])"
        ></alignment-bar>
      </svg>
    </div>
    <b-button @click="changeMode">{{ buttonModeText }}</b-button>
  </div>
</template>

<script>
import AlignmentBar from "@/views/components/blast/AlignmentBar.vue";
import BlastLegend from "@/views/components/blast/BlastLegend.vue";
import BlastQueryBar from "@/views/components/blast/BlastQueryBar.vue";

export default {
  name: "blast-graphics",

  components: {
    AlignmentBar,
    BlastLegend,
    BlastQueryBar
  },

  data: function() {
    return {
      mode: 1 // 0:e-value, 1:max score };
    };
  },
  props: {
    jsonData: { 
      type: Object, 
      default: () => ({}) 
      },
    query:{
      type: String,
      default: ""
    }
  },

  computed: {
    modeLabel: function() {
      return this.mode ? "bit-score" : "evalue";
    },
    buttonModeText: function() {
      return this.mode
        ? "Change scoring to e-value"
        : "Change scoring to bit-score";
    },
    hsps: function() {
      let a_all_hsps = [];

      if (this.jsonData.iterations && this.query !== "") {
        this.jsonData.iterations.forEach(iteration => {
          let queryId = iteration["query-def"];
          if (queryId === this.query) {
            let queryLength = parseInt(iteration["query-len"]);
            let a_hits = iteration["hits"];
            a_hits.forEach(hit => {
              let acc = hit["accession"];
              //let def = hit["def"];
              //let len = hit["len"];
              let a_hsps = hit["hsps"];
              let num = hit["num"];
              a_hsps.forEach(hsp => {
                hsp["accession"] = acc;
                hsp["def"] = hit["def"];
                hsp["row-number"] = num;
                hsp["id"] = acc + "_" + num + "_" + hsp["num"];
                hsp["query-length"] = queryLength;
                hsp["length"] = hsp["query-to"] - hsp["query-from"] + 1;
                hsp["evalue"] = Number(hsp["evalue"]);
                a_all_hsps.push(hsp);
              });
            });
          }
        });
      }
      return a_all_hsps;
    },

    queryLength: function() {
      let queryLength = 0;
      if (this.jsonData.iterations) {
        this.jsonData.iterations.forEach(iteration => {
          let queryId = iteration["query-def"];
          if (queryId === this.query) {
            queryLength = parseInt(iteration["query-len"]);
          }
        });
      }
      return queryLength;
    }
  },

  methods: {
    selectAlignment: function(acc) {
      this.$emit("selectAlignment", acc);
    },
    changeMode: function() {
      this.mode ? (this.mode = 0) : (this.mode = 1);
    }
  }
};
</script>

<style scoped>
#alignments-container {
  border: thin solid rgb(221, 221, 221);
  margin: 10px auto;
  padding: 10px;
  min-width: 400px;
  background-color: rgb(255, 255, 255);
}

.legend-title {
  font-size: 12px;
  font-weight: bold;
}
</style>
