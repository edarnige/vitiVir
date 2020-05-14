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
                <md-datepicker class="md-primary" v-model="startDate">
                  <label>Start date</label>
                </md-datepicker>
                <md-datepicker class="md-primary" v-model="endDate">
                  <label>End date</label>
                </md-datepicker>
              </div>

          </div>
          <div class="md-layout">

              <md-checkbox v-model="verified">Verified only</md-checkbox>
              <md-checkbox v-model="exclude" value="Vitis vinifera" >Exclude <i>Vitis vinifera</i></md-checkbox>

                <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                  <md-field>
                    <label for="order">Order by</label>
                    <md-select v-model="order" name="order" id="order">
                      <md-option value="evalue">evalue</md-option>
                      <md-option value="qlength">query length</md-option>
                      <md-option value="percentID">percent id</md-option>
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
  //bodyClass: "index-page",
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

  data() {
    return {
      exclude: '',
      verified: this.$store.state.verified,
      sample: this.$store.state.sample,
      host: this.$store.state.host_organism,
      vtype: this.$store.state.virus_type,
      taxonomy: this.$store.state.taxonomy,
      description: this.$store.state.description,
      startDate: '',
      endDate: '',
      order: '',

    };
  },
  methods: {
    exportCSV(){
      axios.get("http://0.0.0.0:9000/api/data/entries_csv/", {
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
      console.log("before resetting search_q ",this.search_q,"stored",this.$store.state.search_q)
      this.$store.commit('setSearch', '?') //reset every new search

      console.log("after resetting search_q ",this.search_q, "stored", this.$store.state.search_q)
      console.log("testing the stored host",this.host)

      
      this.$store.dispatch('setQParams',{
        sample: this.sample, 
        host_organism: this.host, 
        virus_type: this.vtype, 
        taxonomy: this.taxonomy, 
        description: this.description, 
        verified: this.verified
      }) //not working

      console.log("host stored after commit", this.$store.state.host)
      //build query
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
      }

      this.$store.commit('setSearch', search_q)
      console.log(this.$store.state.search_q)

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
