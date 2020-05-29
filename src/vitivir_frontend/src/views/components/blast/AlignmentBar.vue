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

<style lang="scss">
.tooltip {
  display: block !important;
  z-index: 10000;
  width: auto;
}

.tooltip .tooltip-inner {
  text-align: left;
  background: white;
  color: steelblue;
  border-radius: 16px;
  border-style: solid;
  border-color: royalblue;
  padding: 5px 10px 4px;
}

.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: black;
  z-index: 1;
}

.tooltip[x-placement^='top'] {
  margin-bottom: 5px;
}

.tooltip[x-placement^='top'] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^='bottom'] {
  margin-top: 5px;
}

.tooltip[x-placement^='bottom'] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^='right'] {
  margin-left: 5px;
}

.tooltip[x-placement^='right'] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip[x-placement^='left'] {
  margin-right: 5px;
}

.tooltip[x-placement^='left'] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip.popover .popover-inner {
  background: #f9f9f9;
  color: black;
  padding: 24px;
  border-radius: 5px;
  box-shadow: 0 5px 30px rgba(black, 0.1);
}

.tooltip.popover .popover-arrow {
  border-color: #f9f9f9;
}

.tooltip[aria-hidden='true'] {
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.15s, visibility 0.15s;
}

.tooltip[aria-hidden='false'] {
  visibility: visible;
  opacity: 1;
  transition: opacity 0.15s;
}
</style>