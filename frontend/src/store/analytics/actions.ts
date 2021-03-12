import { AnalyticsData } from '@/generated';
import { getStoreAccessors } from 'typesafe-vuex';
import { ActionContext } from 'vuex';
import { State } from '../state';
import { AnalyticsState } from './state';

type AnalyticsContext = ActionContext<AnalyticsState, State>;

export const actions = {
  async getDomainAnalytics(
    context: AnalyticsContext,
    domainName: string,
  ): Promise<void> {
    console.log(context.rootState);
    return new Promise(() => null);
    //return await context.rootState.analyticsApi.getAnalytics(
    //domainName,
    //'countries',
    //'2020-03-11T17:11:24.931589+00:00',
    //);
  },
};

const { dispatch } = getStoreAccessors<AnalyticsState, State>('');

export const dispatchGetDomainAnalytics = dispatch(actions.getDomainAnalytics);
