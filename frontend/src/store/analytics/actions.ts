import { AnalyticsApi, AnalyticsType } from '@/generated';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { RootState } from '../state';
import {
  commitSetActiveDomain,
  commitSetAnalyticsData,
  commitSetAnalyticsError,
} from './mutations';
import { AnalyticsState } from './state';

export type AnalyticsContext = ActionContext<AnalyticsState, RootState>;

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
    if (domainName === null) {
      console.error('Cannot fetch analytics data without a domain');
      return Promise.resolve();
    }
    try {
      const response = await analyticsApi.getAnalytics(
        domainName,
        [
          AnalyticsType.Pageviews,
          AnalyticsType.Countries,

          AnalyticsType.ReferrerNames,
          AnalyticsType.ReferrerMediums,

          AnalyticsType.OsFamilies,
          AnalyticsType.BrowserFamilies,
          AnalyticsType.DeviceFamilies,

          AnalyticsType.PageviewsPerDay,
          AnalyticsType.LcpPerDay,
          AnalyticsType.FpPerDay,
          AnalyticsType.ClsPerDay,

          AnalyticsType.UtmSources,
          AnalyticsType.UtmTerms,
          AnalyticsType.UtmMediums,
          AnalyticsType.UtmContents,
          AnalyticsType.UtmCampaigns,
        ],
        context.state.startDate.toISOString(),
        context.state.endDate.toISOString(),
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

const { dispatch } = getStoreAccessors<AnalyticsState, RootState>('');

export const dispatchUpdateActiveDomain = dispatch(actions.updateActiveDomain);
export const dispatchFetchDomainAnalytics = dispatch(
  actions.fetchDomainAnalytics,
);
