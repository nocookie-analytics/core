<template>
  <v-col v-if="hasData">
    <span v-if="blockType == DeclarativeBlockType.AggregateStat">
      <v-card-title>
        <slot name="blockTitle"></slot>
      </v-card-title>
      <v-card class="pa-2" outlined tile>
        <Tabular :data="blockData">
          <template v-slot:itemName="{ item }">
            <slot name="itemName" v-bind:item="item" />
          </template>
        </Tabular>
      </v-card>
    </span>

    <span v-if="blockType == DeclarativeBlockType.ArrayPageViewsPerDayStat">
      <LineChart :blockData="blockData" :styles="styles" />
    </span>
  </v-col>
</template>

<script lang="ts">
import {
  AggregateStat,
  AvgMetricPerDayStat,
  PageViewsPerDayStat,
  PageViewStat,
} from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { DeclarativeBlockType } from './interfaces';
import LineChart from './LineChart.vue';
import Tabular from './Tabular.vue';

@Component({ components: { LineChart, Tabular } })
export default class AnalyticsBlock extends Vue {
  DeclarativeBlockType = DeclarativeBlockType;
  // TODO: There's gotta be a better way to handle this, we don't need an explicit blockType when we already have blockData with a type
  @Prop() public blockData!:
    | Array<AggregateStat>
    | PageViewStat
    | Array<AvgMetricPerDayStat>
    | Array<PageViewsPerDayStat>;

  @Prop() public blockType!: DeclarativeBlockType;

  get hasData(): boolean {
    if (this.blockData && Array.isArray(this.blockData)) {
      return this.blockData.length !== 0;
    }
    return Boolean(this.blockData);
  }

  get styles(): Record<string, string> {
    return {
      height: '500px',
      position: 'relative',
    };
  }
}
</script>
