import { mutations } from './mutations';
import { getters } from './getters';
import { actions } from './actions';
import { AnalyticsState } from './state';
import { addDays, isValid, parseISO } from 'date-fns';

const readDateFromURLParam = (
  urlParamName: string,
  defaultValue: Date,
): Date => {
  const urlParams = new URLSearchParams(window.location.search);
  const dateString = urlParams.get(urlParamName);
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
  page: undefined,
  country: undefined,
};

export const analyticsModule = {
  state: defaultState,
  mutations,
  actions,
  getters,
};
