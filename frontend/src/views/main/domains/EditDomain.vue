<template>
  <v-container fluid>
    <router-view :key="$route.fullPath"></router-view>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text" v-if="isCreate">Add new domain</div>
        <div class="headline primary--text" v-else>Edit domain</div>
      </v-card-title>
      <v-card-text>
        <v-alert
          :value="error"
          transition="fade-transition"
          type="error"
          icon="error"
        >
          We are really sorry but something went wrong, please try again later
        </v-alert>
        <template>
          <v-form
            v-model="valid"
            ref="form"
            @submit="submit"
            @submit.prevent=""
            @keyup.enter="submit"
            v-if="finishedLoading"
          >
            <v-text-field
              label="Domain name"
              v-model="domainName"
              required
              :rules="domainNameRules"
              append-icon="web"
            ></v-text-field>

            <v-checkbox
              label="Make my website analytics page public and viewable by anyone"
              v-model="public_"
            ></v-checkbox>
          </v-form>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn type="submit" @click="submit" :disabled="!valid" color="primary">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import isValidDomain from 'is-valid-domain';
import { DomainCreate, DomainsApi, DomainUpdate } from '@/generated';
import { commitAddNotification } from '@/store/main/mutations';

@Component
export default class EditDomain extends Vue {
  public domainName = '';
  public public_ = false;
  public checkbox = false;

  public finishedLoading = false;
  public valid = false;
  public error = false;

  public domainNameRules = [(name: string): boolean => isValidDomain(name)];

  data(): Record<string, boolean | string> {
    return {
      isCreate: this.$router.currentRoute.name === 'create-domain',
    };
  }

  public async mounted() {
    const domainsApi = this.$store.getters.domainsApi as DomainsApi;
    const response = await domainsApi.readDomainByName(
      this.$router.currentRoute.params.domainName,
    );
    const data = response.data;
    this.domainName = data.domain_name;
    this.public_ = data.public;
    this.finishedLoading = true;
  }

  public async submit(): Promise<void> {
    this.error = false;
    if (await this.$validator.validateAll()) {
      if (this.$router.currentRoute.name === 'create-domain') {
        this.createDomain();
      } else {
        this.updateDomain();
      }
      if (this.error === false) {
        commitAddNotification(this.$store, {
          content: 'Changes saved successfully',
          color: 'success',
          timeout: 5000,
        });
      }
    }
  }

  private get domainData() {
    return {
      domain_name: this.domainName,
      public: this.public_,
    };
  }

  private async createDomain(): Promise<void> {
    const domainsApi = this.$store.getters.domainsApi as DomainsApi;
    try {
      await domainsApi.createDomain(this.domainData);
    } catch (e) {
      this.error = true;
    }
  }

  private async updateDomain(): Promise<void> {
    const domainsApi = this.$store.getters.domainsApi as DomainsApi;
    try {
      await domainsApi.updateDomainByName(
        this.$router.currentRoute.params.domainName,
        this.domainData,
      );
    } catch (e) {
      this.error = true;
    }
  }

  public cancel() {
    this.$router.back();
  }
}
</script>
