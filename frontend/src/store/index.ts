import Vue from 'vue';
import Vuex, { StoreOptions } from 'vuex';

import { mainModule } from './main';
import { RootState } from './state';
import { adminModule } from './admin';
import { analyticsModule } from './analytics';
import {
  AnalyticsApi,
  Configuration,
  ConfigurationParameters,
  DomainsApi,
  UsersApi,
} from '@/generated';
import { apiUrl } from '@/env';

Vue.use(Vuex);

export const storeOptions: StoreOptions<RootState> = {
  modules: {
    main: mainModule,
    admin: adminModule,
    analytics: analyticsModule,
  },
  getters: {
    apiConfig: (state: RootState): ConfigurationParameters => {
      const apiConfig: ConfigurationParameters = {
        accessToken: state.main.token,
        basePath: apiUrl,
      };
      return new Configuration(apiConfig);
    },
    usersApi: (_, getters): UsersApi => {
      return new UsersApi(getters.apiConfig);
    },
    domainsApi: (_, getters): DomainsApi => {
      return new DomainsApi(getters.apiConfig);
    },
    analyticsApi: (_, getters): AnalyticsApi => {
      return new AnalyticsApi(getters.apiConfig);
    },
  },
};

export const store = new Vuex.Store<RootState>(storeOptions);

export default store;
