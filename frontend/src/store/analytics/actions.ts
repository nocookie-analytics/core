import { AnalyticsApi, AnalyticsType, IntervalType } from '@/generated';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { RootState } from '../state';
import {
  commitSetActiveDomain,
  commitSetAnalyticsData,
  commitSetAnalyticsError,
  commitSetFilters,
} from './mutations';
import { AnalyticsFilterState, AnalyticsState } from './state';

export type AnalyticsContext = ActionContext<AnalyticsState, RootState>;

export const actions = {
  async overwriteAnalyticsFilters(
    context: AnalyticsContext,
    {
      filters,
      domainName,
    }: { filters: AnalyticsFilterState; domainName: string },
  ): Promise<void> {
    commitSetActiveDomain(context, domainName);
    commitSetFilters(context, filters);
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
      const start = context.state.filters.start;
      const end = context.state.filters.end;
      let interval = IntervalType.Day;
      if ((end.valueOf() - start.valueOf()) / 1000 <= 86400 * 7) {
        // If the filter interval is shorter than 7 days, then show a hourly view
        interval = IntervalType.Hour;
      }
      const response = await analyticsApi.getAnalytics({
        domainName,
        include: [
          AnalyticsType.Summary,

          AnalyticsType.Pages,
          AnalyticsType.Countries,

          AnalyticsType.ReferrerNames,

          AnalyticsType.OsFamilies,
          AnalyticsType.BrowserFamilies,
          AnalyticsType.DeviceFamilies,

          AnalyticsType.PageviewsPerDay,

          AnalyticsType.UtmSources,
          AnalyticsType.UtmTerms,
          AnalyticsType.UtmMediums,
          AnalyticsType.UtmContents,
          AnalyticsType.UtmCampaigns,
        ],
        ...context.state.filters,
        // start and end are already part of destructured filters, but as Date type
        // The API needs them as string
        start: start.toISOString(),
        end: end.toISOString(),
        interval,
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

export const dispatchFetchDomainAnalytics = dispatch(
  actions.fetchDomainAnalytics,
);
export const dispatchOverwriteAnalyticsFilters = dispatch(
  actions.overwriteAnalyticsFilters,
);
