<template>
  <svg width="100%" v-tooltip="msg" :class="[color]">
    <rect :x="marginLeft" :y="marginTop" :width="width" :height="height" fill-opacity="0.8"></rect>
  </svg>
</template>

<script>
export default {
  name: "alignment-bar",

  props: {
    score: { type: Number, default: 0 },
    evalue: { type: Number, default: 0 },
    mode: { type: Number, default: 1 }, // 0:e-value, 1:max score
    queryLength: { type: Number, default: 0 },
    alignmentLength: { type: Number, default: 0 },
    alignmentPos: { type: Number, default: 1 },
    rowNumber: { type: Number, default: 1 },
    height: { type: Number, default: 20 },
    space: { type: Number, default: 5 },
    accession: { type: String, default: "alignment" },
    def: { type: String, default: "" }
  },

  data: function() {
    return { styleBar: {} };
  },
  computed: {
    marginLeft: function() {
      return (this.alignmentPos / this.queryLength) * 100 + "%";
    },
    width: function() {
      return (this.alignmentLength / this.queryLength) * 100 + "%";
    },
    msg: function() {
      return (
        "<strong>" +
        this.accession +
        "</strong>" +
        "<br />" +
        this.def +
        "<br /><strong>Score:</strong>" +
        this.score +
        "<br /><strong>evalue:</strong>" +
        this.evalue +
        "<br /><strong>from:</strong>" +
        this.alignmentPos +
        "<br /><strong>to:</strong>" +
        (this.alignmentPos + this.alignmentLength - 1)
      );
    },
    color: function() {
      let colorNb;
      if (this.mode === 0) {
        if (this.evalue > 100) {
          colorNb = 1;
        } else if (this.evalue <= 100 && this.evalue > 1) {
          colorNb = 2;
        } else if (this.evalue <= 1 && this.evalue > 0.01) {
          colorNb = 3;
        } else if (this.evalue <= 0.01 && this.evalue > 0.00001) {
          colorNb = 4;
        } else {
          colorNb = 5;
        }
      } else {
        if (this.score < 40) {
          colorNb = 1;
        } else if (this.score >= 40 && this.score < 50) {
          colorNb = 2;
        } else if (this.score >= 50 && this.score < 80) {
          colorNb = 3;
        } else if (this.score >= 80 && this.score < 200) {
          colorNb = 4;
        } else {
          colorNb = 5;
        }
      }

      return "color" + colorNb;
    },
    marginTop: function() {
      return (
        (this.rowNumber - 1) * (this.height + this.space) +
        this.height +
        this.space +
        "px"
      );
    }
  },

  methods: {}
};
</script>

