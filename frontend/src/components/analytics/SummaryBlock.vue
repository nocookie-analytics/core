<template>
  <v-container fluid v-if="summaryData">
    <v-row justify="start">
      <v-col
        v-for="block in summaryBlocks"
        :key="block.title"
        cols="6"
        lg="3"
        xl="2"
        sm="6"
      >
        <v-card outlined min-width="200" max-width="200" width="200">
          <v-card-title>{{ block.title }}</v-card-title>
          <v-card-text>
            <v-icon>{{ block.icon }}</v-icon>
            {{ block.value }}
            <span
              v-if="block.change"
              :class="block.change > 0 ? 'light-green--text' : 'red--text'"
            >
              <v-icon v-if="block.change < 0">{{
                icons.mdiTrendingDown
              }}</v-icon>
              <v-icon v-if="block.change == 0">{{
                icons.mdiTrendingNeutral
              }}</v-icon>
              <v-icon v-if="block.change > 0">{{ icons.mdiTrendingUp }}</v-icon>
              {{ block.change }}%
            </span>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { SummaryStat } from '@/generated';
import {
  mdiAccountMultiple,
  mdiCropLandscape,
  mdiTrendingUp,
  mdiTrendingDown,
  mdiTrendingNeutral,
} from '@mdi/js';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class SummaryBlock extends Vue {
  @Prop() public summaryData!: SummaryStat;
  @Prop() public summaryDataPreviousInterval!: SummaryStat;

  percentagechange(newValue: number, oldValue: number): number | undefined {
    if (oldValue) {
      return Math.round((100 * (newValue - oldValue)) / oldValue);
    }
    return undefined;
  }

  get icons() {
    return {
      mdiTrendingUp,
      mdiTrendingDown,
      mdiTrendingNeutral,
    };
  }

  get summaryBlocks() {
    return [
      {
        title: 'Page views',
        value: this.summaryData.total_visits,
        change: this.percentagechange(
          this.summaryData.total_visits,
          this.summaryDataPreviousInterval.total_visits,
        ),
        icon: mdiCropLandscape,
      },
      {
        title: 'Unique visitors',
        value: this.summaryData.visitors,
        icon: mdiAccountMultiple,
        change: this.percentagechange(
          this.summaryData.visitors,
          this.summaryDataPreviousInterval.visitors,
        ),
      },
    ];
  }
}
</script>
