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
                <md-input v-model="sample"></md-input>
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

          <!-- </div> -->
        <!-- </div> -->


    <!-- Results -->

        <div class="section section-basic">
          <!-- <div class="container"> -->
              
              <div class="title">
                <h2>Results</h2>
              </div>
            
            <div>
              <ListEntries/>
            </div>
          
          </div>

      </div>
    </div>
  </div>
</template>

<script>
import ListEntries from '@/views/components/ListEntries.vue'

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
      exclude: null,
      verified: false,
      sample: null,
      host: null,
      vtype: null,
      startDate: null,
      endDate: null,
      order: null,

    };
  },
  methods: {

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
