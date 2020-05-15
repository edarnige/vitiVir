<template>
  <div class="wrapper">
    <div class="section section-basic">  
      <div class="container">
                
        <div class="title">
          <h2>Search query filters</h2>
        </div>    
      
      <!-- </div>
        
        <div class="container"> -->

          <div class="md-layout">

            <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
              <md-field>
                <label>Sample</label>
                <md-input v-model="sample"><label></label></md-input>
              </md-field>
            </div>

            <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
              <md-field >
                <label>Host organism</label>
                <md-input v-model="host"></md-input>
              </md-field>
            </div>

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                <md-field >
                  <label>Virus type</label>
                  <md-input v-model="vtype"></md-input>
                </md-field>
              </div>

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                <md-field >
                  <label>Taxonomy</label>
                  <md-input v-model="taxonomy"></md-input>
                </md-field>
              </div>
          
          </div>
          <div class="md-layout">

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                <md-datepicker class="md-primary" v-model="start_date">
                  <label>Start date (yyyy-mm-dd)</label>
                </md-datepicker>
                <md-datepicker class="md-primary" v-model="end_date">
                  <label>End date (yyyy-mm-dd)</label>
                </md-datepicker>
              </div>

          </div>
          <div class="md-layout">

              <md-checkbox v-model="verified">Verified only</md-checkbox>
              <md-checkbox v-model="exclude_vitis" >Exclude <i>Vitis vinifera</i></md-checkbox>

                <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                  <md-field>
                    <label for="order">Order by</label>
                    <md-select v-model="ordering" name="ordering" id="ordering">
                      <md-option value=""> </md-option>
                      <md-option value="evalue"> rps-blast evalue (asc)</md-option>
                      <md-option value="query_length"> query length (desc)</md-option>
                      <md-option value="percent_id"> blastx percent id (desc)</md-option>
                    </md-select>
                    </md-field>
                  </div>
          </div>

          <div class="md-layout-item md-size-50 md-small-size-70 md-xsmall-size-100">
            <md-button class="md-primary" @click="search()">
              Search
            </md-button>
          </div>

          <!-- </div> -->
        <!-- </div> -->


    <!-- Results -->

        <div class="section section-basic">
          <!-- <div class="container"> -->
              
            
              <div class="title">
                <h2>Results</h2>
              </div>
              <div class="text-right">
              <md-button  class="md-primary" @click.prevent="exportCSV()"> 
                Export CSV
              </md-button>
              </div>

            
            <div>
              <ListEntries ref="results"/>
            </div>
          
          </div>

      </div>
    </div>
  </div>
</template>

<script>
import ListEntries from '@/views/components/ListEntries.vue'
import axios from 'axios';

export default {
  components: {
    ListEntries,
  },
  name: "search",

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
    },  
  },

  data() {
    return {
      exclude_vitis: this.$store.state.exclude_vitis,
      verified: this.$store.state.verified,
      sample: this.$store.state.sample,
      host: this.$store.state.host_organism,
      vtype: this.$store.state.virus_type,
      taxonomy: this.$store.state.taxonomy,
      description: this.$store.state.description,
      start_date: this.$store.state.start_date,
      end_date: this.$store.state.end_date,
      ordering: this.$store.state.ordering,

    };
  },
  methods: {
    exportCSV(){
      axios.get("http://0.0.0.0:9000/api/data/entries_csv/" + this.$store.state.search_q, {
      })
      .then(res => {
        console.log(res);
        var fileURL = window.URL.createObjectURL(new Blob([res.data]));
        var fileLink = document.createElement('a');
        
        fileLink.href = fileURL;
        fileLink.setAttribute('download', 'results.csv');
        document.body.appendChild(fileLink);
        
        fileLink.click();
      })
      .catch(err => {
        console.log(err);
      })
    },

    search(){
      //Reset query
      this.$store.commit('setSearch', '?')

      //Format the dates
      let formated_start_date = undefined
      let formated_end_date = undefined

      if (this.start_date != undefined){
        this.start_date = new Date(this.start_date)
        formated_start_date = this.start_date.getFullYear() + 
          '-' + (this.start_date.getMonth()+1) +
          '-' + this.start_date.getDate() 
      } 
      if (this.end_date != undefined){
        console.log("end date is not undefined",this.end_date)
        this.end_date = new Date(this.end_date)
        formated_end_date = this.end_date.getFullYear() + 
          '-' + (this.end_date.getMonth()+1) +
          '-' + this.end_date.getDate() 
      }

      //Store variables
      this.$store.dispatch('setQParams',{
        sample: this.sample, 
        host_organism: this.host, 
        virus_type: this.vtype, 
        taxonomy: this.taxonomy, 
        description: this.description, 
        verified: this.verified,
        exclude_vitis: this.exclude_vitis,
        start_date: formated_start_date,
        end_date: formated_end_date,
        ordering: this.ordering 
      }) 

      //Build query
      let search_q= "?"
      if (this.sample != undefined){
        search_q += "&sample=" + this.$store.state.sample
      } if (this.host != undefined){
        search_q += "&host_organism=" + this.$store.state.host_organism //use stored names
      } if (this.vtype != undefined){
        search_q += "&virus_type=" + this.$store.state.virus_type
      } if (this.taxonomy != undefined){
        search_q += "&taxonomy=" + this.$store.state.taxonomy
      } if (this.description != undefined){
        search_q += "&description=" + this.$store.state.description
      } if (this.verified != undefined){
        search_q += "&verified=" + this.$store.state.verified
      } if (this.exclude_vitis!= undefined){
        search_q += "&exclude_vitis=" + this.$store.state.exclude_vitis
      } if(this.start_date != undefined){
        search_q += "&start_date=" + this.$store.state.start_date
      } if(this.end_date != undefined){
        search_q += "&end_date=" + this.$store.state.end_date
      } if(this.ordering != undefined){
        search_q += "&ordering=" + this.$store.state.ordering
      }

      //Store query
      this.$store.commit('setSearch', search_q)

      //set page visual back to 1
      //???

      //Get results based on query
      this.$refs.results.getSearch()
      
      }

  },
  
};
</script>
<style lang="scss">
.vertical-center {
  display: flex;
  align-items: center;
}
.md-checkbox{
  display: flex;
  margin: 0;
  margin-bottom: 0.5rem;
}
</style>
