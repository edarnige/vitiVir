<template>
  <div id="blast-form">
    <b-row>
      <b-col md="12" lg="6">
        <b-form-group label-size="sm" label="Program" label-for="programInput">
          <b-form-select
            id="programInput"
            v-model="program"
            size="sm"
            :options="programs"
            required
          ></b-form-select>
        </b-form-group>
      </b-col>
      <b-col md="6" lg="3">
        <b-form-group type="number" label-size="sm" label="E-value" label-for="evalueInput">
          <b-form-input id="evalueInput" v-model="evalue" size="sm" required></b-form-input>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
    </b-row>
    <b-row>
      <b-col md="6" lg="3">
        <b-form-group label-size="sm" label="Max number" label-for="maxNbAlignments">
          <b-form-input
            id="maxNbAlignments"
            v-model="maxNbAlignments"
            type="number"
            size="sm"
          ></b-form-input>
        </b-form-group>
      </b-col>
    </b-row>
    <b-form-group
      label="Sequences (supports multiple sequence, each with a separate FASTA header. Max 50 sequences; 150 000 letters)"
      label-for="sequenceInput"
      label-size="sm"
    >
      <b-form-textarea
        id="sequenceInput"
        ref="sequenceInput"
        v-model="sequences"
        :state="sequencesState"
        size="sm"
        required
        :rows="10"
        :max-rows="10"
        placeholder="Copy paste fasta sequences here"
      ></b-form-textarea>

      <b-form-invalid-feedback id="input-live-feedback">
        Sequences must contain a header line beginning by ">" and can only contain nucleotides or
        amino acids, depending on the selected program.
      </b-form-invalid-feedback>
    </b-form-group>
  </div>
</template>

<script>
export default {
  name: 'BlastForm',
  props: {
    defaultProgram: {
      type: String,
      default: 'blastn',
    },
    defaultEvalue: {
      type: Number,
      default: 1e-10,
    },
    defaultMaxNbAlignments: {
      type: Number,
      default: null,
    },
    defaultSequences: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      programProxy: null,
      evalueProxy: null,
      maxNbAlignmentsProxy: null,
      sequencesProxy: null,
    };
  },
  computed: {
    program: {
      get: function() {
        return this.programProxy == null ? this.defaultProgram : this.programProxy;
      },
      set: function(val) {
        this.programProxy = val;
      },
    },
    evalue: {
      get: function() {
        return this.evalueProxy == null ? this.defaultEvalue : this.evalueProxy;
      },
      set: function(val) {
        this.evalueProxy = val;
      },
    },
    maxNbAlignments: {
      get: function() {
        return this.maxNbAlignmentsProxy == null
          ? this.defaultMaxNbAlignments
          : this.maxNbAlignmentsProxy;
      },
      set: function(val) {
        this.maxNbAlignmentsProxy = val;
      },
    },
    sequences: {
      get: function() {
        return this.sequencesProxy == null ? this.defaultSequences : this.sequencesProxy;
      },
      set: function(val) {
        this.sequencesProxy = val;
      },
    },
    sequencesState() {
      return this.validateMultiFasta(this.sequences);
    },
    form() {
      return {
        program: this.program,
        evalue: this.evalue,
        maxNbAlignments: this.maxNbAlignments,
        sequences: this.sequences,
      };
    },
    /**
     * Set programs for select
     */
    programs() {
      let programs = [
        { text: 'blastn (nucleotide vs nucleotide)', value: 'blastn' },
        { text: 'tblastn (protein vs translated nucleotide)', value: 'tblastn'},
        { text: 'tblastx (translated nucleotide vs translated nucleotide) ', value: 'tblastx'},
      ];

      return programs;
    },
  },
  watch: {
    defaultProgram() {
      this.programProxy = null;
    },
    defaultEvalue() {
      this.evalueProxy = null;
    },
    defaultMaxNbAlignments() {
      this.maxNbAlignmentsProxy = null;
    },
    defaultSequences() {
      this.sequencesProxy = null;
    },
  },
  mounted() {
    this.setDefaults();
  },
  methods: {
    setDefaults() {
      this.program = this.defaultProgram;
      this.evalue = this.defaultEvalue;
      this.maxNbAlignments = this.defaultMaxNbAlignments;
      this.sequences = this.defaultSequences;
    },
    isValid() {
      return this.$refs['sequenceInput'].state == true;
    },
    validateMultiFasta: function(text) {
      text = text.trim();
      if (text[0] != '>') {
        return false;
      }

      var fastas = text.split('>');

      if (fastas.length == 0) {
        return false;
      }

      let flag = true;

      for (let index = 1; index < fastas.length; index++) {
        let f = '>' + fastas[index];
        var bool = this.validateFasta(f);
        if (bool === false) {
          flag = false;
          break;
        }
      }
      return flag;
    },
    /*
     * Validates (true/false) a single fasta sequence string
     * param   fasta    the string containing a putative single fasta sequence
     * returns boolean  true if string contains single fasta sequence, false
     *                  otherwise
     * source :
     */
    validateFasta: function(fasta) {
      if (!fasta) {
        // check there is something first of all
        return false;
      }

      // // immediately remove trailing spaces
      fasta = fasta.trim();

      // split on newlines...
      var lines = fasta.split('\n');

      // check for header
      if (fasta[0] == '>') {
        // remove one line, starting at the first position
        lines.splice(0, 1);
      }

      // join the array back into a single string without newlines and
      // trailing or leading spaces
      fasta = lines.join('').trim();

      if (!fasta) {
        // is it empty whatever we collected ? re-check not efficient
        return false;
      }

      // note that the empty string is caught above
      // allow for Selenocysteine (U)
      if (this.program == 'blastp' || this.program == 'tblastn') {
        return /^[ACDEFGHIKLMNPQRSTUVWY*\s]+$/i.test(fasta);
      } else {
        return /^[ACGTU\s]+$/i.test(fasta);
      }
    },
  },
};
</script>
<style scoped>
#blast-form {
  margin: 10px;
}
</style>
