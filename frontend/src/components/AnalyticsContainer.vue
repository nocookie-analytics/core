<template>
  <div>Hello world!</div>
</template>

<script lang="ts">
import { AnalyticsData } from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class AnalyticsContainer extends Vue {
  @Prop() public analyticsData!: AnalyticsData;
}
</script>
