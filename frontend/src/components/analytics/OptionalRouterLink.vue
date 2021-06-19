<template>
  <router-link v-if="!disabled" v-bind="$attrs">
    <slot />
  </router-link>

  <span v-else v-bind="$attrs">
    <slot />
  </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class OptionalRouterLink extends Vue {
  @Prop() disabled!: boolean;
}
</script>
