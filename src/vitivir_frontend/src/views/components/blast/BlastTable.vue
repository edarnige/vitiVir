<template>
  <div>
    <vue-good-table
      ref="blast-table"
      :columns="columns"
      :rows="rows"
      :select-options="{
        enabled: true,
        selectOnCheckboxOnly: true, // only select when checkbox is clicked instead of the row
        selectionInfoClass: 'custom-class',
        selectionText: 'accessions selected',
        clearSelectionText: 'clear',
      }"

    >
      <div slot="selected-row-actions">
        <b-button pill @click="clickButton">{{ selectionButtonText }}</b-button>
      </div>

      <template slot="table-row" slot-scope="props">
        <template v-if="maskLink && props.column.field == 'accession'">
          <a
            v-if="props.column.field == 'accession'"
            :href="createLink(props.row.accession)"
            target="_blank"
            >{{ props.row.accession }}</a
          > <!-- remove href and target?-->
        </template>
        <template v-else>
          <span v-if="props.column.field == 'action' || props.column.field == 'align'">
            <b-button v-if="props.column.field == 'action'" pill variant="outline-primary" @click="launchAction(props.row)">entry</b-button>
            <b-button v-if="props.column.field == 'align'" pill variant="outline-primary" @click="onEyeClick(props)"><i class="fas fa-eye"></i>
            </b-button>
          </span>
          <span v-else>{{ props.formattedRow[props.column.field] }}</span>
        </template>
      </template>
      <div slot="table-actions-bottom">
        <b-button @click="downloadAsCsv">Download as CSV</b-button>
      </div>
    </vue-good-table>
  </div>
</template>

<script>
import { VueGoodTable } from 'vue-good-table';
import 'vue-good-table/dist/vue-good-table.css';

const formatPercentage = function(value) {
  return value + '%';
};
export default {
  name: 'BlastTable',
  components: {
    VueGoodTable,
  },
  props: {
    buttonActionLabel: { type: String, default: 'action' },
    jsonData: {
      type: Object,
      default: () => {
        return {};
      },
    },
    query: { type: String, default: '' },
    maskLink: undefined,
    selectionButtonText: { type: String, default: 'Click' },
  },

  computed: {
    columns: function() {
      return [
        {
          label: 'Accession',
          field: 'accession',
        },
        {
          label: 'Description',
          field: 'description',
        },
        {
          label: 'Query ID',
          field: 'query_id',
        },
        {
          label: 'Hit length',
          field: 'length',
          type: 'number',
        },
        {
          label: 'Query cover',
          field: 'query-cover',
          type: 'number',
          formatFn: formatPercentage,
        },
        {
          label: 'Max score',
          field: 'max-score',
          type: 'number',
        },
        {
          label: 'Total score',
          field: 'total-score',
          type: 'number',
        },
        {
          label: 'E-value',
          field: 'evalue',
          type: 'number',
        },
        {
          label: 'Identities',
          field: 'identities',
          type: 'number',
          formatFn: formatPercentage,
        },
        {
          label: "Alignment",//this.buttonActionLabel,
          field: 'align',
        },
        {
          label: "To entry",//this.buttonActionLabel,
          field: 'action',
        },
      ];
    },
    rows: function() {
      var a_rows = [];
      if (this.jsonData.iterations && this.query != '') {
        this.jsonData.iterations.forEach(iteration => {
          let queryId = iteration['query-def'];
          if (queryId === this.query) {
            let queryLength = parseInt(iteration['query-len']);
            let a_hits = iteration['hits'];
            a_hits.forEach(hit => {
              let a_hsps = hit['hsps'];
              let totalLength = 0;
              let totalAlignmentLength = 0;
              let totalIdentities = 0;
              let maxIdentities = 0;
              let minEvalue = 100000;
              let maxScore = 0;
              let totalScore = 0;
              a_hsps.forEach(hsp => {
                totalLength += parseInt(hsp['length']);
                let identity = parseInt(hsp['identity']);
                let alignLen = parseInt(hsp['align-len']);

                totalIdentities += identity;
                totalAlignmentLength += alignLen;

                if (hsp['evalue'] < minEvalue) {
                  minEvalue = hsp['evalue'];
                }
                if (hsp['bit-score'] > maxScore) {
                  maxScore = hsp['bit-score'];
                }
                if (identity > maxIdentities) {
                  maxIdentities = identity;
                }
                totalScore += hsp['bit-score'];
              });
              hit['max-score'] = Math.round(maxScore * 10) / 10;
              hit['length']= totalLength
              hit['total-score'] = Math.round(totalScore * 10) / 10;
              hit['evalue'] = minEvalue;
              hit['query-cover'] = Math.round((totalLength / queryLength) * 100);
              hit['identities'] = Math.round((totalIdentities / totalAlignmentLength) * 100);

              let def = hit.def.split("|");
              hit['accession'] = def[1];
              hit['description'] = def[2];
              hit['query_id'] = def[3];
              hit['vitivir_id'] = hit.id;
              
              a_rows.push(hit); //list of hits has def
            });
          }
        });
      }
      return a_rows;
    },
  },
  methods: {
    createLink: function(value) {
      return this.maskLink + '/' + value;
    },
    clickButton: function() {
      this.$emit(
        'clickActionOnSelect',
        this.$refs['blast-table'].selectedRows.map(x => x.vitivir_id) //accession
      );
    },
    launchAction: function(params) { //to detail page
      const entry_id = params.id
      let route = this.$router.resolve({path: '/search/'+entry_id});
      window.open(route.href)
    },
    onEyeClick: function(params) {
      this.$emit('onRowClick', params.row.accession);
    },
    downloadAsCsv: function() {
      let str = '';

      this.columns.forEach(col => {
        str += col['label'] + ',';
      });
      str += '\n';

      this.rows.forEach(row => {
        str +=
          '"' +
          row['accession'] +
          '",' +
          '"' +
          row['description'] +
          '",' +
          '"' +
          row['query_id'] +
          '",' +
          '"' +
          row['length']+
          '",' +
          '"' +
          row['query-cover'] +
          '",' +
          '"' +
          row['max-score'] +
          '",' +
          '"' +
          row['total-score'] +
          '",' +
          '"' +
          row['evalue'] +
          '",' +
          '"' +
          row['identities'] +
          '"\n';
      });

      var element = document.createElement('a');
      element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(str));
      element.setAttribute('download', 'table.csv');

      element.style.display = 'none';
      document.body.appendChild(element);

      element.click();

      document.body.removeChild(element);
    },
  },
};
</script>

<style scoped>
h4{
  margin-left: 10px;
}
</style>
