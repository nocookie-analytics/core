import { AdminState } from './admin/state';
import { AnalyticsState } from './analytics/state';
import { MainState } from './main/state';

export interface RootState {
  main: MainState;
  analytics: AnalyticsState;
  admin: AdminState;
}
