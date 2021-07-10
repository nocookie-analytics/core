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
        <v-card outlined min-width="165" max-width="165" width="165">
          <v-card-title>{{ block.title }}</v-card-title>
          <v-card-text>
            <v-icon :class="block.class">{{ block.icon }}</v-icon>
            {{ block.value }}
            <span
              v-if="block.change"
              :class="
                block.changeSign * block.change > 0
                  ? 'green--text text--darken-2'
                  : 'red--text'
              "
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
import { ISummaryBlock } from '@/interfaces';
import { SummaryStat } from '@/generated';
import {
  mdiAccountMultiple,
  mdiCropLandscape,
  mdiTrendingUp,
  mdiTrendingDown,
  mdiTrendingNeutral,
  mdiSubdirectoryArrowRight,
  mdiSawtoothWave,
} from '@mdi/js';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class SummaryBlock extends Vue {
  @Prop() public summaryData!: SummaryStat;
  @Prop() public summaryDataPreviousInterval!: SummaryStat;
  @Prop() public liveVisitorCount!: number;

  percentagechange(newValue: number, oldValue?: number): number | undefined {
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

  get summaryBlocks(): Array<ISummaryBlock> {
    const blocks = [
      {
        title: 'Page views',
        value: this.summaryData.total_visits.toString(),
        change: this.percentagechange(
          this.summaryData.total_visits,
          this.summaryDataPreviousInterval.total_visits,
        ),
        changeSign: 1,
        class: '',
        icon: mdiCropLandscape,
      },
      {
        title: 'Visitors',
        value: this.summaryData.visitors.toString(),
        class: '',
        icon: mdiAccountMultiple,
        changeSign: 1,
        change: this.percentagechange(
          this.summaryData.visitors,
          this.summaryDataPreviousInterval.visitors,
        ),
      },
    ];
    if (this.summaryData.bounce_rate) {
      blocks.push({
        title: 'Bounced',
        value: `${this.summaryData.bounce_rate}%`,
        icon: mdiSubdirectoryArrowRight,
        class: 'rotate-45',
        changeSign: -1,
        change: this.percentagechange(
          this.summaryData.bounce_rate,
          this.summaryDataPreviousInterval.bounce_rate,
        ),
      });
    }
    blocks.push({
      // TODO: This should update automatically
      title: 'Live visitors',
      value: `${this.liveVisitorCount}`,
      icon: mdiSawtoothWave,
      changeSign: 1,
      change: undefined,
      class: 'blink',
    });
    return blocks;
  }
}
</script>

<style scoped>
.rotate-45 {
  transform: rotate(-45deg);
}
.blink {
  animation: blinker 5s linear infinite;
}

@keyframes blinker {
  50% {
    opacity: 0;
  }
}
</style>
