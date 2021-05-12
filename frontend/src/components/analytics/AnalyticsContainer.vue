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
              <v-icon v-if="page" v-on:click.stop="filterPage(undefined)">
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:itemName="{ item }"
              ><a v-on:click.stop="filterPage(item.value)">{{
                item.value
              }}</a></template
            >
          </AnalyticsBlock>
        </v-col>
        <v-col cols="3">
          <AnalyticsBlock
            :blockData="analyticsData.browser_families"
            :blockType="BlockType.AggregateStat"
            :startDate="startDate"
            :endDate="endDate"
          >
            <template v-slot:blockTitle>Browser</template>
            <template v-slot:itemName="{ item }">
              <Icon :value="item.value" />
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
            <template v-slot:itemName="{ item }">
              <Icon :value="item.value" />
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
            <template v-slot:itemName="{ item }">
              <Icon :value="item.value" />
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
            <template v-slot:itemName="{ item }">
              <Icon :value="item.value" />
              {{ item.value }}</template
            >
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
              <v-icon v-if="country" v-on:click.stop="filterCountry(undefined)">
                mdi-delete
              </v-icon>
            </template>
            <template v-slot:itemName="{ item }">
              <a
                v-on:click.stop="filterCountry(item.value)"
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
import {
  dispatchUpdateCountry,
  dispatchUpdatePage,
} from '@/store/analytics/actions';
import { readCountry, readPage } from '@/store/analytics/getters';

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

  filterPage(value: string | undefined): void {
    this.$router.push({ query: { page: value } });
    dispatchUpdatePage(this.$store, value);
  }

  filterCountry(value: string | undefined): void {
    this.$router.push({ query: { country: value } });
    dispatchUpdateCountry(this.$store, value);
  }

  countryCodeToCountryName(countryCode: string): string {
    return countryCodes[countryCode] || countryCode;
  }
}
</script>
