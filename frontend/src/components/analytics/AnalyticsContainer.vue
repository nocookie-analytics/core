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
      <v-row>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.browser_families"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>Browser</template>
            <template v-slot:itemName="{ item }"
              ><v-icon>mdi-{{ item.value.toLowerCase() }}</v-icon>
              {{ item.value }}</template
            >
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.os_families"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>OS</template>
            <template v-slot:itemName="{ item }"
              ><v-icon>mdi-{{ item.value.toLowerCase() }}</v-icon>
              {{ item.value }}</template
            >
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.device_families"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>Device type</template>
            <template v-slot:itemName="{ item }"
              ><v-icon>mdi-{{ item.value.toLowerCase() }}</v-icon>
              {{ item.value }}</template
            >
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.referrer_names"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>Referrer name</template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.referrer_mediums"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>Referrer medium</template>
          </AnalyticsBlock>
        </v-col>
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
