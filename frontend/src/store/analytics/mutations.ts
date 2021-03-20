import { AnalyticsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { RootState } from '../state';
import { AnalyticsData } from '@/generated';

export const mutations = {
  setActiveDomain(state: AnalyticsState, domainName: string): void {
    state.currentDomain = domainName;
    state.analyticsError = null; // New domain should not have any error to start off with
    state.analyticsData = null;
  },
  setDomainData(state: AnalyticsState, analyticsData: AnalyticsData): void {
    state.analyticsData = analyticsData;
  },
  setAnalyticsError(state: AnalyticsState, error: string | null): void {
    state.analyticsError = error;
    state.analyticsData = null;
  },
};

const { commit } = getStoreAccessors<AnalyticsState, RootState>('');

export const commitSetActiveDomain = commit(mutations.setActiveDomain);
export const commitSetAnalyticsData = commit(mutations.setDomainData);
export const commitSetAnalyticsError = commit(mutations.setAnalyticsError);
