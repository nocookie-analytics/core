<template>
  <div>
    <v-container v-if="analyticsData">
      <v-row>
        <AnalyticsBlock
          :blockData="analyticsData.pageviews_per_day"
          :blockType="BlockType.ArrayPageViewsPerDayStat"
          :startDate="startDate"
          :endDate="endDate"
        />
      </v-row>
    </v-container>
    <v-container v-else> Loading, please wait </v-container>
  </div>
</template>

<script lang="ts">
import { AnalyticsData } from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';
import AnalyticsBlock, {
  BlockType,
} from '@/components/analytics/AnalyticsBlock.vue';
import { parseISO } from 'date-fns';

@Component({
  components: {
    AnalyticsBlock,
  },
})
export default class AnalyticsContainer extends Vue {
  BlockType = BlockType;
  @Prop() public analyticsData!: AnalyticsData;

  get startDate(): Date {
    return parseISO(this.analyticsData.start);
  }

  get endDate(): Date {
    return parseISO(this.analyticsData.end);
  }
}
</script>
