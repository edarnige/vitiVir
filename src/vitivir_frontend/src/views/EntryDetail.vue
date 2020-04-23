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
                <md-table-cell>{{ entry.verified }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Virus type</md-table-head>
                <md-table-cell>{{ entry.virus_type }}</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Host organism</md-table-head>
                <md-table-cell>{{ entry.host_organism }}</md-table-cell>
            </md-table-row>

        </md-table>

        <md-button class="md-primary">Update</md-button>


        <h2 class="title text-center">Metadata</h2>
        <md-table >

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
import { TokenService } from '@/storage/service.js'

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
        user: Object,
        token: TokenService.getToken() || null,
    };
  },
  methods: {
        getDetail(entry_id) {
            axios.get("http://0.0.0.0:9000/api/data/entries/" + entry_id,{
                headers: {
                    'Authorization': 'Token ' + this.token
                }
            })
            .then(res => (this.entry = res.data))
            .catch(err => console.log(err));
    },
        getUser(){
            axios.get("http://0.0.0.0:9000/users/createuser")
            .then(res => (this.user = res.data))
            .catch(err => console.log(err));
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
</style>
