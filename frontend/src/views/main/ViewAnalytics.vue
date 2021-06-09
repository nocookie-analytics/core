<template>
  <v-container fluid>
    <router-view :key="$route.fullPath"></router-view>
    <v-container fluid>
      <span v-if="analyticsError">
        <v-card class="ma-3 pa-3">
          <v-card-text>
            <div class="headline font-weight-light ma-5">
              {{ analyticsError }} (You might need to
              <a href="/login">log-in)</a>
            </div>
          </v-card-text>
        </v-card>
      </span>
    </v-container>
    <v-container fluid>
      <v-row align="baseline" class="mb-6" no-gutters>
        <v-col>
          {{ domainName }}
        </v-col>
        <v-spacer></v-spacer>
        <v-col align="right">
          <date-range-picker
            ref="picker"
            :locale-data="{ firstDay: 1, format: 'yyyy-mm-dd HH:mm:ss' }"
            :timePicker="true"
            opens="left"
            :timePicker24Hour="true"
            :showWeekNumbers="true"
            :showDropdowns="true"
            :autoApply="true"
            v-model="dateRange"
          >
            <template v-slot:input="picker" style="min-width: 800px">
              {{ picker.startDate.toLocaleString() }} -
              {{ picker.endDate.toLocaleString() }}
            </template>
          </date-range-picker>
        </v-col>
      </v-row>
    </v-container>
    <AnalyticsContainer :analyticsData="analyticsData" />
  </v-container>
</template>

<script lang="ts">
import { Component, Vue, Watch } from 'vue-property-decorator';
import AnalyticsContainer from '@/components/analytics/AnalyticsContainer.vue';
import { dispatchOverwriteAnalyticsFilters } from '@/store/analytics/actions';
import DateRangePicker from 'vue2-daterange-picker';
import 'vue2-daterange-picker/dist/vue2-daterange-picker.css';
import {
  readAnalyticsData,
  readAnalyticsError,
  readEndDate,
  readStartDate,
} from '@/store/analytics/getters';
import { AnalyticsData } from '@/generated';
import { getFiltersFromUrl } from '@/store/analytics';

@Component({
  components: {
    AnalyticsContainer,
    DateRangePicker,
  },
})
export default class ViewAnalytics extends Vue {
  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }

  get dateRange() {
    return {
      startDate: readStartDate(this.$store),
      endDate: readEndDate(this.$store),
    };
  }

  set dateRange(dateRange) {
    this.$router.replace({
      query: {
        ...this.$route.query,
        start: dateRange.startDate.toISOString(),
        end: dateRange.endDate.toISOString(),
      },
    });
  }

  get startDate(): Date {
    return readStartDate(this.$store);
  }

  set startDate(value: Date) {
    this.setQueryParam('start', value.toISOString());
  }

  get endDate(): Date {
    return readEndDate(this.$store);
  }

  set endDate(value: Date) {
    this.setQueryParam('end', value.toISOString());
  }

  get analyticsError(): string | null {
    return readAnalyticsError(this.$store);
  }

  setQueryParam(key: string, value: string): void {
    this.$router.replace({ query: { ...this.$route.query, [key]: value } });
  }

  @Watch('$route', { immediate: true, deep: true })
  async onUrlChange(): Promise<void> {
    await dispatchOverwriteAnalyticsFilters(this.$store, {
      filters: getFiltersFromUrl(),
      domainName: this.$router.currentRoute.params.domainName,
    });
  }

  get analyticsData(): AnalyticsData | null {
    return readAnalyticsData(this.$store);
  }
}
</script>

<style>
.calendars {
  flex-wrap: nowrap !important;
}

@media only screen and (max-width: 800px) {
  .calendars > .ranges > ul > li {
    text-align: right;
  }
}
</style>
