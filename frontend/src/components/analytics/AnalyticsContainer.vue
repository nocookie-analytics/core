<template>
  <div>
    <v-container v-if="analyticsData">
      <v-row dense>
        <AnalyticsBlock
          :blockData="analyticsData.pageviews_per_day"
          :blockType="BlockType.ArrayPageViewsPerDayStat"
        />
      </v-row>
      <v-row>
        <v-col v-for="block in blocks" :key="block.title">
          <AnalyticsBlock :blockData="block.data" :blockType="block.type">
            <template v-slot:blockTitle>
              {{ block.title }}
              <router-link
                :to="{ query: filterURL(block.urlParamName) }"
                v-if="block.urlParamName && isFilterActive(block.urlParamName)"
              >
                <v-icon> {{ $vuetify.icons.values.delete }} </v-icon>
              </router-link>
            </template>
            <template v-slot:itemName="{ item }">
              <Icon
                :value="item.value"
                v-if="block.urlParamName !== 'country'"
              />&nbsp;
              <router-link
                v-if="
                  block.urlParamName &&
                  block.data &&
                  block.data.length > 1 &&
                  block.urlExclude &&
                  !block.urlExclude.includes(item.value)
                "
                :to="{ query: filterURL(block.urlParamName, item.value) }"
              >
                <span v-if="block.urlParamName === 'country'">
                  <country-flag
                    :country="item.value.toLowerCase()"
                    rounded
                    size="normal"
                  />{{ countryCodeToCountryName(item.value) }}
                </span>
                <span v-else>
                  {{ item.value }}
                </span>
              </router-link>
              <span v-else>
                <span v-if="block.urlParamName === 'country'">
                  <country-flag
                    :country="item.value.toLowerCase()"
                    rounded
                    size="normal"
                  />{{ countryCodeToCountryName(item.value) }}
                </span>
                <span v-else>
                  {{ item.value }}
                </span>
              </span>
            </template>
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
import Icon from '@/components/analytics/Icon.vue';
import { parseISO } from 'date-fns';
import countryCodes from '@/components/data/countryCodes';
import CountryFlag from 'vue-country-flag';
import {
  readBrowser,
  readCountry,
  readDevice,
  readOs,
  readPage,
  readReferrerName,
} from '@/store/analytics/getters';

@Component({
  components: {
    AnalyticsBlock,
    CountryFlag,
    Icon,
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

  get blocks() {
    const blocks = [
      {
        data: this.analyticsData.pages,
        type: BlockType.AggregateStat,
        title: 'Page',
        urlParamName: 'page',
        urlExclude: [],
        cols: 3,
      },
      {
        data: this.analyticsData.browser_families,
        type: BlockType.AggregateStat,
        title: 'Browser',
        urlParamName: 'browser',
        urlExclude: [],
        cols: 3,
      },
      {
        data: this.analyticsData.os_families,
        type: BlockType.AggregateStat,
        title: 'OS',
        urlParamName: 'os',
        urlExclude: ['Other'],
        cols: 3,
      },
      {
        data: this.analyticsData.device_families,
        type: BlockType.AggregateStat,
        title: 'Device',
        urlParamName: 'device',
        urlExclude: ['Other', 'Unknown'],
        cols: 3,
      },
      {
        data: this.analyticsData.referrer_names,
        type: BlockType.AggregateStat,
        title: 'Referrer name',
        urlParamName: 'referrerName',
        urlExclude: [],
        cols: 3,
      },
      {
        data: this.analyticsData.countries,
        type: BlockType.AggregateStat,
        title: 'Country',
        urlParamName: 'country',
        urlExclude: ['Unknown'],
        cols: 4,
      },
      {
        data: this.analyticsData.utm_terms,
        type: BlockType.AggregateStat,
        title: 'UTM Term',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_sources,
        type: BlockType.AggregateStat,
        title: 'UTM Source',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_mediums,
        type: BlockType.AggregateStat,
        title: 'UTM Medium',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_contents,
        type: BlockType.AggregateStat,
        title: 'UTM Content',
        cols: 2,
      },
      {
        data: this.analyticsData.utm_campaigns,
        type: BlockType.AggregateStat,
        title: 'UTM Campaign',
        cols: 2,
      },
    ];
    const hasData = (block) => {
      if (block.data && Array.isArray(block.data)) {
        return block.data.length !== 0;
      }
      return true;
    };
    return blocks.filter((block) => hasData(block));
  }

  isFilterActive(key: string): boolean {
    return Boolean(this.$route.query[key]);
  }

  filterURL(key: string, value: string | undefined = undefined) {
    return {
      ...this.$route.query,
      [key]: value,
    };
  }

  countryCodeToCountryName(countryCode: string): string {
    return countryCodes[countryCode] || countryCode;
  }
}
</script>
