import { AnalyticsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { RootState } from '../state';
import { AnalyticsData } from '@/generated';

export const getters = {
  analyticsData: (state: AnalyticsState): AnalyticsData | null => {
    return state.analyticsData;
  },

  currentDomain: (state: AnalyticsState): string | null => {
    return state.currentDomain;
  },
};

const { read } = getStoreAccessors<AnalyticsState, RootState>('');

export const readAnalyticsData = read(getters.analyticsData);
export const readCurrentDomain = read(getters.currentDomain);
