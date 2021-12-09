<template>
  <img
    width="24"
    height="24"
    style="vertical-align: middle"
    :src="iconUrl"
    v-if="iconUrl"
  />
  <v-icon v-else-if="iconData">{{ iconData }}</v-icon>
  <v-icon size="24" v-else>{{ mdiHelpCircleOutline }}</v-icon>
</template>

<script lang="ts">
import {
  mdiCellphone,
  mdiDesktopMac,
  mdiHelpCircleOutline,
  mdiTablet,
} from '@mdi/js';
import { Component, Prop, Vue } from 'vue-property-decorator';

const iconMap = {
  desktop: mdiDesktopMac,
  mobile: mdiCellphone,
  tablet: mdiTablet,
};

const directMatchIconMap = [
  'amazon',
  'android',
  'apple',
  'asus',
  'baidu',
  'duckduckgo',
  'facebook',
  'fedora',
  'firefox',
  'flipboard',
  'freebsd',
  'github',
  'gmail',
  'google',
  'huawei',
  'instagram',
  'ios',
  'lenovo',
  'lg',
  'linkedin',
  'linux',
  'macos',
  'medium',
  'motorola',
  'nokia',
  'oneplus',
  'openbsd',
  'opera',
  'reddit',
  'safari',
  'samsung',
  'twitter',
  'ubuntu',
  'windows',
  'xiaomi',
  'youtube',
];

const indirectIconMap = {
  'Chrome Mobile iOS': 'googlechrome',
  'Chrome OS': 'googlechrome',
  'Edge Mobile': 'microsoftedge',
  'Hacker News': 'ycombinator',
  'Opera Mobile': 'opera',
  'Product Hunt': 'producthunt',
  'Yahoo!': 'yahoo',
  'com.linkedin.android': 'linkedin',
  Bing: 'microsoftbing',
  Chrome: 'googlechrome',
  Chromium: 'googlechrome',
  Edge: 'microsoftedge',
  Googlebot: 'google',
  IE: 'internetexplorer',
};

@Component
export default class Icon extends Vue {
  @Prop() public value!: string;
  mdiHelpCircleOutline = mdiHelpCircleOutline;

  get iconData(): string | undefined {
    if (iconMap[this.value.toLowerCase()]) {
      return iconMap[this.value.toLowerCase()];
    }
    return undefined;
  }

  get iconUrl(): string | undefined {
    if (directMatchIconMap.includes(this.value.toLowerCase())) {
      return `/static/brand-icons/${this.value.toLowerCase()}.svg`;
    }
    if (indirectIconMap[this.value]) {
      return `/static/brand-icons/${indirectIconMap[
        this.value
      ].toLowerCase()}.svg`;
    }
    return undefined;
  }
}
</script>
