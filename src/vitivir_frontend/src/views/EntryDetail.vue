<template>
  <div class="wrapper">
      <div class="section section-basic">  
      <div class="md-layout-item md-size-90">

        <md-button class="md-simple md-primary md-lg">Back</md-button>

        <h2 class="title text-center">Entry information</h2>
        <md-table >

            <md-table-row>
                <md-table-head >Query ID</md-table-head>
                <md-table-cell >{{ entry.query_id }}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head >Sample</md-table-head>
                <md-table-cell >{{ entry.sample }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Verified</md-table-head>
                <md-table-cell>
                    <div v-if="editMode==false" >
                        <i v-if="entry.verified==true" id="check" class="fas fa-check-circle"></i>
                        <i v-if="entry.verified==false" id="cross" class="fas fa-times-circle"></i>
                    </div>
                    <div v-if="editMode==true" class="edit">
                        <md-checkbox v-model="entry.verified"></md-checkbox>
                    </div>
                </md-table-cell>
            </md-table-row>    

            <md-table-row>
                <md-table-head>Virus type</md-table-head>
                <md-table-cell>
                    <div v-if="editMode==false" >
                        {{ entry.virus_type}}
                    </div>
                    <div v-if="editMode==true" class="edit">
                        <md-input class="input" type="text" v-model="entry.virus_type"></md-input>
                    </div>
                </md-table-cell> 
             </md-table-row>

            <md-table-row>
                <md-table-head>Host organism</md-table-head>
                <md-table-cell>
                    <div v-if="editMode==false" >
                        {{ entry.host_organism }}
                    </div>
                    <div v-if="editMode==true" class="edit">
                        <md-input class="input" type="text" v-model="entry.host_organism"></md-input>
                    </div>
                </md-table-cell>
            </md-table-row>

        </md-table>

        <md-button class="md-primary" v-if="this.$store.state.can_verify==true && this.editMode==false" @click="editDetail()">
            Edit
        </md-button>

        <md-button class="md-primary" v-if="this.$store.state.can_verify==true && this.editMode==true" @click="updateDetail()">
            Update
        </md-button>

        <md-button class="md-danger" v-if="this.$store.state.can_verify==true && this.editMode==true" @click="cancelEdit()">
            Cancel
        </md-button>


        <h2 class="title text-center">Metadata</h2>
        <md-table v-if="type=='sra'">


            <md-table-row>
                <md-table-head>NCBI SRA</md-table-head>
                <md-table-cell><p @click="openNCBI()">Click <b>here</b> to see entry in NCBI</p></md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Relsease Date</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.ReleaseDate }}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head>Spots</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.spots }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Experiment</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.Experiment }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Library Name</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.LibraryName }}.1</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Library Strategy</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.LibraryStrategy }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Platform</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.Platform }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>SRA Study</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.SRAStudy }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Run Hash</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.RunHash }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Library Layout</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.LibraryLayout }}</md-table-cell>
            </md-table-row>

        </md-table>


        <md-table v-if="type=='inv'">

            <md-table-row>
                <md-table-head>Project</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.project }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Grapevine cultivar</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.grapevine_cultivar }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Rootstock</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.rootstock }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Plantation year</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.plantation_year}}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Location</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.location}}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Substrate</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.substrate}}</md-table-cell>
            </md-table-row>
            
           
        </md-table>

        <h2 class="title text-center">BLASTX results</h2>
        <md-table >           

            <md-table-row>
                <md-table-head>Taxonomy</md-table-head>
                <md-table-cell >{{ entry.blastx.taxonomy }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Organism</md-table-head>
                <md-table-cell >{{ entry.blastx.organism }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Percent ID</md-table-head>
                <md-table-cell >{{ entry.blastx.percent_idenentity }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Number of reads</md-table-head>
                <md-table-cell >{{ entry.blastx.nb_reads }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Algorithm</md-table-head>
                <md-table-cell>{{ entry.blastx.algo }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Accession</md-table-head>
                <md-table-cell>{{ entry.blastx.accession }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Sequence</md-table-head>
                <md-table-cell>{{ entry.blastx.sequence }}</md-table-cell>
            </md-table-row>

        </md-table>

        <h2 class="title text-center">RPS-BLAST results</h2>
        <md-table >

            <md-table-row>
                <md-table-head >Cdd ID</md-table-head>
                <md-table-cell >{{ entry.blastrps.cdd_id }}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head >Query length</md-table-head>
                <md-table-cell >{{ entry.blastrps.query_length }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Hit ID</md-table-head>
                <md-table-cell>{{ entry.blastrps.hit_id }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Description</md-table-head>
                <md-table-cell class="text-left">{{ entry.blastrps.description }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Evalue</md-table-head>
                <md-table-cell>{{ entry.blastrps.evalue }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Family</md-table-head>
                <md-table-cell>{{ entry.blastrps.family }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Genus</md-table-head>
                <md-table-cell>{{ entry.blastrps.genus }}</md-table-cell>
            </md-table-row>
            
        </md-table>

    </div>
    </div>
  </div>
</template>




<script>
import axios from 'axios';

export default {
  components: {

  },
  name: "entrydetail",
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
        entry: Object,
        editMode: false,
        beforeEditCache: null,
        type: '',
    };
  },
  methods: {
        getDetail(entry_id) {
            axios.get("http://0.0.0.0:9000/api/data/entries/" + entry_id,{
                headers: {
                    'Authorization': 'Token ' + this.$store.state.token
                }
            })
            .then(res => {
                this.entry = res.data
                console.log(this.entry)
                if(this.entry.sra_metadata != null){
                    this.type = 'sra'
                }else{
                    this.type = 'inv'
                }
                })
            .catch(err => console.log(err));
        },

        editDetail(){
            this.editMode = true;
            this.beforeEditCache = Object.assign({}, this.entry); //{verified:entry.verified, virus_type:entry.virus_type, host_type:entry.host_type}
            console.log("CACHE",this.beforeEditCache.verified)
        },

        updateDetail(){//verified, virus_type, host_organism
            this.edited = this.entry;
            console.log("EDITED", this.edited.verified)
            let newData = {'verified':this.edited.verified, 'virus_type':this.edited.virus_type, 'host_organism':this.edited.host_organism}
            axios.patch("http://0.0.0.0:9000/api/data/entries/" + this.$route.params.entry_id + "/", newData,{
                headers: {
                    'Authorization': 'Token ' + this.$store.state.token
                }
            })
            .then(res =>{
                console.log(res)
            })
            .catch(err => {
                console.log(err);
            })
            this.editMode = false

        },

        cancelEdit(){
            this.editMode = false 
            //this.entry = this.beforeEditCache
            Object.assign(this.entry, this.beforeEditCache);
            console.log("CANCELLED", this.entry.verified)
            this.beforeEditCache = null;
        },

        openNCBI(){
            window.open("https://www.ncbi.nlm.nih.gov/sra/" + this.entry.sample, "_blank");    
        }



  },
  created(){
      this.getDetail(this.$route.params.entry_id);
  }
  
};
</script>
<style lang="scss">
.md-table-head{
    width: 100px;
}

.edit{
    display: block;
}

.input{
    width: 200%;
    padding: 12px 20px;
    margin: 8px 0;
    box-sizing: border-box;
}

#check{
  color:  #4caf50;
}
#cross{
    color: red;
}

</style>
