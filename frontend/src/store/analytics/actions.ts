import { AnalyticsApi, AnalyticsType } from '@/generated';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import {
  commitSetActiveDomain,
  commitSetAnalyticsData,
  commitSetAnalyticsError,
} from './mutations';
import { AnalyticsState } from './state';

type AnalyticsContext = ActionContext<AnalyticsState, State>;

export const actions = {
  async updateActiveDomain(
    context: AnalyticsContext,
    domainName: string,
  ): Promise<void> {
    commitSetActiveDomain(context, domainName);
    commitSetAnalyticsError(context, null);
    await dispatchFetchDomainAnalytics(context);
  },

  async fetchDomainAnalytics(context: AnalyticsContext): Promise<void> {
    const analyticsApi = context.getters.analyticsApi as AnalyticsApi;
    const domainName = context.state.currentDomain as string;
    try {
      const response = await analyticsApi.getAnalytics(
        domainName,
        [AnalyticsType.Countries, AnalyticsType.UtmTerms],
        '2020-03-11T17:11:24.931589+00:00',
      );
      const analyticsData = response.data;
      commitSetAnalyticsData(context, analyticsData);
    } catch (e) {
      commitSetAnalyticsError(
        context,
        'Domain not found. You might need to login',
      );
    }
  },
};

const { dispatch } = getStoreAccessors<AnalyticsState, State>('');

export const dispatchUpdateActiveDomain = dispatch(actions.updateActiveDomain);
export const dispatchFetchDomainAnalytics = dispatch(
  actions.fetchDomainAnalytics,
);
