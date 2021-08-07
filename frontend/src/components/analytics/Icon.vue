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
  'android',
  'android',
  'apple',
  'baidu',
  'duckduckgo',
  'facebook',
  'firefox',
  'fedora',
  'github',
  'google',
  'huawei',
  'instagram',
  'ios',
  'linux',
  'macos',
  'medium',
  'nokia',
  'opera',
  'safari',
  'samsung',
  'twitter',
  'ubuntu',
  'windows',
  'xiaomi',
];

const indirectIconMap = {
  Bing: 'microsoftbing',
  Chrome: 'googlechrome',
  Chromium: 'googlechrome',
  Edge: 'microsoftedge',
  Googlebot: 'google',
  'Hacker News': 'ycombinator',
  'Yahoo!': 'yahoo',
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
