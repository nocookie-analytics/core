import { dispatchFetchDomainAnalytics } from '@/store/analytics/actions';
import { createLocalVue } from '@vue/test-utils';
import Vuex, { Store } from 'vuex';
import sinon from 'sinon';
import { storeOptions } from '@/store';
import { commitSetActiveDomain } from '@/store/analytics/mutations';
import { RootState } from '@/store/state';
import { AnalyticsApi } from '@/generated';
import { AxiosResponse } from 'axios';
import { expect } from 'chai';
import { cloneDeep } from 'lodash';

const axiosResponse: AxiosResponse = {
  data: {
    start: '2020-03-11T17:11:24.931589+00:00',
    end: '2021-03-20T15:14:33.135494+00:00',
  },
  status: 200,
  statusText: 'OK',
  config: {},
  headers: {},
};

describe('actions', () => {
  let store: Store<RootState>;

  beforeEach(() => {
    const localVue = createLocalVue();
    localVue.use(Vuex);
    store = new Vuex.Store<RootState>(cloneDeep(storeOptions));
    expect(store.state.analytics.analyticsError).to.equal(null);
    expect(store.state.analytics.currentDomain).to.equal(null);
    expect(store.state.analytics.analyticsData).to.equal(null);
    commitSetActiveDomain(store, 'domain.com');
  });

  afterEach(function() {
    sinon.restore();
  });

  it('fetch domain analytics - successful', async () => {
    store.state.analytics.analyticsError = 'some error';
    sinon.stub(AnalyticsApi.prototype, 'getAnalytics').returns(
      Promise.resolve({
        ...axiosResponse,
      }),
    );
    await dispatchFetchDomainAnalytics(store);
    expect(store.state.analytics.analyticsError).to.equal(null);
    expect(store.state.analytics.analyticsData).to.have.keys(['start', 'end']);
  });

  it('fetch domain analytics - error', async () => {
    sinon.stub(AnalyticsApi.prototype, 'getAnalytics').returns(
      Promise.reject({
        ...axiosResponse,
        status: 404,
      }),
    );
    await dispatchFetchDomainAnalytics(store);
    expect(store.state.analytics.analyticsError).to.not.equal(null);
    expect(store.state.analytics.analyticsData).to.equal(null);
  });
});
