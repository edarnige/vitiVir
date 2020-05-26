<template>
  <svg width="100%" height="25px">
    <g class="color5">
      <rect x="0" y="0" width="100%" height="15px"></rect>
      <text x="45%" y="10" fill="white" font-weight="bold" font-size="10">{{ queryStr }}</text>
      <text
        v-for="(label) in labels"
        :key="label.id"
        :x="label.pos"
        y="25"
        fill="black"
        font-size="10"
      >{{label.label}}</text>
    </g>
  </svg>
</template>

<script>
export default {
  name: "blast-query-bar",

  props: {
    length: { type: Number, default: 100 },
    text: { type: String, default: "query" }
  },
  computed: {
    queryStr: function() {
      return this.text;
    },
    labels: function() {
      let a_labels = [{ id: 0, label: "0", pos: "0%" }];

      for (let i = 1; i < 4; i++) {
        a_labels.push({
          id: i,
          label: Math.round(this.length * 0.25 * i),
          pos: 25 * i + "%"
        });
      }

      a_labels.push({
        id: 4,
        label: this.length,
        pos: "97%"
      });

      return a_labels;
    }
  }
};
</script>

