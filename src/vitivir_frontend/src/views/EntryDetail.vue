<template>
  <div class="wrapper">
      <div class="section section-basic">  
      <div class="md-layout-item md-size-90">

        <md-button class="md-simple md-primary md-lg">Back</md-button>

        <h2 class="title text-center">Entry information</h2>
        <md-table >

            <md-table-row>
                <md-table-head >Query ID</md-table-head>
                <md-table-cell >SRR10518885_0</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head >Sample</md-table-head>
                <md-table-cell >SRR10518885</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Verified</md-table-head>
                <md-table-cell>False</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Virus type</md-table-head>
                <md-table-cell>-</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Host organism</md-table-head>
                <md-table-cell>-</md-table-cell>
            </md-table-row>

        </md-table>

        <md-button class="md-primary">Update</md-button>


        <h2 class="title text-center">Metadata</h2>
        <md-table >

            <md-table-row>
                <md-table-head>Relsease Date</md-table-head>
                <md-table-cell>11/23/19 10:55</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head>Spots</md-table-head>
                <md-table-cell>23900218</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Experiment</md-table-head>
                <md-table-cell>SRX7203860</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>LibraryName</md-table-head>
                <md-table-cell>berry_EE_4.1</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>LibraryStrategy</md-table-head>
                <md-table-cell>RNA-Seq</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Platform</md-table-head>
                <md-table-cell>ILLUMINA</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>SRAStudy</md-table-head>
                <md-table-cell>SRP231551</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>RunHash</md-table-head>
                <md-table-cell>0515A8E804B22D0DD3DB2E54624CE5F6</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>LibraryLayout</md-table-head>
                <md-table-cell>PAIRED</md-table-cell>
            </md-table-row>

        </md-table>

        <h2 class="title text-center">BLASTX results</h2>
        <md-table >           

            <md-table-row>
                <md-table-head>Number of reads</md-table-head>
                <md-table-cell >2548</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head >Query length</md-table-head>
                <md-table-cell >7005</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Algorithm</md-table-head>
                <md-table-cell>BLASTX</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Accession</md-table-head>
                <md-table-cell>KDP44557</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Sequence</md-table-head>
                <md-table-cell>ATGCGGGGGGTATATTAGATGATGTACGTCGCTGACTGATACGCTCAGCTAGCATCAGTCAGACTGCATCAGTCAGACTGCAGCAGCAGTTCGATCAGCAGTTACGTCGTCAGTCAGGCGACTGCATCATGCAGTCAGTCATGACTGTCAGTCATGCAGTCATGACTGTTGCGT</md-table-cell>
            </md-table-row>

        </md-table>

        <h2 class="title text-center">RPS-BLAST results</h2>
        <md-table >

            <md-table-row>
                <md-table-head >Number of reads</md-table-head>
                <md-table-cell >2548</md-table-cell>
            </md-table-row>
            
            <md-table-row>
                <md-table-head >Query length</md-table-head>
                <md-table-cell >7005</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Algorithm</md-table-head>
                <md-table-cell>BLASTX</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Accession</md-table-head>
                <md-table-cell>KDP44557</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Evalue</md-table-head>
                <md-table-cell>3.1e-89</md-table-cell>
            </md-table-row>

            <md-table-row>
                <md-table-head>Description</md-table-head>
                <md-table-cell>hypothetical protein JCGZ_16390 [Jatropha curcas]</md-table-cell>
            </md-table-row>
            
        </md-table>



 
            
        




    </div>
    </div>
  </div>
</template>




<script>

export default {
  components: {

  },
  name: "entrydetail",
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

    };
  },
  methods: {

  },
  
};
</script>
<style lang="scss">
.md-table-head{
    width: 100px;
}
</style>
