<template>
  <v-container>
    <router-view :key="$route.fullPath"></router-view>
    <v-container fluid v-if="analyticsError">
      <v-card class="ma-3 pa-3">
        <v-card-text>
          <div class="headline font-weight-light ma-5">
            {{ analyticsError }}
            <span v-if="isLoggedIn">Please try again in a little while.</span>
            <span v-else>
              (Are you <router-link to="/login">logged-in</router-link>?)
            </span>
          </div>
        </v-card-text>
      </v-card>
    </v-container>
    <v-container v-else-if="!analyticsData"> Loading, please wait </v-container>
    <v-container fluid v-else>
      <v-row align="baseline" no-gutters>
        <v-col cols="12" class="text-h5">
          <v-icon>{{ $vuetify.icons.values.web }}</v-icon> {{ domainName }}
        </v-col>
        <v-spacer></v-spacer>
        <v-col cols="12">
          <date-range-picker
            ref="picker"
            :locale-data="{ firstDay: 1, format: 'yyyy-mm-dd HH:mm:ss' }"
            :timePicker="true"
            opens="right"
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
                {{ formatISO9075(picker.startDate).slice(0, -3) }} -
                {{ formatISO9075(picker.endDate).slice(0, -3) }}
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
import { readIsLoggedIn } from '@/store/main/getters';

@Component({
  components: {
    AnalyticsContainer,
    DateRangePicker,
  },
})
export default class ViewAnalytics extends Vue {
  formatISO9075 = formatISO9075;

  get isLoggedIn(): boolean {
    return readIsLoggedIn(this.$store) || false;
  }
  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }

  get dateRanges(): Record<string, Array<Date>> {
    const today = new Date();
    return {
      'This month': [startOfMonth(today), today],
      'Last 1 month': [addMonths(today, -1), today],
      'This year': [startOfYear(today), today],
      'Last 1 year': [addYears(today, -1), today],
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
