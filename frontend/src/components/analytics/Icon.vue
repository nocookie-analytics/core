<template>
  <img
    width="24"
    height="24"
    style="vertical-align: middle"
    :src="iconUrl"
    v-if="iconUrl"
  />
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

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
};

@Component
export default class Icon extends Vue {
  @Prop() public value!: string;

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
