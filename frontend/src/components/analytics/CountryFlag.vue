<template>
  <img width="24" :src="countryFlagUrl" />
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class CountryFlag extends Vue {
  @Prop() public countryName!: string;

  get countryFlagUrl(): string {
    return `/static/flags/${this.countryName.toLowerCase()}.svg`;
  }
}
</script>
