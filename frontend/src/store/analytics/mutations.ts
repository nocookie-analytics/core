import { AnalyticsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';
import { AnalyticsData } from '@/generated';

export const mutations = {
  setActiveDomain(state: AnalyticsState, domainName: string): void {
    state.currentDomain = domainName;
  },
  setDomainData(state: AnalyticsState, analyticsData: AnalyticsData): void {
    state.analyticsData = analyticsData;
  },
  setAnalyticsError(state: AnalyticsState, error: string | null): void {
    state.analyticsError = error;
  },
};

const { commit } = getStoreAccessors<AnalyticsState, State>('');

export const commitSetActiveDomain = commit(mutations.setActiveDomain);
export const commitSetAnalyticsData = commit(mutations.setDomainData);
export const commitSetAnalyticsError = commit(mutations.setAnalyticsError);
