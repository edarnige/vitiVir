<template>
  <b-form-group :label-size="size" :label="label" :label-for="id">
    <b-form-select
      ref="input"
      :placeholder="placeholder"
      :size="size"
      :id="id"
      :required="required"
      :value="value"
      :readonly="readonly"
      :description="description"
      :options="options"
      @input="update()"
    ></b-form-select>
  </b-form-group>
</template>
<script>
export default {
  name: 'custom-select',
  props: {
    size: {
      type: String,
      default: 'sm',
    },
    options: {
      type: Array,
      default: '',
    },
    id: {
      type: String,
      default: 'customInput',
    },
    value: String,
    label: {
      type: String,
      default: '',
    },
    placeholder: {
      type: String,
      default: '',
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    required: { type: Boolean, default: false },
    description: {
      type: String,
      default: '',
    },
  },
  methods: {
    update() {
      this.$emit('input', this.$refs.input.value);
    },
  },
};
</script>

<style scoped>
</style>
