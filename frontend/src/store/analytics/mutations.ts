import { AnalyticsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { State } from '../state';

export const mutations = {
  setActiveDomain(state: AnalyticsState, domainName: string): void {
    state.currentDomain = domainName;
  },
  setDomainData(state: AnalyticsState, analyticsData: any): void {
    state.analyticsData = analyticsData;
  },
};

const { commit } = getStoreAccessors<AnalyticsState, State>('');

export const commitSetActiveDomain = commit(mutations.setActiveDomain);
export const commitSetAnalyticsData = commit(mutations.setDomainData);
