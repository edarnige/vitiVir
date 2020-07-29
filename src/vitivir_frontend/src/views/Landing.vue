<template>
  <div class="wrapper">
    <parallax class="section page-header header-filter" :style="headerStyle">
      <div class="container">
        <div class="md-layout">
          <div
            class="md-layout-item md-size-50 md-small-size-70 md-xsmall-size-100"
          >
            <h1 class="title">VitiVir Database</h1>
            <h4 id="subtitle">
              A web mining tool to analyze the phytovirus and mycovirus diversity of grapevine. 
              Login to access the search utility.
            </h4>
            <br />
            <md-button
              class="md-primary md-lg"
              @click="canSearch()"
              >Search</md-button>
            <p id="photo-cred">
            Photo by Dario Krejci
            </p>
          </div>
        </div>
      </div>
    </parallax>
    <div class="main main-raised">
      <div class="section">
        <div class="container">
          <div class="md-layout">
            <div
              class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto text-center"
            >
              <h2 class="title text-center">About the database</h2>
              <h5 class="description">
                Project 
                <a href="https://www.plan-deperissement-vigne.fr/recherches/programmes-de-recherche/mycovir"> MYCOVIR </a>
                is a collaboration between multiple research units of the INRAE 
                and the IFV. The objective of project MYCOVIR is to determine the diversity and 
                interactions of viral and fungal communities associated with grapevine trunk diseases.
                In a similar light, the InViCeB project aims to take virologic inventory of Bordeaux grape varieties.
                Grapevine associated raw RNA-seq data from NCBI's publically available SRA as well as data from project InViCeB 
                were analyzed via the 
                <a href="https://apsjournals.apsnet.org/doi/full/10.1094/PBIOMES-07-19-0037-A">
                  VirAnnot pipeline</a>, 
                as developped by Marie Lefebvre and Sebastien Thiel within the INRAE  UMR 1332 BFP 
                plant virology etiology team. The resulting taxonomic classifications were stored in
                the VitiVir database and can be mined in this web tool.
              </h5>
            </div>
          </div>
          <div class="features text-center">
            <div class="md-layout">
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                  <i class="fas fa-viruses"></i>
                  <h4 class="info-title">Virus data</h4>
                  <p>
                    While the focus of project MYCOVIR targets mycoviruses, 
                    grapevine associated phytoviruses and bacteriophages are also 
                    present in the VitiVir database.
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                    <i class="fas fa-user-check"></i>
                  <h4 class="info-title">Verified users</h4>
                  <p>
                    Database access is restricted to INRAE UMR 1332 researchers 
                    and MYCOVIR partners. Only MYCOVIR project directors can verify
                    taxonomy, host organism, and virus type of an entry. 
                  </p>
                </div>
              </div>
              <div class="md-layout-item md-medium-size-33 md-small-size-100">
                <div class="info">
                  <md-button id="blast-button" class="md-simple" @click="$router.push('/blast');">
                    <i class="fas fa-file-upload"></i>
                  </md-button>
                  <h4 class="info-title">BLAST portal</h4>
                  <p>
                    Enter your grapevine-associated viral fasta sequences to run BLASTN, TBLASTN, 
                    or TBLASTX against the VitiVir viral sequence database. 
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>


      <div class="section section-contacts">
        <div class="container">
          <div class="md-layout">
            <div class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto">
              <h2 class="text-center title">Database statistics</h2>
              <h4 class="text-center description">
                Current counts:
                <div>
                  <span class="purple">{{total_entries}} </span> total entries 
                </div>
                <div>
                  <span class="purple">{{sra_count}}</span> SRA samples | <span class="purple">{{inv_count}}</span> InViCeB samples 
                </div>
                <div>
                  <span class="purple"> {{seq_count}} </span> viral sequences 
                </div>
              </h4>   
                <div>
                  <highcharts v-if="chartOptions_fam.series[0].data.length > 0 " class="hc" :options="chartOptions_fam" ref="chart"></highcharts>
                </div>                         
                <div>
                  <highcharts v-if="chartOptions_vir.series[0].data.length > 0 " class="hc" :options="chartOptions_vir" ref="chart"></highcharts>
                </div>                         

            </div>
          </div>
        </div>
      </div>



      <div class="section section-contacts">
        <div class="container">
          <div class="md-layout">
            <div class="md-layout-item md-size-66 md-xsmall-size-100 mx-auto">
              <h2 class="text-center title">Contact</h2>
              <h4 class="text-center description">
                Feel free to reach out with any comments or questions. We will get back 
                to you as soon as possible.
              </h4>
              <form class="contact-form">
                <div class="md-layout">
                  <div class="md-layout-item md-size-50">
                    <md-field>
                      <label>Your Name</label>
                      <md-input v-model="name" type="text"></md-input>
                    </md-field>
                  </div>
                  <div class="md-layout-item md-size-50">
                    <md-field>
                      <label>Your Email</label>
                      <md-input v-model="email" type="email"></md-input>
                    </md-field>
                  </div>
                </div>
                <md-field>
                  <label>Your Message</label>
                  <md-textarea v-model="message"></md-textarea>
                </md-field>
                <div class="md-layout">
                  <div class="md-layout-item md-size-33 mx-auto text-center">
                    <md-field>
                      <label>What is {{x}} + {{y}}</label>
                      <md-input v-model="answer" type="email"></md-input>
                    </md-field>
                    <md-button @click="sendContact()" :disabled="x + y != answer" class="md-primary">Send Message</md-button>
                  </div>
                </div>
              </form>
                            
                            
              <img src="@/assets/img/logos.png" alt="">

            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {Chart} from 'highcharts-vue'
