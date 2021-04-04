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
        <v-col cols="2">
          <v-datetime-picker
            class="mb-3"
            label="Start"
            v-model="startDate"
            okText="Set start date"
          >
            <template slot="dateIcon">
              <v-icon>mdi-calendar</v-icon>
            </template>
            <template slot="timeIcon">
              <v-icon>mdi-clock-outline</v-icon>
            </template>
          </v-datetime-picker>
        </v-col>
        <v-col cols="2">
          <v-datetime-picker
            label="End"
            v-model="endDate"
            okText="Set end date"
          >
            <template slot="dateIcon">
              <v-icon>mdi-calendar</v-icon>
            </template>
            <template slot="timeIcon">
              <v-icon>mdi-clock-outline</v-icon>
            </template>
          </v-datetime-picker>
        </v-col>
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
import {
  readAnalyticsData,
  readAnalyticsError,
  readEndDate,
  readStartDate,
} from '@/store/analytics/getters';
import { AggregateStat } from '@/generated';
import { AnalyticsState } from '@/store/analytics/state';
import {
  commitSetEndDate,
  commitSetStartDate,
} from '@/store/analytics/mutations';

@Component({
  components: {
    ChoroplethMap,
  },
})
export default class ViewAnalytics extends Vue {
  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }

  get startDate(): Date {
    return readStartDate(this.$store);
  }

  set startDate(value: Date) {
    commitSetStartDate(this.$store, value);
  }

  get endDate(): Date {
    return readEndDate(this.$store);
  }
  set endDate(value: Date) {
    commitSetEndDate(this.$store, value);
  }

  get analyticsError(): string | null {
    return readAnalyticsError(this.$store);
  }

  public async mounted(): Promise<void> {
    await dispatchUpdateActiveDomain(
      this.$store,
      this.$router.currentRoute.params.domainName,
    );
  }

  get mapData(): Array<AggregateStat> | undefined {
    return readAnalyticsData(this.$store)?.countries;
  }
}
</script>
