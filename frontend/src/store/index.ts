import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';

import { mainModule } from './main';
import { State } from './state';
import { adminModule } from './admin';
import { analyticsModule } from './analytics';
import {
  AnalyticsApi,
  Configuration,
  ConfigurationParameters,
  DomainsApi,
} from '@/generated';
import { apiUrl } from '@/env';

Vue.use(Vuex);

const storeOptions: StoreOptions<State> = {
  modules: {
    main: mainModule,
    admin: adminModule,
    analytics: analyticsModule,
  },
  getters: {
    apiConfig: (state): ConfigurationParameters => {
      const apiConfig: ConfigurationParameters = {
        accessToken: state.main.token,
        basePath: apiUrl,
      };
      return new Configuration(apiConfig);
    },
    domainsApi: (_, getters): DomainsApi => {
      return new DomainsApi(getters.apiConfig);
    },
    analyticsApi: (_, getters): AnalyticsApi => {
      return new AnalyticsApi(getters.apiConfig);
    },
  },
};

export const store = new Vuex.Store<State>(storeOptions);

export default store;