//import { chart } from 'highcharts';
//import exportingInit from 'highcharts/modules/exporting'


function getRandomInt(max) {
  return Math.floor(Math.random() * Math.floor(max));
}
export default {
  bodyClass: "landing-page",
  components: {
    highcharts: Chart,
  },
  props: {
    header: {
      type: String,
      default: require("@/assets/img/vineyard.jpeg")
    },

  },

  data() {
    return {
      name: null,
      email: null,
      message: null,
      x: getRandomInt(10),
      y: getRandomInt(10),
      answer: 0,

      total_entries: null,
      sra_count: null,
      inv_count: null,
      seq_count: null,

      chartOptions_fam: {
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false,
          type: 'pie'
        },
        title:{
          text: 'Taxonomic families represented in VitiVir'
        },
        subtitle: {
          text: 'From all entries excluding Vitaceae'
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        series: [
          {
            name: 'Value',
            colorByPoint: true,
            data: []
          }
        ]
      },

      chartOptions_vir:{
        chart: {
          type: 'pie'
        },
        title: {
          text: 'Viruses represented in VitiVir'
        },
        subtitle: {
          text: 'ssRNA, dsRNA, or orther genome types and corresponding families'
        },
        tooltip: {
          pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
        },
        series: [{
          name: 'Genome type',
          data: [],
          size: '60%',
          dataLabels: {
              formatter: function () {
                  return this.y > 1 ? this.point.name : null;
              },
              color: '#ffffff',
              distance: -30
          }
      }, {
          name: 'Family',
          data: [],
          size: '80%',
          innerSize: '60%',
          dataLabels: {
              formatter: function () {
                  // display only if larger than 1
                  return this.y > 0 ? '<b>' + this.point.name + ':</b> ' +
                      this.y.toFixed(2) + '%' : null;
              }
          },
          id: 'versions'
    }],

      }

    };
  },

  computed: {
    headerStyle() {
      return {
        backgroundImage: `url(${this.header})`
      };
    }
  },

  methods: {
    canSearch(){
      if(this.$store.state.token != null){
        this.$router.push('/search')
      }
      else{
        this.$router.push('/login')
      }
    },
    async sendContact() {
      const data = {
        'name': this.name,
        'email': this.email,
        'message': this.message
      }

      await axios.post(`${process.env.VUE_APP_API_HOST}/api/contact/`, data); //once done then...
      alert('sent');
      this.name = '';
      this.email = '';
      this.message = '';
      this.answer = 0;
    },
    getStats(){
      axios.get(`${process.env.VUE_APP_API_HOST}/stats/`)
      .then(res=> {
        console.log(res)

        //vitivir in numbers
        this.total_entries = res.data.total
        this.sra_count = res.data.SRA_count
        this.inv_count = res.data.INV_count
        this.seq_count = res.data.viral_seq_count

        //families chart
        this.chartOptions_fam.series[0].data = res.data.families

        //virus chart
        let data = res.data.viruses
        let genome_type_data = [] //browserData
        let virus_family_data = [] //versionsData
        let dataLen = data.length
        let categories = [
				'ssRNA',
        'dsRNA',
        'Other (ssDNA, retro-transcribing, etc.)'
      ]


        // Build the data arrays for virus donut chart
        for (let i = 0; i < dataLen; i += 1) {

            // add genome type data
            genome_type_data.push({
                name: categories[i],
                y: data[i].y,
                color: data[i].color
            });

            // add virus family data
            let drillDataLen = data[i].drilldown.data.length;
            for (let j = 0; j < drillDataLen; j += 1) {
                //let brightness = 0.2 - (j / drillDataLen) / 5;
                virus_family_data.push({
                    name: data[i].drilldown.categories[j],
                    y: data[i].drilldown.data[j]*data[i].y,
                    color: data[i].color + "80"
                    //color: Highcharts.color(data[i].color).brighten(brightness).get() //not working
                    //color: this.chartOptions_vir.series[0].color
                });
            }
        }
        this.chartOptions_vir.series[0].data = genome_type_data
        this.chartOptions_vir.series[1].data = virus_family_data

      })
      .catch(err => {
        console.log(err);
      })
    }

  },
  created(){
      this.getStats();
  }
};
</script>

<style lang="scss" scoped>
.md-card-actions.text-center {
  display: flex;
  justify-content: center !important;
}
.contact-form {
  margin-top: 30px;
}
.md-has-textarea + .md-layout {
  margin-top: 15px;
}
.fa-viruses{
  color: #f57c00;
  font-size: 3em;
}
.fa-user-check{
  color: #4caf50;
  font-size: 3em;
}
.fa-file-upload{
  color: #2196f3;
  font-size: 3em;
}
#subtitle{
  font-weight: bold;
  text-shadow: 2px 2px 3px rgba(0,0,0,0.3);
}
#photo-cred{
  padding-top:30px;
  font-size: 0.5em;
}
#blast-button{
  margin: -5px;
}
img{
  padding-top: 100px;
}
.section-contacts{
  margin-top: -100px;
}
.purple{
  color:#4a148c;
  font-weight: bold;
  
}

</style>
