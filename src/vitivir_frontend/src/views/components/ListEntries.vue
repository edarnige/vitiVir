<template>
    <div>

        <ul id="entriesList">

          <li v-for="entry in entries" v-bind:key="entry.entry_id">
            {{ entry.query_id }}
          </li>
        </ul>


        <p v-bind:key="entry.entry_id" v-for="entry in entries">
            {{entry.query_id}}
       </p>
   </div>


</template>


<script>
import axios from 'axios';


export default {
  name: 'entries',
  components: {

  },
  data() {
    return {
      entries : [],
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