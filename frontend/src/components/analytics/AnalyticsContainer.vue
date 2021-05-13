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
            :blockData="analyticsData.pages"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>
              Page
              <v-icon
                v-if="page"
                v-on:click.stop="updateFilter('page')"
              >
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:itemName="{ item }"><a v-on:click.stop="updateFilter('page', item.value)">{{
                item.value
              }}</a></template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.browser_families"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>Browser
              <v-icon
                v-if="browser"
                v-on:click.stop="updateFilter('browser')"
              >
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:itemName="{ item }">
              <a
                v-on:click.stop="updateFilter('browser', item.value)"
                v-if="item.value !== 'Unknown'"
              >
                <Icon :value="item.value" />
                {{ item.value }}
              </a></template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.os_families"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>
              <v-icon
                v-if="os"
                v-on:click.stop="updateFilter('os')"
              >
                mdi-delete
              </v-icon>
              OS
            </template>
            <template v-slot:itemName="{ item }">
              <a
                v-on:click.stop="updateFilter('os', item.value)"
                v-if="item.value !== 'Unknown'"
              >
                <Icon :value="item.value" />
                {{ item.value }}
              </a>
            </template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.device_families"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>
              <v-icon
                v-if="device"
                v-on:click.stop="updateFilter('device')"
              >
                Device type
              </v-icon>
            </template>
            <template v-slot:itemName="{ item }">
              <a
                v-on:click.stop="updateFilter('device', item.value)"
                v-if="item.value !== 'Unknown'"
              >
                <Icon :value="item.value" />
                {{ item.value }}
              </a>
            </template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.referrer_names"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>
              <v-icon
                v-if="referrerName"
                v-on:click.stop="updateFilter('referrerName')"
              >
                Referrer name
              </v-icon>
            </template>
            <template v-slot:itemName="{ item }">
              <a
                v-on:click.stop="updateFilter('referrerName', item.value)"
                v-if="item.value !== 'Unknown'"
              >
                <Icon :value="item.value" />
                {{ item.value }}
              </a>
            </template>
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
        <v-col cols="4">
          <AnalyticsBlock
            :blockData="analyticsData.countries"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>
              Country
              <v-icon
                v-if="country"
                v-on:click.stop="updateFilter('country')"
              >
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:itemName="{ item }">
              <a
                v-on:click.stop="updateFilter('country', item.value)"
                v-if="item.value !== 'Unknown'"
              >
                <country-flag
                  :country="item.value.toLowerCase()"
                  rounded
                  size="normal"
                />
                {{ countryCodeToCountryName(item.value) }}
              </a>
            </template>
          </AnalyticsBlock>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="2">
          <AnalyticsBlock
            :blockData="analyticsData.utm_terms"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>UTM Term</template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="2">
          <AnalyticsBlock
            :blockData="analyticsData.utm_sources"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>UTM Source</template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="2">
          <AnalyticsBlock
            :blockData="analyticsData.utm_mediums"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>UTM Medium</template>
          </AnalyticsBlock>
        </v-col>
        <v-col cols="2">
          <AnalyticsBlock
            :blockData="analyticsData.utm_contents"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>UTM Content</template>
          </AnalyticsBlock>
        </v-col>
      </v-row>
      <v-col cols="2">
        <AnalyticsBlock
          :blockData="analyticsData.utm_campaigns"
          :blockType="BlockType.AggregateStat"
          :startDate="startDate"
          :endDate="endDate"
        >
          <template v-slot:blockTitle>UTM Campaign</template>
        </AnalyticsBlock>
      </v-col>
    </v-container>
    <v-container v-else> Loading, please wait </v-container>
  </div>
</template>

<script lang="ts">
import { AggregateStat, AnalyticsData } from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';
import AnalyticsBlock, {
  BlockType,
} from '@/components/analytics/AnalyticsBlock.vue';
import Icon from '@/components/analytics/Icon.vue';
import { parseISO } from 'date-fns';
import countryCodes from '@/components/data/countryCodes';
import CountryFlag from 'vue-country-flag';
import { dispatchUpdateAnalyticsFilter } from '@/store/analytics/actions';
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

  updateFilter(key: string, value: string | undefined = undefined): void {
    this.$router.replace({ query: { ...this.$route.query, [key]: value } });
    dispatchUpdateAnalyticsFilter(this.$store, { key, value });
  }

  countryCodeToCountryName(countryCode: string): string {
    return countryCodes[countryCode] || countryCode;
  }
}
</script>
