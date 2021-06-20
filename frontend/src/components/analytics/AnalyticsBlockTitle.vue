<template>
  <span
    >{{ block.title }}

    <router-link :to="urlWithRemovedFilter" v-if="isFilterActive">
      <v-icon> {{ $vuetify.icons.values.delete }} </v-icon>
    </router-link>
  </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { DeclarativeAnalyticsBlock } from './interfaces';

@Component
export default class AnalyticsBlockTitle extends Vue {
  @Prop() block!: DeclarativeAnalyticsBlock;

  get isFilterActive(): boolean {
    return Boolean(
      this.block.urlParamName && this.$route.query[this.block.urlParamName],
    );
  }

  get urlWithRemovedFilter() {
    if (this.isFilterActive) {
      return {
        query: {
          ...this.$route.query,
          [this.block.urlParamName!]: undefined,
        },
      };
    }
    return undefined;
  }
}
</script>
