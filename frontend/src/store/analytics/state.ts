import { AnalyticsData } from '@/generated';

export interface AnalyticsFilterState {
  page: string | undefined;
  country: string | undefined;
  browser: string | undefined;
  os: string | undefined;
  device: string | undefined;
  referrerName: string | undefined;
}

export interface AnalyticsState {
  currentDomain: string | null;
  filters: AnalyticsFilterState;
  analyticsData: AnalyticsData | null;
  analyticsError: string | null;

  startDate: Date;
  endDate: Date;
}
