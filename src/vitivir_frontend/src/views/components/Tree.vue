<template>
  <div id="symdb-tree">
    <b-row align-h="center">
      <b-col md="6" sm="12">
        <ListsSelect ref="publicSetSelect" @change="selectSet"></ListsSelect>
      </b-col>
      <b-col md="6" sm="12">
        <ListsSelect ref="userSetSelect" :public="false" @change="selectSet"></ListsSelect>
      </b-col>
    </b-row>
    <b-row>
      <b-col md="6" sm="12">
        <TypeSelect @change="filterByDataType"></TypeSelect>
      </b-col>

      <b-col md="6" sm="12">
        <label for="inputSpecies">Filter by name</label>
        <b-form-input
          id="inputSpecies"
          v-model="specieQuery"
          width="100"
          multiple
          allow-batch
          size="sm"
          class="mt-1"
          @input="filterTreeByText"
        ></b-form-input>
      </b-col>
    </b-row>
    <p v-if="isAdmin" class="tinytext">Right-click on a node to display its content</p>
    <a @click="closeAll"><CloseCircleIcon title="close all" @click="closeAll"></CloseCircleIcon></a>
    &nbsp;
    <a @click="openAll"> <GraphOutlineIcon title="open all"></GraphOutlineIcon></a>
    &nbsp;
    <a @click="deselectAll"
      ><CheckboxMultipleBlankOutlineIcon title="deselect all"></CheckboxMultipleBlankOutlineIcon
    ></a>
    <v-jstree
      ref="tree"
      :data="data"
      :show-checkbox="showCheckbox"
      :multiple="multiple"
      :allow-batch="allowBatch"
      :item-events="finalItemEvents"
    ></v-jstree>
    <b-modal id="modalChart" ref="modalChart" title="Categories" ok-only hide-header-close>
      <GChart id="chart" type="PieChart" :data="chartData" :options="chartOptions" />
      <GChart id="chart2" type="PieChart" :data="chartData2" :options="chartOptions2" />
    </b-modal>

    <b-alert
      dismissible
      :show="dismissCountDown"
      :variant="variant"
      @dismissed="dismissCountDown = 0"
      @dismiss-count-down="countDownChanged"
      >{{ messageAlert }}</b-alert
    >
  </div>
</template>

<script>
import ListsSelect from '@/views/components/lists/ListsSelect.vue';
import TypeSelect from '@/views/components/TypeSelect.vue';

import CheckboxMultipleBlankOutlineIcon from 'vue-material-design-icons/CheckboxMultipleBlankOutline.vue';
import CloseCircleIcon from 'vue-material-design-icons/CloseCircle.vue';
import GraphOutlineIcon from 'vue-material-design-icons/GraphOutline.vue';

import Vue from 'vue';

import { GChart } from 'vue-google-charts';
import { mapGetters } from 'vuex';

