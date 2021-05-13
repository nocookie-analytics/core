import { AnalyticsData } from '@/generated';

export interface AnalyticsState {
  currentDomain: string | null;
  page: string | undefined;
  country: string | undefined;
  browser: string | undefined;
  os: string | undefined;
  device: string | undefined;
  referrerName: string | undefined;
  analyticsData: AnalyticsData | null;
  analyticsError: string | null;

  startDate: Date;
  endDate: Date;
}
