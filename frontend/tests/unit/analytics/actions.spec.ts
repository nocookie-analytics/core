import { dispatchFetchDomainAnalytics } from '@/store/analytics/actions';
import Vuex, { Store } from 'vuex';
import sinon from 'sinon';
import { storeOptions } from '@/store';
import { commitSetActiveDomain } from '@/store/analytics/mutations';
import { RootState } from '@/store/state';
import { AnalyticsApi } from '@/generated';
import { AxiosResponse } from 'axios';
import { expect } from 'chai';

const axiosResponse: AxiosResponse = {
  data: { detail: 'Domain not found' },
  status: 404,
  statusText: 'OK',
  config: {},
  headers: {},
};

describe('actions', () => {
  let store: Store<RootState>;

  beforeEach(() => {
    store = new Vuex.Store<RootState>(storeOptions);
  });

  it('fetch domain analytics', async () => {
    sinon
      .stub(AnalyticsApi.prototype, 'getAnalytics')
      .returns(Promise.reject(axiosResponse));
    commitSetActiveDomain(store, 'doesnotexist.com');
    expect(store.state.analytics.analyticsError).to.equal(null);
    await dispatchFetchDomainAnalytics(store);
    expect(store.state.analytics.analyticsError).to.not.equal(null);
  });
});
