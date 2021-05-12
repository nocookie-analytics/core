import { AnalyticsData } from '@/generated';

export interface AnalyticsState {
  currentDomain: string | null;
  page: string | undefined;
  country: string | undefined;
  analyticsData: AnalyticsData | null;
  analyticsError: string | null;

  startDate: Date;
  endDate: Date;
}
