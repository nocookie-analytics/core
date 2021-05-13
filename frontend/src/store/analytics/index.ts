import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { AnalyticsState } from './state';
import { addDays, isValid, parseISO } from 'date-fns';

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

const now = new Date();

export const defaultState: AnalyticsState = {
  currentDomain: null,
  analyticsData: null,
  analyticsError: null,

  startDate: readDateFromURLParam('start', addDays(now, -30)),
  endDate: readDateFromURLParam('end', now),
  page: getURLParamValue('page'),
  country: getURLParamValue('country'),
  browser: getURLParamValue('browser'),
  device: getURLParamValue('device'),
  os: getURLParamValue('os'),
  referrerName: getURLParamValue('referrerName'),
};

console.log(defaultState);
export const analyticsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