export default {
  name: 'Tree',

  components: {
    GChart,
    ListsSelect,
    TypeSelect,
    CheckboxMultipleBlankOutlineIcon,
    CloseCircleIcon,
    GraphOutlineIcon,
  },
  props: {
    data: {
      type: Array,
      default: function() {
        return [];
      },
    },
    showCheckbox: Boolean,
    itemEvents: {
      type: Object,
      default: function() {
        return {};
      },
    },
    multiple: Boolean,
    allowBatch: Boolean,
  },
  data() {
    return {
      specieQuery: '',
      status: 'success',
      dismissSecs: 3,
      dismissCountDown: 0,
      messageAlert: '',
      variant: 'success',
      cleanSelected: 'false',
      chartData: null,
      chartData2: null,
      chartOptions: {
        title: 'Categories',
        subtitle: 'Number of organisms by category for this node',
        width: 450,
        pieSliceText: 'value',
      },
      chartOptions2: {
        title: 'Categories',
        subtitle: 'Number of organisms by category for this node',
        width: 450,
        pieSliceText: 'value',
      },
    };
  },
  computed: {
    ...mapGetters(['isAdmin']),
    finalItemEvents() {
      var itemEvents = this.itemEvents;

      // LC 27/09/2019
      // Desactivation en attendant les vraies categories
      var component = this;
      if (typeof itemEvents.contextmenu !== undefined) {
        itemEvents.contextmenu = (node, x, e) => {
          e.preventDefault();
          component.loadStats(node);
        };
      }

      return itemEvents;
    },
  },
  methods: {
    countDownChanged(dismissCountDown) {
      this.dismissCountDown = dismissCountDown;
    },
    showAlert() {
      this.dismissCountDown = this.dismissSecs;
    },
    /**
     * Get all leaves of a node
     */
    getLeaves(root) {
      let a_leaves = [];
      function recursive(node) {
        if (node.$children && node.$children.length > 0) {
          for (let childNode of node.$children) {
            recursive(childNode);
          }
        } else {
          a_leaves.push(node);
        }
      }
      recursive(root);
      return a_leaves;
    },
    openOrCloseAll(bool) {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });
      function recursive(node) {
        if (node.$children && node.$children.length > 0) {
          for (let childNode of node.$children) {
            recursive(childNode);
          }
        }

        if (node.model !== undefined) {
          node.model.opened = bool;
        }
      }
      recursive(this.$refs.tree);
      this.$refs.tree.opened = bool;
      loader.hide();
    },
    openAll() {
      this.openOrCloseAll(true);
    },
    closeAll() {
      this.openOrCloseAll(false);
    },
    deselectAll() {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });

      this.setSelected([]);
      this.filterTreeBySelected();
      loader.hide();
    },
    getSelected() {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });
      let a_selected = [];

      function recursive(node, a_selected) {
        let selected = false;

        if (node.model !== undefined) {
          selected = node.model.selected;
        }

        if (node.$children && node.$children.length > 0) {
          for (let childNode of node.$children) {
            a_selected = recursive(childNode, a_selected);
          }
        } else {
          if (selected) {
            a_selected.push({ id: node.model.id, text: node.model.text });
          }
        }

        return a_selected;
      }
      a_selected = recursive(this.$refs.tree, a_selected);

      loader.hide();
      return a_selected;
    },
    /**
     * Select nodes from an array of ids
     * returns the  number of nodes selected
     */
    setSelected(a_ids) {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });

      let n = 0;

      function recursive(node, a_ids, parentSelected) {
        if (node.model !== undefined) {
          if (
            (a_ids.includes(node.model.id) || parentSelected) &&
            (!('disabled' in node.model) || !node.model.disabled)
          ) {
            node.model.selected = true;
            node.model.opened = true;
            n++;
          } else {
            node.model.selected = false;
            node.model.opened = false;
          }

          if (
            a_ids.includes(node.model.id) &&
            (!('disabled' in node.model) || !node.model.disabled)
          ) {
            parentSelected = true;
          }
        }

        if (node.$children && node.$children.length > 0) {
          for (let childNode of node.$children) {
            recursive(childNode, a_ids, parentSelected);
          }
        }
      }

      try {
        recursive(this.$refs.tree, a_ids, false);
      } catch (error) {
        loader.hide();
        this.variant = 'danger';
        this.messageAlert = 'Problem when selecting genomes';
        this.showAlert();
      }

      this.$refs.tree.opened = true;
      loader.hide();
      return n;
    },
    /**
     * Filter Tree by text input
     */
    filterTreeByText() {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });
      function recursive(node, patt, text) {
        let flag = false;

        if (node.$children && node.$children.length > 0) {
          for (let childNode of node.$children) {
            let flag_child = recursive(childNode, patt, text);
            if (flag_child === true) {
              flag = true;
            }
          }
        }

        if (text === '') {
          flag = false;
        } else {
          if (flag === false) {
            if (text !== '' && node.model !== undefined) {
              const str = node.model.text;

              if (patt.test(str)) {
                flag = true;
              }
            } else {
              flag = false;
            }
          }
        }
        if (node.model !== undefined) {
          node.model.opened = flag;
        } else {
          node.opened = flag;
        }
        if (flag) {
          node.$el.querySelector('.tree-anchor').style.color = '#8b0000';
          node.$el.querySelector('.tree-anchor').style['font-style'] = 'italic';
        } else {
          node.$el.querySelector('.tree-anchor').style.color = '#000';
          node.$el.querySelector('.tree-anchor').style['font-style'] = 'normal';
        }
        return flag;
      }

      var text = this.specieQuery;
      const patt = new RegExp(text, 'i');

      recursive(this.$refs.tree, patt, text);

      loader.hide();
    },
    /**
     * Filter Tree by text input
     */
    filterTreeBySelected() {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });
      function recursive(node) {
        let flag = false;

        if (node.$children && node.$children.length > 0) {
          for (let childNode of node.$children) {
            let flag_child = recursive(childNode);
            if (flag_child === true) {
              flag = true;
            }
          }
        }

        if (node.model !== undefined) {
          flag = !flag ? node.model.selected : flag;
          node.model.opened = flag;
        } else {
          node.opened = flag;
        }

        return flag;
      }

      recursive(this.$refs.tree);

      loader.hide();
    },
    /**
     * Filter tree by dataType
     */
    filterByDataType(typedb) {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });

      if (typedb == null || typedb == 0) {
        this.makeAvailableNodes(null);
        loader.hide();
      } else {
        Vue.http.post('api/getNodeIdsByDataType', { typedb: typedb }).then(
          resp => {
            loader.hide();
            const data = resp.body;
            if (data != null && data.success == true && typeof data.ids !== 'undefined') {
              let a_ids = data.ids.map(d => {
                return d.parent_id;
              });

              this.makeAvailableNodes(a_ids);
            } else {
              this.messageAlert =
                data != null && typeof data.message !== 'undefined'
                  ? data.message
                  : 'Server problem when loading set';

              this.variant = 'danger';
              this.messageAlert = 'Server problem when loading set';
              this.showAlert();
            }
          },
          error => {
            loader.hide();
            this.variant = 'danger';
            this.messageAlert = 'Server problem when loading set (' + error.statusText + ')';
            this.showAlert();
          }
        );
      }
      this.$emit('changedbtype', typedb != 0 && typedb != null ? typedb : '');
    },

    /**
     *
     */
    makeAvailableNodes: function(a_ids) {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });

      function recursive(node, a_ids) {
        if (node.$children && node.$children.length > 0) {
          for (let childNode of node.$children) {
            recursive(childNode, a_ids);
          }
        } else {
          if (node.model !== undefined) {
            if (a_ids == null || a_ids.includes(node.model.id)) {
              node.model.disabled = false;
            } else {
              node.model.selected = false;
              node.model.disabled = true;
            }
          }
        }
      }

      try {
        recursive(this.$refs.tree, a_ids);
      } catch (error) {
        loader.hide();
        this.variant = 'danger';
        this.messageAlert = 'Problem when selecting genomes';
        this.showAlert();
      }

      this.$refs.tree.opened = true;
      loader.hide();
    },

    /**
     * Get the changes from the set comboboxes
     */
    selectSet: function(idSet, publicMode) {
      let loader = this.$loading.show({
        // Optional parameters
        container: null,
        canCancel: false,
        loader: 'dots',
      });

      let elt = publicMode ? this.$refs.userSetSelect : this.$refs.publicSetSelect;

      elt.selectedSet = null;

      if (idSet == null || idSet == 0) {
        this.setSelected([]);
        this.filterTreeBySelected();
        loader.hide();
        this.variant = 'success';
        this.messageAlert = 'All the nodes are deselected';
        this.showAlert();
      } else {
        Vue.http.post('api/getSetContent', { idSet: idSet, public: publicMode }).then(
          resp => {
            const data = resp.body;
            if (data != null && data.success == true && typeof data.ids !== 'undefined') {
              let nSelected = this.setSelected(data.ids);
              this.filterTreeBySelected();
              this.variant = 'success';
              this.messageAlert = nSelected + ' nodes selected';
              this.showAlert();
              loader.hide();
            } else {
              loader.hide();
              this.variant = 'danger';
              this.messageAlert = 'Server problem when loading set';
              this.showAlert();
            }
          },
          error => {
            loader.hide();
            this.variant = 'danger';
            this.messageAlert = 'Server problem when loading set (' + error.statusText + ')';
            this.showAlert();
          }
        );
      }
    },
    loadStats: function(node) {
      let a_leaveIds = this.getLeaves(node).map(l => {
        return l.model.id;
      });

      this.chartData = null;
      this.chartData2 = null;

      Vue.http.post('api/getSupCategories', { ids: a_leaveIds }).then(
        resp => {
          if (resp.body.success === false) {
            this.messageAlert = resp.body.message;
            this.variant = 'danger';
            this.showAlert();
          } else {
            // if (resp.body.cats.length > 0) {
            this.$set(
              this.chartOptions,
              'title',
              'Generic categories, total :' + a_leaveIds.length
            );

            this.chartData = [['cat', 'nb']];

            let a_cats = resp.body.cats;

            a_cats.sort((a, b) => {
              return b[1] - a[1];
            });

            a_cats.forEach(c => {
              this.chartData.push(c);
            });
          }
        },
        () => {
          this.messageAlert = 'Server error';
          this.variant = 'danger';
          this.chartData = Object.assign({}, this.chartData, {});
          this.showAlert();
        }
      );

      Vue.http.post('api/getSubCategories', { ids: a_leaveIds }).then(
        resp => {
          if (resp.body.success === false) {
            this.messageAlert = resp.body.message;
            this.variant = 'danger';
            this.showAlert();
          } else {
            // if (resp.body.cats.length > 0) {
            this.$set(this.chartOptions2, 'title', 'Symbiotic categories');

            this.chartData2 = [['cat', 'nb']];

            let a_cats = resp.body.cats;

            a_cats.sort((a, b) => {
              return b[1] - a[1];
            });

            a_cats.forEach(c => {
              this.chartData2.push(c);
            });
          }
        },
        () => {
          this.messageAlert = 'Server error';
          this.variant = 'danger';
          this.chartData = Object.assign({}, this.chartData, {});
          this.showAlert();
        }
      );
      this.$refs['modalChart'].show();
    },
  },
};
</script>
<style scoped>
#symdb-tree {
  margin: 10px;
  text-align: left;
}

input {
  width: 200px;
}

.tinytext {
  font-size: 12px;
  margin-bottom: 0px;
}
</style>

<style>
.tree-disabled span {
  text-decoration: line-through;
}
.tree-selected span {
  color: #8b0000;
  font-style: italic;
}

label {
  margin-bottom: 0px;
  font-size: 12px;
}
</style>
