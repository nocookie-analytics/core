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
      <v-row align="baseline">
        <v-col cols="2">
          {{ domainName }}
        </v-col>
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
    <v-container>
      <AnalyticsContainer :analyticsData="analyticsData" />
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import AnalyticsContainer from '@/components/AnalyticsContainer.vue';
import {
  dispatchFetchDomainAnalytics,
  dispatchUpdateActiveDomain,
} from '@/store/analytics/actions';
import {
  readAnalyticsData,
  readAnalyticsError,
  readEndDate,
  readStartDate,
} from '@/store/analytics/getters';
import { AnalyticsData } from '@/generated';
import {
  commitSetEndDate,
  commitSetStartDate,
} from '@/store/analytics/mutations';

@Component({
  components: {
    AnalyticsContainer,
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
    this.setQueryParam('start', value.toISOString());
  }

  get endDate(): Date {
    return readEndDate(this.$store);
  }

  set endDate(value: Date) {
    commitSetEndDate(this.$store, value);
    this.setQueryParam('end', value.toISOString());
  }

  get analyticsError(): string | null {
    return readAnalyticsError(this.$store);
  }

  setQueryParam(key: string, value: string): void {
    this.$router.replace({ query: { ...this.$route.query, [key]: value } });
  }

  @Watch('startDate')
  @Watch('endDate')
  async updateData(): Promise<void> {
    await dispatchFetchDomainAnalytics(this.$store);
  }

  public async mounted(): Promise<void> {
    await dispatchUpdateActiveDomain(
      this.$store,
      this.$router.currentRoute.params.domainName,
    );
  }

  get analyticsData(): AnalyticsData | null {
    return readAnalyticsData(this.$store);
  }
}
</script>
