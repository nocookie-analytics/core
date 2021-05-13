import { AnalyticsState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { RootState } from '../state';
import { AnalyticsData } from '@/generated';
import { commitAddNotification } from '../main/mutations';

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
  setStartDate(state: AnalyticsState, startDate: Date): void {
    state.startDate = startDate;
  },
  setEndDate(state: AnalyticsState, endDate: Date): void {
    state.endDate = endDate;
  },

  setFilter(
    state: AnalyticsState,
    { key, value }: { key: string; value: string | undefined },
  ): void {
    state[key] = value;
  },

  setPage(state: AnalyticsState, page: string | undefined): void {
    state.page = page;
  },
  setCountry(state: AnalyticsState, country: string | undefined): void {
    state.country = country;
  },
};

const { commit } = getStoreAccessors<AnalyticsState, RootState>('');

export const commitSetActiveDomain = commit(mutations.setActiveDomain);
export const commitSetAnalyticsData = commit(mutations.setDomainData);
export const commitSetAnalyticsError = commit(mutations.setAnalyticsError);
export const commitSetStartDate = commit(mutations.setStartDate);
export const commitSetEndDate = commit(mutations.setEndDate);
export const commitSetFilter = commit(mutations.setFilter);
export const commitSetPage = commit(mutations.setPage);
export const commitSetCountry = commit(mutations.setCountry);
