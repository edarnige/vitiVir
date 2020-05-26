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
        <b-form-group label-size="sm" label="Filter" label-for="filterInput">
          <b-form-checkbox
            id="checkbox1"
            v-model="filter"
            size="sm"
            value="true"
            unchecked-value="false"
          ></b-form-checkbox>
        </b-form-group>
      </b-col>
      <b-col md="6" lg="3">
        <b-form-group type="number" label-size="sm" label="E-value" label-for="evalueInput">
          <b-form-input id="evalueInput" v-model="evalue" size="sm" required></b-form-input>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="12" lg="4">
        <b-form-group label-size="sm" label="Database Type" label-for="dbTypeInput">
          <b-form-select
            id="dbTypeInput"
            v-model="db"
            size="sm"
            :options="dbTypes"
            required
            @change="emitChangeDbType"
          ></b-form-select>
        </b-form-group>
      </b-col>
      <b-col md="6" lg="4">
        <b-form-group label-size="sm" label="Matrix" label-for="matrixInput">
          <b-form-select
            id="matrixInput"
            v-model="matrix"
            size="sm"
            :options="matrices"
            :disabled="disableMatrix"
          ></b-form-select>
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6" lg="3">
        <b-form-group label-size="sm" label="Word size" label-for="wordSizeInput">
          <b-form-input
            id="wordSizeInput"
            v-model="wordSize"
            type="number"
            size="sm"
          ></b-form-input>
        </b-form-group>
      </b-col>
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
    dbType: {
      type: String,
      default: null,
    },
    defaultProgram: {
      type: String,
      default: 'blastn',
    },
    defaultFilter: {
      type: Boolean,
      default: true,
    },
    defaultEvalue: {
      type: Number,
      default: 1e-10,
    },
    defaultDb: {
      type: String,
      default: 'CDS',
    },
    defaultMatrix: {
      type: String,
      default: 'BLOSUM62',
    },
    defaultWordSize: {
      type: Number,
      default: null,
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
      matrices: [
        { text: 'BLOSUM45', value: 'BLOSUM45' },
        { text: 'BLOSUM50', value: 'BLOSUM50' },
        { text: 'BLOSUM62', value: 'BLOSUM62' },
        { text: 'BLOSUM80', value: 'BLOSUM80' },
        { text: 'BLOSUM90', value: 'BLOSUM90' },
        { text: 'PAM250', value: 'PAM250' },
        { text: 'PAM30', value: 'PAM30' },
        { text: 'PAM70', value: 'PAM70' },
      ],
      programProxy: null,
      filterProxy: null,
      evalueProxy: null,
      dbProxy: null,
      matrixProxy: null,
      wordSizeProxy: null,
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
    filter: {
      get: function() {
        return this.filterProxy == null ? this.defaultFilter : this.filterProxy;
      },
      set: function(val) {
        this.filterProxy = val;
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
    db: {
      get: function() {
        return this.dbProxy == null ? this.defaultDb : this.dbProxy;
      },
      set: function(val) {
        this.dbProxy = val;
      },
    },
    matrix: {
      get: function() {
        return this.matrixProxy == null ? this.defaultMatrix : this.matrixProxy;
      },
      set: function(val) {
        this.matrixProxy = val;
      },
    },
    wordSize: {
      get: function() {
        return this.wordSizeProxy == null ? this.defaultWordSize : this.wordSizeProxy;
      },
      set: function(val) {
        this.wordSizeProxy = val;
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
    disableMatrix() {
      return this.program == 'blastn' || this.program == 'tblastn' || this.program == 'tblastx';
    },
    form() {
      return {
        program: this.program,
        filter: this.filter,
        evalue: this.evalue,
        db: this.db,
        matrix: this.matrix,
        wordSize: this.wordSize,
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
        { text: 'blastp (protein vs protein)', value: 'blastp' },
        { text: 'blastx (translated nucleotide vs protein)', value: 'blastx' },
        {
          text: 'tblastn (protein vs translated nucleotide)',
          value: 'tblastn',
        },
        {
          text: 'tblastx (translated nucleotide vs translated nucleotide) ',
          value: 'tblastx',
        },
      ];

      programs.forEach(p => {
        let disabled = false;
        switch (this.dbType) {
          case 'protein':
            disabled = p.value == 'blastn' || p.value == 'tblastn' || p.value == 'tblastx';
            break;

          case 'CDS':
            disabled = p.value == 'blastp' || p.value == 'blastx';
            break;

          case 'genomic':
            disabled = p.value == 'blastp' || p.value == 'blastx';
            break;

          case 'transcriptome':
            disabled = p.value == 'blastp' || p.value == 'blastx';
            break;
          default:
            disabled = false;
            break;
        }
        p.disabled = disabled;
      });

      return programs;
    },
    /**
     * Set dbTypes for select
     */
    dbTypes() {
      let dbTypes = [
        { text: 'CDS', value: 'CDS' },
        { text: 'genomic', value: 'genomic' },
        { text: 'protein', value: 'protein', disabled: true },
      ];

      dbTypes.forEach(type => {
        let disabled = false;
        switch (this.dbType) {
          case 'protein':
            disabled = type.value == 'CDS' || type.value == 'genomic';
            break;

          case 'CDS':
            disabled = type.value == 'protein' || type.value == 'genomic';
            break;

          case 'genomic':
            disabled = type.value == 'CDS' || type.value == 'protein';
            break;

          case 'transcriptome':
            disabled = type.value == 'protein';
            break;
          default:
            disabled = false;
            break;
        }
        type.disabled = disabled;
      });
      return dbTypes;
    },
  },
  watch: {
    defaultProgram() {
      this.programProxy = null;
    },
    defaultFilter() {
      this.filterProxy = null;
    },
    defaultEvalue() {
      this.evalueProxy = null;
    },
    defaultDb() {
      this.dbProxy = null;
    },
    defaultMatrix() {
      this.matrixProxy = null;
    },
    defaultWordSize() {
      this.wordSizeProxy = null;
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
      this.filter = this.defaultFilter;
      this.evalue = this.defaultEvalue;
      this.db = this.defaultDb;
      this.matrix = this.defaultMatrix;
      this.wordSize = this.defaultWordSize;
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
    emitChangeDbType: function(dbType) {
      this.$emit('changedbtypeinput', dbType);
    },
  },
};
</script>
<style scoped>
#blast-form {
  margin: 10px;
}
</style>
