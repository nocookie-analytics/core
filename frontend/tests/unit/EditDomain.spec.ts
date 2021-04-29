import Vue from 'vue';
import { expect } from 'chai';
import Vuex from 'vuex';
import { createLocalVue, shallowMount } from '@vue/test-utils';
import EditDomain from '@/views/main/domains/EditDomain.vue';
import Vuetify from 'vuetify';
import sinon from 'sinon';

const domainResponse = {
  data: {
    domain_name: 'example.com',
    public: true,
    id: 1,
    owner_id: 1,
  },
};

const $store = {
  getters: {
    domainsApi: {
      readDomainByName: () => domainResponse,
    },
  },
};

describe('EditDomain.vue', () => {
  let localVue;
  let vuetify;

  beforeEach(() => {
    localVue = createLocalVue();
    vuetify = new Vuetify();
    localVue.use(Vuex);
  });

  afterEach(function() {
    sinon.restore();
  });

  it('renders "Add new domain"', async () => {
    const $route = {
      name: 'create-domain',
    };

    const wrapper = shallowMount(EditDomain, {
      localVue,
      vuetify,
      stubs: ['router-link', 'router-view'],
      mocks: { $route },
    });
    await Vue.nextTick();

    expect(wrapper.html()).to.include('Make my website analytics page public');
  });

  it('renders edit domain', async () => {
    const $route = {
      name: 'edit-domain',
      params: {
        domainName: 'example.com',
      },
    };

    const wrapper = shallowMount(EditDomain, {
      localVue,
      vuetify,
      stubs: ['router-link', 'router-view'],
      mocks: { $route, $store },
    });
    await Vue.nextTick();

    expect(wrapper.html()).to.include('Make my website analytics page public');
  });
});
