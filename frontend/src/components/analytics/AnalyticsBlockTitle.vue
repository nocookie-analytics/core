<template>
  <span
    >{{ block.title }}

    <router-link :to="urlWithRemovedFilter" v-if="isFilterActive">
      <v-icon> {{ $vuetify.icons.values.delete }} </v-icon>
    </router-link>
    <span v-if="totalPages > 1">
      <v-icon :disabled="currentPage === 0" @click="$emit('prev-page')">{{
        $vuetify.icons.values.chevronLeft
      }}</v-icon>
      {{ currentPage + 1 }}/{{ totalPages }}
      <v-icon
        :disabled="currentPage === totalPages - 1"
        @click="$emit('next-page')"
        >{{ $vuetify.icons.values.chevronRight }}</v-icon
      >
    </span>
  </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { DeclarativeAnalyticsBlock } from './interfaces';

@Component
export default class AnalyticsBlockTitle extends Vue {
  @Prop() block!: DeclarativeAnalyticsBlock;
  @Prop() currentPage!: number;
  @Prop() totalPages!: number;

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
