<template>
  <span class="fixed-min-width">
    <span v-if="block.urlParamName === 'country'" class="nowrap">
      <country-flag :countryName="item.value" style="margin-right: 5px" />
      <optional-router-link
        :to="filterOnThisItemUrl"
        :disabled="!filterOnThisItemUrl"
        >{{ countryCodeToCountryName(item.value) }}</optional-router-link
      >
    </span>
    <span v-else-if="block.urlParamName === 'page'">
      <span class="nowrap">
        <optional-router-link
          :to="filterOnThisItemUrl"
          :disabled="!filterOnThisItemUrl"
          >{{ item.value }}</optional-router-link
        >
      </span>
      <a
        :href="externalLink"
        rel="noopener"
        target="_blank"
        class="external-link"
      >
        <Icon value="openInNew" />
      </a>
    </span>
    <span v-else>
      <Icon :value="item.value" /><optional-router-link
        :to="filterOnThisItemUrl"
        :disabled="!filterOnThisItemUrl"
        >{{ item.value }}</optional-router-link
      ></span
    >
  </span>
</template>
<script lang="ts">
import countryCodes from '@/components/data/countryCodes';
import { Component, Prop, Vue } from 'vue-property-decorator';
import Icon from '@/components/analytics/Icon.vue';
import CountryFlag from '@/components/analytics/CountryFlag.vue';
import { DeclarativeAnalyticsBlock } from './interfaces';
import { AggregateStat } from '@/generated';
import { readCurrentDomain } from '@/store/analytics/getters';
import OptionalRouterLink from './OptionalRouterLink.vue';

@Component({
  components: {
    CountryFlag,
    Icon,
    OptionalRouterLink,
  },
})
export default class AnalyticsSingleValue extends Vue {
  @Prop() public block!: DeclarativeAnalyticsBlock;
  @Prop() public item!: AggregateStat;

  countryCodeToCountryName(countryCode: string): string {
    return countryCodes[countryCode] || countryCode;
  }

  get externalLink(): string {
    const domainName = readCurrentDomain(this.$store);
    return `https://${domainName}${this.item.value}`;
  }

  get filterOnThisItemUrl() {
    if (this.block.urlParamName && this.block.data.length > 1) {
      const value = this.item.value;
      const excludes = this.block.urlExclude;
      if (excludes && !excludes.includes(value)) {
        return {
          ...this.$route.query,
          [this.block.urlParamName]: value,
        };
      }
    }
    return null;
  }
}
</script>

<style scoped>
.fixed-min-width {
  min-width: 200px;
  display: block;
}
.nowrap {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: inline-block;
  max-width: 250px;
}
.external-link {
  margin-left: 5px;
  vertical-align: super;
}
</style>
