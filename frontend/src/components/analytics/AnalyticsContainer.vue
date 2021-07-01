<template>
  <v-container v-if="analyticsData" class="pa-0">
    <v-row no-gutters>
      <v-col>
        <SummaryBlock :summaryData="analyticsData.summary" />
      </v-col>
    </v-row>
    <v-row no-gutters>
      <v-col>
        <LineChart
          :blockData="analyticsData.pageviews_per_day"
          :styles="styles"
        />
      </v-col>
    </v-row>
    <v-row dense no-gutters>
      <v-col
        v-for="block in blocks"
        :key="block.title"
        :lg="6"
        :md="6"
        :sm="6"
        :xl="3"
        cols="12"
      >
        <AnalyticsBlock :block="block" />
      </v-col>
    </v-row>
  </v-container>
  <v-container v-else> Loading, please wait </v-container>
</template>

<script lang="ts">
import LineChart from './LineChart.vue';
import SummaryBlock from './SummaryBlock.vue';
import { AnalyticsData } from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';
import AnalyticsBlock from '@/components/analytics/AnalyticsBlock.vue';
import { DeclarativeAnalyticsBlock } from './interfaces';

@Component({
  components: {
    AnalyticsBlock,
    LineChart,
    SummaryBlock,
  },
})
export default class AnalyticsContainer extends Vue {
  @Prop() public analyticsData!: AnalyticsData;

  get blocks(): Array<DeclarativeAnalyticsBlock> {
    const blocks = [
      {
        data: this.analyticsData.pages || [],
        title: 'Page',
        urlParamName: 'page',
        urlExclude: [],
      },
      {
        data: this.analyticsData.browser_families || [],
        title: 'Browser',
        urlParamName: 'browser',
        urlExclude: ['Unknown'],
      },
      {
        data: this.analyticsData.os_families || [],
        title: 'OS',
        urlParamName: 'os',
        urlExclude: ['Other'],
      },
      {
        data: this.analyticsData.device_families || [],
        title: 'Device',
        urlParamName: 'device',
        urlExclude: ['Other', 'Unknown'],
      },
      {
        data: this.analyticsData.referrer_names || [],
        title: 'Referrer',
        urlParamName: 'referrerName',
        urlExclude: [],
      },
      {
        data: this.analyticsData.countries || [],
        title: 'Country',
        urlParamName: 'country',
        urlExclude: ['Unknown'],
      },
      {
        data: this.analyticsData.utm_terms || [],
        title: 'UTM Term',
      },
      {
        data: this.analyticsData.utm_sources || [],
        title: 'UTM Source',
      },
      {
        data: this.analyticsData.utm_mediums || [],
        title: 'UTM Medium',
      },
      {
        data: this.analyticsData.utm_contents || [],
        title: 'UTM Content',
      },
      {
        data: this.analyticsData.utm_campaigns || [],
        title: 'UTM Campaign',
      },
    ];
    return blocks.filter((block) => block.data.length > 0);
  }
  get styles(): Record<string, string> {
    return {
      height: '500px',
      position: 'relative',
    };
  }
}
</script>
