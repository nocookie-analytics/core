<template>
  <div>
    <v-container fluid>
      <span v-if="analyticsError">
        <v-card class="ma-3 pa-3">
          <v-card-text>
            <div class="headline font-weight-light ma-5">
              {{ analyticsError }} (You might need to
              <a href="/login">log-in</a>
              >
            </div>
          </v-card-text>
        </v-card>
      </span>
    </v-container>
    <v-container>
      <v-row>
        <v-datetime-picker
          class="mb-6"
          label="Start"
          v-model="datetime"
          okText="Set start date"
        >
          <template slot="dateIcon">
            <v-icon>mdi-calendar</v-icon>
          </template>
          <template slot="timeIcon">
            <v-icon>mdi-clock-outline</v-icon>
          </template>
        </v-datetime-picker>
        <v-datetime-picker
          class="mb-6"
          label="End"
          v-model="datetime"
          okText="Set end date"
        >
          <template slot="dateIcon">
            <v-icon>mdi-calendar</v-icon>
          </template>
          <template slot="timeIcon">
            <v-icon>mdi-clock-outline</v-icon>
          </template>
        </v-datetime-picker>
      </v-row>
    </v-container>
    <!--
    <span v-if="mapData">
      <ChoroplethMap :mapData="mapData"></ChoroplethMap>
    </span>
    -->
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ChoroplethMap from '@/components/ChoroplethMap.vue';
import { dispatchUpdateActiveDomain } from '@/store/analytics/actions';
import { readAnalyticsData } from '@/store/analytics/getters';
import { AggregateStat } from '@/generated';
import { AnalyticsState } from '@/store/analytics/state';

@Component({
  components: {
    ChoroplethMap,
  },
})
export default class ViewAnalytics extends Vue {
  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }

  get analyticsError(): string | null {
    return (this.$store.state as AnalyticsState).analyticsError;
  }

  public async mounted(): Promise<void> {
    dispatchUpdateActiveDomain(
      this.$store,
      this.$router.currentRoute.params.domainName,
    );
  }

  get mapData(): Array<AggregateStat> | undefined {
    return readAnalyticsData(this.$store)?.countries;
  }
}
</script>
