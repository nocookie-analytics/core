<template>
  <span v-if="valueType === 'country'" class="nowrap">
    <country-flag :countryName="value" />
    {{ countryCodeToCountryName(value) }}
  </span>
  <span v-else class="nowrap"> <Icon :value="value" />&nbsp; {{ value }} </span>
</template>
<script lang="ts">
import countryCodes from '@/components/data/countryCodes';
import { Component, Prop, Vue } from 'vue-property-decorator';
import Icon from '@/components/analytics/Icon.vue';
import CountryFlag from '@/components/analytics/CountryFlag.vue';

@Component({
  components: {
    CountryFlag,
    Icon,
  },
})
export default class AnalyticsValue extends Vue {
  @Prop() public valueType!: string;
  @Prop() public value!: string;

  countryCodeToCountryName(countryCode: string): string {
    return countryCodes[countryCode] || countryCode;
  }
}
</script>

<style scoped>
.nowrap {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
  max-width: 400px;
  min-width: 200px;
}
</style>
