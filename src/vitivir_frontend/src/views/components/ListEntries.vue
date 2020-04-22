<template>
  <div>

   <div class="md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
    <md-table component-name="pagination" class="pagination pagination-primary">
      <md-table-row>
        <md-table-head>query id</md-table-head>
        <md-table-head>evalue</md-table-head>
        <md-table-head>query length</md-table-head>
        <md-table-head>percent id</md-table-head>
      </md-table-row>

      <md-table-row @click="$router.push('/landing');" v-for="entry in entries" v-bind:key="entry.entry_id">
        <md-table-cell>{{ entry.query_id }}</md-table-cell>
        <md-table-cell>{{ entry.blastrps.evalue}}</md-table-cell>
        <md-table-cell>{{ entry.blastx.query_length }}</md-table-cell>
        <md-table-cell>{{ entry.blastx.percent_identity }}</md-table-cell>
      </md-table-row>

    </md-table>
        <!-- <md-list-item to="/components/list/router">Router <code>/router/**</code></md-list-item> -->
   
    <pagination
      type="primary"
      no-arrows
      v-model="defaultPagination"
      :per-page="5">
    </pagination>

   </div>


  </div>
</template>


<script>
import axios from 'axios';
import {Pagination} from '@/components'


export default {
  name: 'entries',
  components: {
    Pagination

  },
  data() {
    return {
      entries : [],
      defaultPagination: 1,
    }
  },
  methods: {
    getEntries() {
      axios.get("http://0.0.0.0:9000/api/data/entries/")
      .then(res => (this.entries = res.data))
      .catch(err => console.log(err));
    },
  },
    created() { //calls methods
    this.getEntries();
  }
};
</script>

<style >
/* #entriesList li:nth-child(odd){
 background-color:#4a148c30;
}
#entriesList{
  list-style-type: none;
} */

/* .head {
    font-weight: bold;
} */
/* span.col {
    display: inline-block;
    width: 25%;
} */



</style>