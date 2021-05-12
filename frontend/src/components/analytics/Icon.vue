<template>
  <v-icon v-if="iconName">{{ iconName }}</v-icon>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

const iconMap = {
  Android: 'mdi-android',
  Linux: 'mdi-linux',
  'Mac OS X': 'mdi-apple',
  Windows: 'mdi-microsoft-windows',
  iOS: 'mdi-apple-ios',
  Mac: 'mdi-apple',

  Facebook: 'mdi-facebook',
  Twitter: 'mdi-twitter',

  Chrome: 'mdi-google-chrome',
  Firefox: 'mdi-firefox',
};

@Component
export default class AnalyticsContainer extends Vue {
  @Prop() public value!: string;

  get iconName(): string | undefined {
    console.log(iconMap[this.value], this.value);
    if (iconMap[this.value]) {
      return iconMap[this.value];
    }
    return undefined;
  }
}
</script>
