<template>
  <div>
    <label for="typeSelect">Filter by data type</label>
    <b-form-select
      id="typSelect"
      v-model="selected"
      :options="options"
      size="sm"
      @input="emitInput"
      @change="emitChange"
    ></b-form-select>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selected: null,
      options: [
        {
          value: 0,
          text: 'no filter',
        },
        {
          value: 'protein',
          text: 'protein',
        },
        {
          value: 'CDS',
          text: 'CDS',
        },
        {
          value: 'transcriptome',
          text: 'transcriptome',
        },
        {
          value: 'genomic',
          text: 'genomic',
        },
      ],
    };
  },
  methods: {
    emitInput: function(value) {
      this.$emit('input', value);
    },
    emitChange: function(value) {
      this.$emit('change', value);
    },
  },
};
</script>

<style scoped>
select {
  width: 200px;
}

label {
  margin-bottom: 0px;
  font-size: 12px;
}
</style>
