import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { AnalyticsState } from './state';

export const defaultState: AnalyticsState = {
  currentDomain: null,
  analyticsData: null,
  analyticsError: null,
};

export const analyticsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
