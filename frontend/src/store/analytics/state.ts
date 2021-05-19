import { AnalyticsData } from '@/generated';

export interface BaseAnalyticsFilterState {
  page: string | undefined;
  country: string | undefined;
  browser: string | undefined;
  os: string | undefined;
  device: string | undefined;
  referrerName: string | undefined;
}

export interface AnalyticsFilterState extends BaseAnalyticsFilterState {
  start: Date;
  end: Date;
}

export interface AnalyticsState {
  currentDomain: string | null;
  filters: AnalyticsFilterState;
  analyticsData: AnalyticsData | null;
  analyticsError: string | null;
}
