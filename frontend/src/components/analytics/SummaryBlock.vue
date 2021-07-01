<template>
  <v-container fluid v-if="summaryData">
    <v-row justify="start">
      <v-col
        v-for="block in summaryBlocks"
        :key="block.title"
        cols="6"
        lg="3"
        xl="2"
        sm="6"
      >
        <v-card outlined min-width="200" max-width="200" width="200">
          <v-card-title>{{ block.title }}</v-card-title>
          <v-card-text>
            <v-icon>{{ block.icon }}</v-icon>
            {{ block.text }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { SummaryStat } from '@/generated';
import { mdiAccountMultiple, mdiCropLandscape } from '@mdi/js';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class SummaryBlock extends Vue {
  @Prop() public summaryData!: SummaryStat;

  justifyData() {
    return {
      justify: ['start', 'center', 'end', 'space-around', 'space-between'],
    };
  }

  get summaryBlocks() {
    return [
      {
        title: 'Unique visitors',
        text: this.summaryData.visitors,
        icon: mdiAccountMultiple,
      },
      {
        title: 'Page views',
        text: this.summaryData.total_visits,
        icon: mdiCropLandscape,
      },
    ];
  }
}
</script>
