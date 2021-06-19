<template>
  <v-container v-if="analyticsData" fluid class="pa-0">
    <v-row no-gutters>
      <AnalyticsBlock
        :blockData="analyticsData.pageviews_per_day"
        :blockType="DeclarativeBlockType.ArrayPageViewsPerDayStat"
      />
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
        <AnalyticsBlock :blockData="block.data" :blockType="block.type">
          <template v-slot:blockTitle>
            <AnalyticsBlockTitle :block="block" />
          </template>
          <template v-slot:itemName="{ item }">
            <AnalyticsSingleValue :block="block" :item="item" />
          </template>
        </AnalyticsBlock>
      </v-col>
    </v-row>
  </v-container>
  <v-container v-else> Loading, please wait </v-container>
</template>

<script lang="ts">
import { AggregateStat, AnalyticsData } from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';
import AnalyticsBlock from '@/components/analytics/AnalyticsBlock.vue';
import AnalyticsSingleValue from './AnalyticsSingleValue.vue';
import AnalyticsBlockTitle from './AnalyticsBlockTitle.vue';
import { parseISO } from 'date-fns';
import {
  readBrowser,
  readCountry,
  readDevice,
  readOs,
  readPage,
  readReferrerName,
} from '@/store/analytics/getters';
import { DeclarativeBlockType, DeclarativeAnalyticsBlock } from './interfaces';

@Component({
  components: {
    AnalyticsBlock,
    AnalyticsBlockTitle,
    AnalyticsSingleValue,
  },
})
export default class AnalyticsContainer extends Vue {
  DeclarativeBlockType = DeclarativeBlockType;
  @Prop() public analyticsData!: AnalyticsData;

  get startDate(): Date {
    return parseISO(this.analyticsData.start);
  }

  get endDate(): Date {
    return parseISO(this.analyticsData.end);
  }

  get page(): string | undefined {
    return readPage(this.$store);
  }

  get country(): string | undefined {
    return readCountry(this.$store);
  }

  get browser(): string | undefined {
    return readBrowser(this.$store);
  }

  get os(): string | undefined {
    return readOs(this.$store);
  }

  get device(): string | undefined {
    return readDevice(this.$store);
  }

  get referrerName(): string | undefined {
    return readReferrerName(this.$store);
  }

  get blocks(): Array<DeclarativeAnalyticsBlock> {
    const blocks = [
      {
        data: this.analyticsData.pages || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'Page',
        urlParamName: 'page',
        urlExclude: [],
        cols: 3,
      },
      {
        data: this.analyticsData.browser_families || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'Browser',
        urlParamName: 'browser',
        urlExclude: ['Unknown'],
        cols: 3,
      },
      {
        data: this.analyticsData.os_families || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'OS',
        urlParamName: 'os',
        urlExclude: ['Other'],
        cols: 3,
      },
      {
        data: this.analyticsData.device_families || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'Device',
        urlParamName: 'device',
        urlExclude: ['Other', 'Unknown'],
        cols: 3,
      },
      {
        data: this.analyticsData.referrer_names || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'Referrer',
        urlParamName: 'referrerName',
        urlExclude: [],
        cols: 3,
      },
      {
        data: this.analyticsData.countries || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'Country',
        urlParamName: 'country',
        urlExclude: ['Unknown'],
        cols: 4,
      },
      {
        data: this.analyticsData.utm_terms || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'UTM Term',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_sources || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'UTM Source',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_mediums || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'UTM Medium',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_contents || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'UTM Content',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_campaigns || [],
        type: DeclarativeBlockType.AggregateStat,
        title: 'UTM Campaign',
        cols: 2,
      },
    ];
    return blocks.filter((block) => block.data.length > 0);
  }

  itemUrl(block: DeclarativeAnalyticsBlock, item): string {
    if (
      block.urlParamName &&
      block.data &&
      block.data.length > 1 &&
      block.urlExclude &&
      !block.urlExclude.includes(item.value)
    ) {
      return 'hello';
    }
    return 'hello';
  }

  filterURL(key: string, value: string | undefined = undefined) {
    return {
      ...this.$route.query,
      [key]: value,
    };
  }
}
</script>
