import Vue from 'vue';
import { expect } from 'chai';
import Vuex from 'vuex';
import { createLocalVue, mount } from '@vue/test-utils';
import EditDomain from '@/views/main/domains/EditDomain.vue';
import Vuetify from 'vuetify';
import sinon from 'sinon';
import { mutations } from '@/store/main/mutations';

const domainResponse = {
  data: {
    domain_name: 'example.com',
    public: true,
    id: 1,
    owner_id: 1,
  },
};

const mockStore = () => {
  return {
    commit: sinon.spy(),
    getters: {
      domainsApi: {
        readDomainByName: sinon.stub().resolves(domainResponse),
        updateDomainByName: sinon.stub().resolves(domainResponse),
        createDomain: sinon.stub().resolves(domainResponse),
      },
    },
  };
};
const $validator = {
  validateAll: () => true,
};

describe('EditDomain.vue', () => {
  let localVue;
  let vuetify;

  const testFormAndSave = async (wrapper, $store, $router, apiStub) => {
    // Simulate filling up the form and save it
    // TODO: Perhaps move this to an e2e test or something
    const [domainNameInput, publicCheckbox] = wrapper.findAll('input').wrappers;
    domainNameInput.setValue('hello.com');
    const [cancelButton, saveButton] = wrapper.findAll('button').wrappers;
    await Vue.nextTick();
    await Vue.nextTick();
    expect($router.length).to.equal(0);
    expect(saveButton.text()).to.equal('Save');
    saveButton.trigger('click');
    await Vue.nextTick();
    expect(apiStub.calledOnce).to.be.true;
    expect($router.length).to.equal(1);
    expect($router[0]).to.equal('/domains/');
  };

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
    const $store = mockStore();
    const $router = [];
    const wrapper = mount(EditDomain, {
      localVue,
      vuetify,
      stubs: ['router-link', 'router-view'],
      mocks: { $route, $store, $validator, $router },
    });
    await Vue.nextTick();
    expect($store.getters.domainsApi.readDomainByName.notCalled).to.be.true;

    expect(wrapper.html()).to.include('Make my website analytics page public');

    await testFormAndSave(
      wrapper,
      $store,
      $router,
      $store.getters.domainsApi.createDomain,
    );
  });

  it('renders edit domain', async () => {
    const $route = {
      name: 'edit-domain',
      params: {
        domainName: 'example.com',
      },
    };

    const $store = mockStore();
    const $router = [];
    const wrapper = mount(EditDomain, {
      localVue,
      vuetify,
      stubs: ['router-link', 'router-view'],
      mocks: { $route, $store, $validator, $router },
    });
    // Need to wait two ticks, not sure why
    await Vue.nextTick();
    await Vue.nextTick();
    expect($store.getters.domainsApi.readDomainByName.calledOnce).to.be.true;

    expect(wrapper.html()).to.include('Make my website analytics page public');

    await testFormAndSave(
      wrapper,
      $store,
      $router,
      $store.getters.domainsApi.updateDomainByName,
    );
  });
});
