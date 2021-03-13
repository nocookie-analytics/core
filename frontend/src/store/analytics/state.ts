import { AnalyticsData } from '@/generated';

export interface AnalyticsState {
  currentDomain: string | null;
  analyticsData: AnalyticsData | null;
  analyticsError: string | null;
}
