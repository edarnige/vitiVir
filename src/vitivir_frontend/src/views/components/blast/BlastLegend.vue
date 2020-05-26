<template>
  <svg width="100%" height="20px">
    <g class="color1">
      <rect x="0" y="0" width="20%" height="20px"></rect>
      <text x="5%" y="15" font-size="15" font-weight="bold" fill="white">{{ legend[0] }}</text>
    </g>
    <g class="color2">
      <rect x="20%" y="0" width="20%" height="20px"></rect>
      <text x="25%" y="15" font-size="15" font-weight="bold" fill="white">{{ legend[1] }}</text>
    </g>
    <g class="color3">
      <rect x="40%" y="0" width="20%" height="20px"></rect>
      <text x="45%" y="15" font-size="15" font-weight="bold" fill="white">{{ legend[2] }}</text>
    </g>
    <g class="color4">
      <rect x="60%" y="0" width="20%" height="20px"></rect>
      <text x="65%" y="15" font-size="15" font-weight="bold" fill="white">{{ legend[3] }}</text>
    </g>
    <g class="color5">
      <rect x="80%" y="0" width="20%" height="20px"></rect>
      <text x="85%" y="15" font-size="15" font-weight="bold" fill="white">{{ legend[4] }}</text>
    </g>
  </svg>
</template>

<script>
export default {
  name: "blast-legend",

  props: {
    mode: { type: Number, default: 1 } // 0:e-value, 1:max score
  },

  computed: {
    legend: function() {
      return this.mode
        ? ["<40", "40-50", "50-80", "80-200", ">=200"]
        : [">100", "100-1", "1-1e-2", "1e-2-1e-5", "<1e-5"];
    }
  }
};
</script>

<style scoped>
</style>