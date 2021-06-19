<template><span>Title</span></template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { DeclarativeBlockType } from './interfaces';

@Component
export default class AnalyticsBlockTitle extends Vue {
  @Prop() block!: DeclarativeBlockType;
}
</script>
