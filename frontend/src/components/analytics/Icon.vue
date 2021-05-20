<template>
  <v-icon v-if="iconName">{{ iconName }}</v-icon>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

const iconMap = {
  Android: 'mdi-android',
  Apple: 'mdi-apple',
  Bing: 'mdi-microsoft-bing',
  Chrome: 'mdi-google-chrome',
  'Chrome OS': 'mdi-google-chrome',
  Edge: 'mdi-microsoft-edge',
  Facebook: 'mdi-facebook',
  Fedora: 'mdi-fedora',
  Firefox: 'mdi-firefox',
  GitHub: 'mdi-github',
  Google: 'mdi-google',
  Googlebot: 'mdi-google',
  Instagram: 'mdi-instagram',
  Linux: 'mdi-linux',
  Mac: 'mdi-apple',
  'Mac OS X': 'mdi-apple',
  Opera: 'mdi-opera',
  Safari: 'mdi-apple-safari',
  Spider: 'mdi-spider',
  Twitter: 'mdi-twitter',
  Ubuntu: 'mdi-ubuntu',
  Windows: 'mdi-microsoft-windows',
  iOS: 'mdi-apple-ios',
};

@Component
export default class AnalyticsContainer extends Vue {
  @Prop() public value!: string;

  get iconName(): string | undefined {
    if (iconMap[this.value]) {
      return iconMap[this.value];
    }
    return undefined;
  }
}
</script>
