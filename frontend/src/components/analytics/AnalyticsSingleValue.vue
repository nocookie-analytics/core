<template>
  <span class="fixed-min-width">
    <span v-if="urlParamName === 'country'" class="nowrap">
      <country-flag :countryName="itemValue" style="margin-right: 5px" />
      <optional-router-link
        :to="filterOnThisItemUrl"
        :disabled="!filterOnThisItemUrl.query"
        >{{ countryCodeToCountryName(itemValue) }}</optional-router-link
      >
    </span>
    <span v-else-if="urlParamName === 'page'">
      <span class="nowrap">
        <optional-router-link
          :to="filterOnThisItemUrl"
          :disabled="!filterOnThisItemUrl.query"
          >{{ itemValue }}</optional-router-link
        >
      </span>
      <a
        :href="externalLink"
        rel="noopener"
        target="_blank"
        class="external-link"
      >
        <v-icon>{{ $vuetify.icons.values.openInNew }}</v-icon>
      </a>
    </span>
    <span v-else>
      <Icon :value="itemValue" v-if="!noIcon" />&nbsp;<optional-router-link
        :to="filterOnThisItemUrl"
        :disabled="!filterOnThisItemUrl.query"
        >{{ itemValue }}</optional-router-link
      ></span
    >
  </span>
</template>
<script lang="ts">
import countryCodes from '@/components/data/countryCodes';
import { Component, Prop, Vue } from 'vue-property-decorator';
import Icon from '@/components/analytics/Icon.vue';
import CountryFlag from '@/components/analytics/CountryFlag.vue';
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
  @Prop() public value!: string;
  @Prop() public noIcon!: boolean;
  @Prop() public urlParamName?: string;
  @Prop() public urlExclude?: Array<string>;

  countryCodeToCountryName(countryCode: string): string {
    return countryCodes[countryCode] || countryCode;
  }

  get itemValue(): string {
    return this.value;
  }

  get externalLink(): string {
    const domainName = readCurrentDomain(this.$store);
    return `https://${domainName}${this.value}`;
  }

  get filterOnThisItemUrl() {
    if (this.urlParamName) {
      const value = this.itemValue;
      const excludes = this.urlExclude;
      if (excludes && !excludes.includes(value)) {
        return {
          query: {
            ...this.$route.query,
            [this.urlParamName]: value,
          },
        };
      }
    }
    return { query: null };
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
  max-width: 240px;
}
.external-link {
  margin-left: 5px;
  vertical-align: super;
}
</style>
