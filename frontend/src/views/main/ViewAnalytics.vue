<template>
  <v-container fluid class="pa-0 ma-0">
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
      <v-row align="baseline" no-gutters>
        <v-col xs="12">
          {{ domainName }}
        </v-col>
        <v-spacer></v-spacer>
        <v-col xs="12" xl="5" align="right">
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
            :max-date="new Date()"
            :ranges="dateRanges"
          >
            <template v-slot:input="picker">
              <v-card flat class="text-no-wrap text-truncate">
                {{ formatISO9075(picker.startDate) }} -
                {{ formatISO9075(picker.endDate) }}
              </v-card>
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
import DateRangePicker from 'vue2-daterange-picker/src/index';
import 'vue2-daterange-picker/dist/vue2-daterange-picker.css';
import {
  readAnalyticsData,
  readAnalyticsError,
  readEndDate,
  readStartDate,
} from '@/store/analytics/getters';
import { AnalyticsData } from '@/generated';
import { getFiltersFromUrl } from '@/store/analytics';
import {
  addMonths,
  addYears,
  startOfMonth,
  startOfYear,
  formatISO9075,
} from 'date-fns';

@Component({
  components: {
    AnalyticsContainer,
    DateRangePicker,
  },
})
export default class ViewAnalytics extends Vue {
  formatISO9075 = formatISO9075;
  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }

  get dateRanges(): Record<string, Array<Date>> {
    const today = new Date();
    return {
      'This month': [startOfMonth(today), today],
      'Last 1 month': [addMonths(today, -1), today],
      'This year': [startOfYear(today), today],
      'Last 1 year': [addYears(today, -12), today],
    };
  }

  get dateRange(): Record<string, Date> {
    return {
      startDate: readStartDate(this.$store),
      endDate: readEndDate(this.$store),
    };
  }

  set dateRange(dateRange: Record<string, Date>) {
    this.$router.replace({
      query: {
        ...this.$route.query,
        start: dateRange.startDate.toISOString(),
        end: dateRange.endDate.toISOString(),
      },
    });
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
.vue-daterange-picker {
  display: block !important;
}
.reportrange-text {
  border: none !important;
}
</style>
