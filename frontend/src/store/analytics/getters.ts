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
    return state.startDate;
  },
  endDate: (state: AnalyticsState): Date => {
    return state.endDate;
  },

  page: (state: AnalyticsState): string | undefined => {
    return state.page;
  },
  country: (state: AnalyticsState): string | undefined => {
    return state.country;
  },
  browser: (state: AnalyticsState): string | undefined => {
    return state.browser;
  },
  os: (state: AnalyticsState): string | undefined => {
    return state.os;
  },
  device: (state: AnalyticsState): string | undefined => {
    return state.device;
  },
  referrerName: (state: AnalyticsState): string | undefined => {
    return state.referrerName;
  },
};

const { read } = getStoreAccessors<AnalyticsState, RootState>('');

export const readAnalyticsData = read(getters.analyticsData);
export const readCurrentDomain = read(getters.currentDomain);
export const readStartDate = read(getters.startDate);
export const readEndDate = read(getters.endDate);
export const readAnalyticsError = read(getters.analyticsError);
export const readPage = read(getters.page);
export const readCountry = read(getters.country);
export const readBrowser = read(getters.browser);
export const readOs = read(getters.os);
export const readDevice = read(getters.device);
export const readReferrerName = read(getters.referrerName);
