import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { AnalyticsFilterState, AnalyticsState } from './state';
import { addDays, isValid, parseISO } from 'date-fns';
import { DeviceType } from '@/generated';

const getURLParamValue = (urlParamName: string): string | undefined => {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(urlParamName) || undefined;
};

const readDateFromURLParam = (
  urlParamName: string,
  defaultValue: Date,
): Date => {
  const dateString = getURLParamValue(urlParamName);
  if (dateString) {
    const parsedDate = parseISO(dateString);
    if (isValid(parsedDate)) {
      return parsedDate;
    }
  }
  return defaultValue;
};

const mapDeviceStringToDeviceEnum = (
  device?: string,
): DeviceType | undefined => {
  // Damn Typescript, where can't I reverse map Enum's?
  for (const [key, value] of Object.entries(DeviceType)) {
    if (value === device) {
      return DeviceType[key];
    }
  }
  return undefined;
};

export const getFiltersFromUrl = (): AnalyticsFilterState => {
  const now = new Date();

  return {
    page: getURLParamValue('page'),
    country: getURLParamValue('country'),
    browser: getURLParamValue('browser'),
    device: mapDeviceStringToDeviceEnum(getURLParamValue('device')),
    deviceBrand: getURLParamValue('deviceBrand'),
    os: getURLParamValue('os'),
    referrerName: getURLParamValue('referrerName'),
    start: readDateFromURLParam('start', addDays(now, -30)),
    end: readDateFromURLParam('end', now),
  };
};

export const defaultState: AnalyticsState = {
  currentDomain: null,
  analyticsData: null,
  analyticsError: null,
  filters: getFiltersFromUrl(),
};

export const analyticsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
