<template>
  <span
    >{{ block.title }}

    <router-link :to="urlWithRemovedFilter" v-if="isFilterActive">
      <v-icon> {{ $vuetify.icons.values.delete }} </v-icon>
    </router-link>
    <span v-if="totalPages > 1">
      <v-btn icon :disabled="currentPage === 0" @click="$emit('prev-page')"
        ><v-icon>{{ $vuetify.icons.values.chevronLeft }}</v-icon></v-btn
      >
      {{ currentPage + 1 }}/{{ totalPages }}

      <v-btn
        :disabled="currentPage === totalPages - 1"
        icon
        @click="$emit('next-page')"
      >
        <v-icon>{{ $vuetify.icons.values.chevronRight }}</v-icon>
      </v-btn>
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
