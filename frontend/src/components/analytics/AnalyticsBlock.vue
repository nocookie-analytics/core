<template>
  <v-col>
    <v-card
      class="pa-2"
      outlined
      tile
      v-if="blockType == BlockType.AggregateStat"
    >
      Aggregate Stat: Not implemented
    </v-card>
    <v-card
      class="pa-2"
      outlined
      tile
      v-if="blockType == BlockType.ArrayPageViewsPerDayStat"
    >
      <LineChart
        :blockData="blockData"
        :startDate="startDate"
        :endDate="endDate"
        :styles="styles"
      />
    </v-card>
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
import LineChart from './LineChart.vue';

export enum BlockType {
  AggregateStat,
  ArrayAvgMetricPerDayStat,
  PageViewStat,
  ArrayPageViewsPerDayStat,
}

@Component({ components: { LineChart } })
export default class AnalyticsBlock extends Vue {
  BlockType = BlockType;
  // TODO: There's gotta be a better way to handle this, we don't need an explicit blockType when we already have blockData with a type
  @Prop() public blockData!:
    | AggregateStat
    | PageViewStat
    | Array<AvgMetricPerDayStat>
    | Array<PageViewsPerDayStat>;

  @Prop() public blockType!: BlockType;

  @Prop() public startDate!: Date;
  @Prop() public endDate!: Date;

  get styles(): Record<string, string> {
    return {
      height: '500px',
      position: 'relative',
    };
  }
}
</script>
