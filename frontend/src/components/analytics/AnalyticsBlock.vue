<template>
  <v-col v-if="hasData">
    <v-card-title>
      <AnalyticsBlockTitle
        :block="block"
        :currentPage="currentPage"
        :totalPages="totalPages"
        v-on:next-page="currentPage += 1"
        v-on:prev-page="currentPage -= 1"
      />
    </v-card-title>
    <v-card class="pa-2" outlined tile>
      <Tabular :data="currentPageItems">
        <template v-slot:itemName="{ item }">
          <AnalyticsSingleValue :block="block" :item="item" />
        </template>
      </Tabular>
    </v-card>
  </v-col>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { DeclarativeAnalyticsBlock } from './interfaces';
import Tabular from './Tabular.vue';
import AnalyticsSingleValue from './AnalyticsSingleValue.vue';
import AnalyticsBlockTitle from './AnalyticsBlockTitle.vue';

@Component({
  components: { Tabular, AnalyticsSingleValue, AnalyticsBlockTitle },
})
export default class AnalyticsBlock extends Vue {
  @Prop() public block!: DeclarativeAnalyticsBlock;

  currentPage = 0;

  itemsPerPage = 10;

  private get totalPages() {
    return Math.ceil(this.block.data.length / this.itemsPerPage);
  }

  private get currentPageStart() {
    return this.currentPage * this.itemsPerPage;
  }

  private get nextPageStart() {
    return (this.currentPage + 1) * this.itemsPerPage;
  }

  get currentPageItems() {
    return this.block.data.slice(this.currentPageStart, this.nextPageStart);
  }

  get hasData(): boolean {
    if (this.block && this.block.data && Array.isArray(this.block.data)) {
      return this.block.data.length !== 0;
    }
    return Boolean(this.block && this.block.data);
  }
}
</script>
