import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { AnalyticsState } from './state';
import { addDays } from 'date-fns';

const now = new Date();

export const defaultState: AnalyticsState = {
  currentDomain: null,
  analyticsData: null,
  analyticsError: null,

  startDate: addDays(now, -30),
  endDate: now,
};

export const analyticsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
