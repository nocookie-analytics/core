<template>
  <v-icon v-if="iconName">{{ iconName }}</v-icon>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

import {
  mdiAndroid,
  mdiApple,
  mdiAppleIos,
  mdiAppleSafari,
  mdiFacebook,
  mdiFedora,
  mdiFirefox,
  mdiGithub,
  mdiGoogle,
  mdiGoogleChrome,
  mdiInstagram,
  mdiLinux,
  mdiMicrosoftBing,
  mdiMicrosoftEdge,
  mdiMicrosoftWindows,
  mdiOpera,
  mdiSpider,
  mdiTwitter,
  mdiUbuntu,
} from '@mdi/js';

const iconMap = {
  Android: mdiAndroid,
  Apple: mdiApple,
  Bing: mdiMicrosoftBing,
  Chrome: mdiGoogleChrome,
  'Chrome OS': mdiGoogleChrome,
  Edge: mdiMicrosoftEdge,
  Facebook: mdiFacebook,
  Fedora: mdiFedora,
  Firefox: mdiFirefox,
  GitHub: mdiGithub,
  Google: mdiGoogle,
  Googlebot: mdiGoogle,
  Instagram: mdiInstagram,
  Linux: mdiLinux,
  Mac: mdiApple,
  'Mac OS X': mdiApple,
  Opera: mdiOpera,
  Safari: mdiAppleSafari,
  Spider: mdiSpider,
  Twitter: mdiTwitter,
  Ubuntu: mdiUbuntu,
  Windows: mdiMicrosoftWindows,
  iOS: mdiAppleIos,
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