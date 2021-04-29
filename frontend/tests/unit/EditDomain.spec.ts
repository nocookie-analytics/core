import Vue from 'vue';
import { expect } from 'chai';
import { createLocalVue, mount, shallowMount } from '@vue/test-utils';
import EditDomain from '@/views/main/domains/EditDomain.vue';
import Vuetify from 'vuetify';

describe('EditDomain.vue', () => {
  let localVue;
  let vuetify;

  beforeEach(() => {
    vuetify = new Vuetify();
    localVue = createLocalVue();
  });

  it('renders "Add new domain"', async () => {
    const $route = {
      fullPath: '/some-route',
      name: 'create-domain',
    };

    const wrapper = mount(EditDomain, {
      localVue,
      vuetify,
      mocks: { $route },
    });
    await Vue.nextTick();

    expect(wrapper.html()).to.include('Make my website analytics page public');
  });
});
