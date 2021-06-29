<template>
  <v-container v-if="analyticsData" class="pa-0">
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
        :lg="block.cols * 2"
        :md="block.cols * 4"
        :sm="block.cols * 4"
        :xl="block.cols"
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
import { AnalyticsData } from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';
import AnalyticsBlock from '@/components/analytics/AnalyticsBlock.vue';
import { DeclarativeAnalyticsBlock } from './interfaces';

@Component({
  components: {
    AnalyticsBlock,
    LineChart,
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
        cols: 3,
      },
      {
        data: this.analyticsData.browser_families || [],
        title: 'Browser',
        urlParamName: 'browser',
        urlExclude: ['Unknown'],
        cols: 3,
      },
      {
        data: this.analyticsData.os_families || [],
        title: 'OS',
        urlParamName: 'os',
        urlExclude: ['Other'],
        cols: 3,
      },
      {
        data: this.analyticsData.device_families || [],
        title: 'Device',
        urlParamName: 'device',
        urlExclude: ['Other', 'Unknown'],
        cols: 3,
      },
      {
        data: this.analyticsData.referrer_names || [],
        title: 'Referrer',
        urlParamName: 'referrerName',
        urlExclude: [],
        cols: 3,
      },
      {
        data: this.analyticsData.countries || [],
        title: 'Country',
        urlParamName: 'country',
        urlExclude: ['Unknown'],
        cols: 4,
      },
      {
        data: this.analyticsData.utm_terms || [],
        title: 'UTM Term',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_sources || [],
        title: 'UTM Source',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_mediums || [],
        title: 'UTM Medium',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_contents || [],
        title: 'UTM Content',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_campaigns || [],
        title: 'UTM Campaign',
        cols: 2,
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
