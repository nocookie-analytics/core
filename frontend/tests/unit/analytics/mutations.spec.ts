import { expect } from 'chai';
import { mutations } from '@/store/analytics/mutations';
import { defaultState } from '@/store/analytics';

const { setActiveDomain, setDomainData, setAnalyticsError } = mutations;

describe('mutations', () => {
  it('sets active domain and unsets error', () => {
    const state = { ...defaultState, error: 'error' };
    setActiveDomain(state, 'newdomain.com');
    expect(state.currentDomain).to.equal('newdomain.com');
    expect(state.analyticsError).to.equal(null);
  });

  it('sets domain data', () => {
    const state = { ...defaultState };
    const domainData = {
      start: new Date().toISOString(),
      end: new Date().toISOString(),
    };
    setDomainData(state, domainData);
    expect(state.analyticsData).to.equal(domainData);
    expect(state.analyticsError).to.equal(null);
  });

  it('sets domain error', () => {
    const state = { ...defaultState };
    setAnalyticsError(state, 'something is wrong');
    expect(state.analyticsError).to.equal('something is wrong');
  });
});
