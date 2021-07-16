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

  analyticsError: (state: AnalyticsState): string | null => {
    return state.analyticsError;
  },

  startDate: (state: AnalyticsState): Date => {
    return state.filters.start;
  },
  endDate: (state: AnalyticsState): Date => {
    return state.filters.end;
  },
};

const { read } = getStoreAccessors<AnalyticsState, RootState>('');

export const readAnalyticsData = read(getters.analyticsData);
export const readCurrentDomain = read(getters.currentDomain);
export const readStartDate = read(getters.startDate);
export const readEndDate = read(getters.endDate);
export const readAnalyticsError = read(getters.analyticsError);
