<template>
  <div class="wrapper" v-if="$store.state.token">
    <div class="section section-basic">  
      <div class="container">
                
        <div class="title">
          <h2>Search query filters</h2>
        </div>    
      

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
                    <md-select v-model="vtype" placeholder="" name="vtype" id="vtype">
                      <md-option value=""></md-option>
                      <md-option value="Mycovirus"> 
                        Mycovirus
                      </md-option>
                      <md-option value="Phytovirus"> 
                        Phytovirus
                      </md-option>
                      <md-option value="Bacteriophage"> 
                        Bacteriophage
                      </md-option>
                    </md-select>
                </md-field>
              </div>
          
          </div>

          <div class="md-layout">

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                <md-field >
                  <label>Taxonomy (any level)</label>
                  <md-input v-model="taxonomy"></md-input>
                </md-field>
                </div>

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                <md-autocomplete v-model="description" :md-options="domains" md-dense>
                  <label>Protein domain</label>
                </md-autocomplete>
              </div>

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                <md-autocomplete v-model="cultivar" :md-options="cultivars" md-dense>
                  <label>Cultivar</label>
                </md-autocomplete>
              </div>

          </div>

          <div class="md-layout">

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
                <md-datepicker class="md-primary" v-model="start_date">
                  <label>Start date (yyyy-mm-dd)</label>
                </md-datepicker>
              </div>

              <div class="md-layout-item md-size-25 md-xsmall-size-100 md-small-size-50 md-medium-size-25">
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
                    <md-select v-model="ordering" placeholder="" name="ordering" id="ordering">
                      <md-option value=""></md-option>
                      <md-option value="evalue"> 
                        rps-blast evalue (asc)
                      </md-option>
                      <md-option value="query_length"> 
                        query length (desc) 
                      </md-option>
                      <md-option value="percent_id"> 
                        blastx percent id (desc) 
                      </md-option>
                    </md-select>
                    </md-field>
                  </div>
          </div>

          <div class="md-layout-item md-size-50 md-small-size-70 md-xsmall-size-100">
            <md-button class="md-primary" @click="search()">
              Search
            </md-button>
          </div>


        <div class="section section-basic">

              
            
              <div class="title">
                <h2>Results</h2>
              </div>
              <div class="text-right">
              <md-button  class="md-primary" @click.prevent="exportFasta()"> 
                Export FASTA
              </md-button>
              <md-button  class="md-primary" @click.prevent="exportCSV()"> 
                Export CSV
              </md-button>
              <p class="csv-info"><br></p>
              <p class="csv-info">*The more results, the longer the download</p>
              </div>
              
            <div>
              <ListEntries ref="results"/>
            </div>
          
          </div>

      </div>
    </div>
  </div>
  <div class="wrapper login-alert" v-else >
    <b-alert show variant="danger">You must be logged in to access the search function</b-alert>
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
      cultivar: this.$store.state.cultivar,
      start_date: this.$store.state.start_date,
      end_date: this.$store.state.end_date,
      ordering: this.$store.state.ordering,
      domains:[
        'pfam00680, RdRP_1',
        'pfam00978, RdRP_2',
        'pfam00998, RdRP_3',
        'pfam02123, RdRP_4',
        'pfam07925, RdRP_5',
        'RdRP',
        'RNA dependent RNA polymerase',
        'pfam00286, Flexi_CP',
        'coat protein',
        'pfam01443, Viral_helicase1',
        'RNA helicase',
      ],
      cultivars:[
        'Petit Verdot noir',
        'Shiraz',
        'Mertlot noir',
        'Semillon blanc',
        'Sauvignon blanc',
        'Sauvignon gris',
        'Cabernet sauvignon noir',
        'Cabernet Sauvignon',
        'Pinot noir',
        'Fengzao'
      ]

    };
  },
  methods: {
    exportCSV(){
      this.$Progress.start()
      axios.get(`${process.env.VUE_APP_API_HOST}/api/data/entries_csv/` + this.$store.state.search_q, {
        headers: {
          'Authorization': 'Token ' + this.$store.state.token
        }
      })
      .then(res => {
        var fileURL = window.URL.createObjectURL(new Blob([res.data]));
        var fileLink = document.createElement('a');
        
        fileLink.href = fileURL;
        fileLink.setAttribute('download', 'results.csv');
        document.body.appendChild(fileLink);
        
        fileLink.click();
        this.$Progress.finish()
      })
      .catch(err => {
        this.$Progress.fail()
        console.log(err);
      })
    },

    exportFasta(){
      this.$Progress.start()
      axios.get(`${process.env.VUE_APP_API_HOST}/api/data/entries_fasta/` + this.$store.state.search_q, {
        headers: {
          'Authorization': 'Token ' + this.$store.state.token
        }
      })
      .then(res => {
        console.log(res)
        let fasta_format = ""
        let acc_list = [] //avoid redundancy 
        for (let obj of res.data){
          if (obj.blastx){
            if(obj.blastx.sequence){
              if(acc_list.includes(obj.blastx.accession) == false ){ //1x per accession
                acc_list.push(obj.blastx.accession);
                //console.log(acc_list);
                fasta_format += ">" + obj.blastx.accession + "|" + obj.blastx.description + "|" + 
                obj.query_id + "|" + obj.entry_id + "\n" + obj.blastx.sequence + "\n";
              }
            }
          }
        }
        var fileURL = window.URL.createObjectURL(new Blob([fasta_format]));
        var fileLink = document.createElement('a');
        
        fileLink.href = fileURL;
        fileLink.setAttribute('download', 'results.fasta');
        document.body.appendChild(fileLink);
        
        fileLink.click();
        this.$Progress.finish()
      })
      .catch(err => {
        this.$Progress.fail()
        console.log(err);
      })
    },

    search(){
      //Reset query
      this.$store.commit('setSearch', '?')

      //Format the dates
      let formated_start_date = undefined
      let formated_end_date = undefined
      if (this.start_date){
        this.start_date = new Date(this.start_date)
        formated_start_date = this.start_date.getFullYear() + 
          '-' + (this.start_date.getMonth()+1) +
          '-' + this.start_date.getDate() 
      } 
      if (this.end_date){
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
        cultivar: this.cultivar,
        verified: this.verified,
        exclude_vitis: this.exclude_vitis,
        start_date: formated_start_date,
        end_date: formated_end_date,
        ordering: this.ordering 
      }) 

      //Build query
      let search_q= "?"
      if (this.sample != undefined && this.sample != ''){
        search_q += "&sample=" + this.$store.state.sample
      } if (this.host != undefined && this.host != ''){
        search_q += "&host_organism=" + this.$store.state.host_organism //use stored names
      } if (this.vtype != undefined && this.vtype != ''){
        search_q += "&virus_type=" + this.$store.state.virus_type
      } if (this.taxonomy != undefined && this.taxonomy != ''){
        search_q += "&taxonomy=" + this.$store.state.taxonomy
      } if (this.description != undefined && this.description != ''){
        search_q += "&description=" + this.$store.state.description
      } if (this.cultivar != undefined && this.cultivar != ''){
        search_q += "&cultivar=" + this.$store.state.cultivar
      } if (this.verified != undefined && this.verified != false){
        search_q += "&verified=" + this.$store.state.verified
      } if (this.exclude_vitis!= undefined && this.exclude_vitis != false){
        search_q += "&exclude_vitis=" + this.$store.state.exclude_vitis
      } if(this.start_date){
        search_q += "&start_date=" + this.$store.state.start_date
      } if(this.end_date){
        search_q += "&end_date=" + this.$store.state.end_date
      } if(this.ordering != undefined && this.ordering != ''){
        search_q += "&ordering=" + this.$store.state.ordering
      }

      //Store query
      console.log("stored SQ", this.$store.state.search_q)
      this.$store.commit('setSearch', search_q)
      console.log("SQ",search_q)

      //Get results based on query
      this.$refs.results.getSearch()
      
      }

  },
  
};
</script>
<style lang="scss">
.md-list-item-text {
  padding-left: 10px;
  padding-right: 10px;
}
.vertical-center {
  display: flex;
  align-items: center;
}
.md-checkbox{
  display: flex;
  margin: 0;
  margin-bottom: 0.5rem;
  padding-right: 15px;
}
.options{
  padding-left: 20px;
}
.csv-info{
  font-size: 0.8em;
  color: #646464;
  line-height: 0.75;
}
.login-alert{
  padding-top:100px
}

</style>
