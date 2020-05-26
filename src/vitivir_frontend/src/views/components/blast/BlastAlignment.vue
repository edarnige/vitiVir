<template>
  <div class="blast-alignment">
    <b-form-select
      v-if="hsps && hsps.length > 1"
      id="selectHsps"
      size="sm"
      :options="hsps"
      :value="hspSelected"
      @input="changeHsp"
    ></b-form-select>
    <br />
    <br />
    <h6>
      <strong>Subject:</strong>
      {{ hsp['accession'] }}
    </h6>
    <b-row>
      <b-col>
        <strong>Score:</strong>
        {{ hsp['bit-score'] }}
      </b-col>
      <b-col>
        <strong>E-value:</strong>
        {{ hsp['evalue'] }}
      </b-col>
      <b-col>
        <strong>Identities:</strong>
        {{ hsp['identity-per'] }} %
      </b-col>
      <b-col>
        <strong>Positives:</strong>
        {{ hsp['positive-per'] }} %
      </b-col>
      <b-col>
        <strong>Gaps:</strong>
        {{ hsp['gaps-per'] }} %
      </b-col>
    </b-row>
    <br />
    <div class="alignment-svg">
      <svg :width="svgWidth" :height="svgHeight">
        <svg>
          <g>
            <text x="5" y="15" font-size="15" font-weight="bold" fill="black">Query</text>
            <text x="65" y="15" font-size="15" font-weight="bold" fill="black">
              {{ hsp['query-from'] }}
            </text>
            <template v-for="letter in lettersQuery">
              <alignment-letter
                :key="letter.id"
                :width="letterWidth"
                :padding="letterPadding"
                :offsetX="100"
                :pos="letter.id"
              >
                {{ letter.value }}
              </alignment-letter>
            </template>
          </g>
        </svg>
        <svg>
          <g>
            <template v-for="letter in lettersMiddle">
              <alignment-letter
                :key="letter.id"
                :width="letterWidth"
                :padding="letterPadding"
                :offsetX="100"
                :offsetY="letterWidth + 2 * letterPadding"
                :pos="letter.id"
              >
                {{ letter.value }}
              </alignment-letter>
            </template>
          </g>
        </svg>
        <svg>
          <g>
            <text
              x="5"
              :y="3 * (letterWidth + 2 * letterPadding) - letterPadding"
              font-size="15"
              font-weight="bold"
              fill="black"
            >
              Subject
            </text>
            <text
              x="65"
              :y="3 * (letterWidth + 2 * letterPadding) - letterPadding"
              font-size="15"
              font-weight="bold"
              fill="black"
            >
              {{ hsp['hit-from'] }}
            </text>
            <template v-for="letter in lettersSubject">
              <alignment-letter
                :key="letter.id"
                :width="letterWidth"
                :padding="letterPadding"
                :offsetX="100"
                :offsetY="2 * (letterWidth + 2 * letterPadding)"
                :pos="letter.id"
                :height="letterWidth"
              >
                {{ letter.value }}
              </alignment-letter>
            </template>
          </g>
        </svg>
      </svg>
    </div>
  </div>
</template>

<script>
const OFFSET = 100;

import AlignmentLetter from '@/views/components/blast/AlignmentLetter.vue';

export default {
  name: 'BlastAlignment',
  components: {
    AlignmentLetter,
  },
  props: {
    jsonData: {
      type: Object,
      default: () => {
        return {};
      },
    },
    query: { type: String, default: '' },
    dbType: { type: String, default: '' },
    subject: { type: String, default: '' },
    letterWidth: { type: Number, default: 15 },
    letterPadding: { type: Number, default: 3 },
  },
  data: () => {
    return { hsp: {} };
  },
  computed: {
    /*eslint-disable */
    //Unexpected side effect in "hspSelected" computed property 
    lettersQuery() {
      let i = 0;
      if (this.hspSelected.qseq) {
        return this.hsp.qseq.split('').map(l => {
          i++;
          return { value: l, id: i };
        });
      } else {
        return [];
      }
    },
    lettersMiddle() {
      let i = 0;
      if (this.hspSelected.midline) {
        return this.hsp.midline.split('').map(l => {
          i++;
          return { value: l, id: i };
        });
      } else {
        return [];
      }
    },
    lettersSubject() {
      let i = 0;
      if (this.hspSelected.hseq) {
        return this.hsp.hseq.split('').map(l => {
          i++;
          return { value: l, id: i };
        });
      } else {
        return [];
      }
    },
    svgWidth() {
      return this.hspSelected.qseq
        ? OFFSET + (2 * this.letterPadding + this.letterWidth) * this.hspSelected.qseq.length + 100
        : OFFSET * 2;
    },
    svgHeight() {
      return this.hspSelected.qseq ? this.letterWidth * 3 + 6 * this.letterPadding : 100;
    },

    hsps() {
      let hsps = [];
      if (this.jsonData.iterations && this.query !== '') {
        this.jsonData.iterations.forEach(iteration => {
          let queryId = iteration['query-def'];
          if (queryId === this.query) {
            let a_hits = iteration['hits'];
            a_hits.forEach(hit => {
              let acc = hit['accession'];
              if (acc === this.subject) {
                hit['hsps'].forEach(hsp => {
                  let identity = parseInt(hsp['identity']);
                  let alignLen = parseInt(hsp['align-len']);
                  let positive = parseInt(hsp['positive']);
                  let gaps = parseInt(hsp['gaps']);

                  hsp['identity-per'] = Math.round((identity / alignLen) * 100);
                  hsp['positive-per'] = Math.round((positive / alignLen) * 100);
                  hsp['gaps-per'] = Math.round((gaps / alignLen) * 100);
                });
                hsps = hit['hsps'].map(h => ({
                  value: h,
                  text: 'Hsp ' + h.num,
                }));
              }
            });
          }
        });
      }
      return hsps;
    },
    hspSelected: {
      get: function() {
        let val = this.hsps.length > 0 ? this.hsps[0].value : null;
        this.hsp = val;
        return val;
      },
      set: function() {},
    },
    /*eslint-enable */
  },
  methods: {
    changeHsp: function(v) {
      this.hsp = v;
    },
  },
};
</script>

<style scoped>
.blast-alignment {
  border: thin solid rgb(221, 221, 221);
  padding: 10px;
  min-width: 400px;
  margin: 50px 0px 50px 0px;
}

.alignment-svg {
  height: auto;
  padding: 5px 0px 5px 0px;
  overflow-x: scroll;
}
</style>
