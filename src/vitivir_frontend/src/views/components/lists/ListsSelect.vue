<template>
  <div>
    <label for="publicSets">{{ computedLabel }}</label>
    <b-form-select
      id="publicSets"
      v-model="selectedSet"
      size="sm"
      :options="sets"
      text-field="selection"
      value-field="id"
      html-field="html"
      :multiple="multiple"
      @input="emitInput"
      @change="emitChange"
    ></b-form-select>
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  props: {
    public: {
      type: Boolean,
      default: true,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: null,
    },
  },
  data: function() {
    return {
      selectedSet: this.multiple ? [null] : null,
    };
  },
  computed: {
    ...mapState(['publicSets', 'userSets']),
    sets: function() {
      return this.public ? this.publicSets : this.userSets;
    },
    computedLabel: function() {
      if (this.label === null) {
        return this.public ? 'Select a public set' : 'Or Select one of your sets';
      } else {
        return this.label;
      }
    },
    isNotEmpty: function() {
      let bool = false;
      if (typeof this.sets != 'undefined') {
        bool = this.sets.length > 0;
      }
      return bool;
    },
  },
  methods: {
    emitInput: function(value) {
      this.$emit('input', value, this.public);
    },
    emitChange: function(value) {
      this.$emit('change', value, this.public);
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
