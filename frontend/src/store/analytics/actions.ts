import { AnalyticsApi, AnalyticsType } from '@/generated';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { RootState } from '../state';
import {
  commitSetActiveDomain,
  commitSetAnalyticsData,
  commitSetAnalyticsError,
  commitSetCountry,
  commitSetFilter,
  commitSetPage,
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

  async updateAnalyticsFilter(
    context: AnalyticsContext,
    { value, key }: { value: string | undefined; key: string },
  ): Promise<void> {
    commitSetFilter(context, { key, value });
    commitSetAnalyticsError(context, null);
    await dispatchFetchDomainAnalytics(context);
  },

  async updatePage(
    context: AnalyticsContext,
    page: string | undefined,
  ): Promise<void> {
    commitSetPage(context, page);
    commitSetAnalyticsError(context, null);
    await dispatchFetchDomainAnalytics(context);
  },

  async updateCountry(
    context: AnalyticsContext,
    page: string | undefined,
  ): Promise<void> {
    commitSetCountry(context, page);
    commitSetAnalyticsError(context, null);
    await dispatchFetchDomainAnalytics(context);
  },

  async fetchDomainAnalytics(context: AnalyticsContext): Promise<void> {
    const analyticsApi = context.getters.analyticsApi as AnalyticsApi;
    const domainName = context.state.currentDomain as string;
    commitSetAnalyticsError(context, null);
    if (domainName === null) {
      console.error('Cannot fetch analytics data without a domain');
      return Promise.resolve();
    }
    try {
      const response = await analyticsApi.getAnalytics({
        domainName,
        include: [
          AnalyticsType.Pages,
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
        page: context.state.page,
        country: context.state.country,
        start: context.state.startDate.toISOString(),
        end: context.state.endDate.toISOString(),
      });
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
export const dispatchUpdateAnalyticsFilter = dispatch(
  actions.updateAnalyticsFilter,
);
