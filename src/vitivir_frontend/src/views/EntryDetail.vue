<template>
  <div class="wrapper">
      <div class="section section-basic">  
      <div class="md-layout-item md-size-90">

        <md-button class="md-simple md-primary md-lg" @click="goBack()">Back</md-button>

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
                <md-table-head>Bases</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.bases }}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head>Average Length</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.avgLength }}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head>Size MB</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.size_MB }}</md-table-cell>
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
                <md-table-head>Library Selection</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.LibrarySelection }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Library Layout</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.LibraryLayout }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Platform</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.Platform }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Model</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.Model }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>SRA Study</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.SRAStudy }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Bio Project</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.BioProject }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Sample</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.Sample }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Bio Sample</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.BioSample }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Tax ID</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.TaxID }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Scientific Name</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.ScientificName }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Sample Name</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.SampleName }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Center Name</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.CenterName }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Submission</md-table-head>
                <md-table-cell>{{ entry.sra_metadata.Submission }}</md-table-cell>
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

            <md-table-row>
                <md-table-head>Extraction method</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.extraction_method}}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Organ</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.organ}}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head>Run Name</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.run_name}}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Technology</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.technology}}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head>Run ID</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.run_id}}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Date</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.date}}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Sequencing location</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.seq_location}}</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head>RNA</md-table-head>
                <md-table-cell>{{ entry.inv_metadata.rna}}</md-table-cell>
            </md-table-row>
            
        </md-table>

        <h2 class="title text-center" v-if="entry.blastx">BLASTX results</h2>
        <md-table v-if="entry.blastx">           

            <md-table-row>
                <md-table-head>Taxonomy</md-table-head>
                <md-table-cell >{{ entry.blastx.taxonomy }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Number of Reads</md-table-head>
                <md-table-cell >{{ entry.blastx.nb_reads }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Accession</md-table-head>
                <md-table-cell>{{ entry.blastx.accession }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Description</md-table-head>
                <md-table-cell>{{ entry.blastx.description }}</md-table-cell>
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
                <md-table-head>Number of Hsps</md-table-head>
                <md-table-cell >{{ entry.blastx.nb_hsps }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Query Overlap</md-table-head>
                <md-table-cell >{{ entry.blastx.query_overlap }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Hit Overlap</md-table-head>
                <md-table-cell >{{ entry.blastx.hit_overlap }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Evalue</md-table-head>
                <md-table-cell >{{ entry.blastx.evalue }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Score</md-table-head>
                <md-table-cell >{{ entry.blastx.score }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Tax ID</md-table-head>
                <md-table-cell >{{ entry.blastx.tax_id }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Algorithm</md-table-head>
                <md-table-cell>{{ entry.blastx.algo }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Sequence</md-table-head>
                <md-table-cell>{{ entry.blastx.sequence }}</md-table-cell>
            </md-table-row>

        </md-table>

        <h2 class="title text-center" v-if="entry.blastrps">RPS-BLAST results</h2>
        <md-table v-if="entry.blastrps">

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
                <md-table-head>Evalue</md-table-head>
                <md-table-cell>{{ entry.blastrps.evalue }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>StartQ</md-table-head>
                <md-table-cell>{{ entry.blastrps.startQ }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>EndQ</md-table-head>
                <md-table-cell>{{ entry.blastrps.endQ }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Frame</md-table-head>
                <md-table-cell>{{ entry.blastrps.frame }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Description</md-table-head>
                <md-table-cell class="text-left">{{ entry.blastrps.description }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Super Kingdom</md-table-head>
                <md-table-cell>{{ entry.blastrps.superkingdom }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>No Rank</md-table-head>
                <md-table-cell>{{ entry.blastrps.no_rank }}</md-table-cell>
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
            this.$Progress.start()
            axios.get(`${process.env.VUE_APP_API_HOST}/api/data/entries/` + entry_id,{
                headers: {
                    'Authorization': 'Token ' + this.$store.state.token
                }
            })
            .then(res => {
                this.$Progress.finish()
                this.entry = res.data
                console.log(this.entry)
                if(this.entry.sra_metadata != null){
                    this.type = 'sra'
                }else{
                    this.type = 'inv'
                }
                })
            .catch(err => {
                this.$Progress.fail()
                console.log(err)
                })
        },

        editDetail(){
            this.editMode = true;
            this.beforeEditCache = Object.assign({}, this.entry); //{verified:entry.verified, virus_type:entry.virus_type, host_type:entry.host_type}
            console.log("CACHE",this.beforeEditCache.verified)
        },

        updateDetail(){//verified, virus_type, host_organism
            this.$Progress.start()
            this.edited = this.entry;
            console.log("EDITED", this.edited.verified)
            let newData = {'verified':this.edited.verified, 'virus_type':this.edited.virus_type, 'host_organism':this.edited.host_organism}
            axios.patch(`${process.env.VUE_APP_API_HOST}/api/data/entries/` + this.$route.params.entry_id + "/", newData,{
                headers: {
                    'Authorization': 'Token ' + this.$store.state.token
                }
            })
            .then(res =>{
                this.$Progress.finish()
                console.log(res)
            })
            .catch(err => {
                this.$Progress.fail()
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
        },

        goBack(){
            this.$router.push('/search');
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
