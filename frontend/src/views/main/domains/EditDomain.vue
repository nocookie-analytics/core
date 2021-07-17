<template>
  <v-container>
    <router-view :key="$route.fullPath"></router-view>
    <v-card class="ma-3 pa-3" outlined>
      <v-card-title primary-title>
        <div class="headline primary--text" v-if="isCreate">Add new domain</div>
        <div class="headline primary--text" v-else>Edit domain</div>
      </v-card-title>
      <v-card-text>
        <v-alert
          :value="error"
          transition="fade-transition"
          type="error"
          :icon="$vuetify.icons.values.alertCircle"
        >
          We are really sorry but something went wrong, please try again later
        </v-alert>
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
            :append-icon="$vuetify.icons.values.web"
          ></v-text-field>

          <v-checkbox
            label="Make my website analytics page public and viewable by anyone"
            v-model="public_"
          ></v-checkbox>
        </v-form>
      </v-card-text>
      <v-card-actions v-if="!error">
        <v-spacer></v-spacer>
        <v-btn @click="cancel">Cancel</v-btn>
        <v-btn type="submit" @click="submit" :disabled="!valid" color="primary">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
    <v-expansion-panels class="pa-3">
      <v-expansion-panel>
        <v-expansion-panel-header>
          Add the script tag to your website
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <code v-pre>
            &lt;script async defer
            src="https://nocookieanalytics.com/latest.js"&gt;&lt;/script&gt;
          </code>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import isValidDomain from 'is-valid-domain';
import { DomainsApi } from '@/generated';
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

  private get isCreate(): boolean {
    return this.$route.name === 'create-domain';
  }

  public async mounted(): Promise<void> {
    if (!this.isCreate) {
      const domainsApi = this.$store.getters.domainsApi as DomainsApi;
      const response = await domainsApi.readDomainByName({
        name: this.$route.params.domainName,
      });
      const data = response.data;
      this.domainName = data.domain_name;
      this.public_ = data.public;
    }
    this.finishedLoading = true;
  }

  public async submit(): Promise<void> {
    this.error = false;
    if (await this.$validator.validateAll()) {
      if (this.isCreate) {
        this.createDomain();
      } else {
        this.updateDomain();
      }
      if (this.error === false) {
        this.$router.push(`/domains/`);
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
      await domainsApi.createDomain({ domainCreate: this.domainData });
    } catch (e) {
      this.error = true;
    }
  }

  private async updateDomain(): Promise<void> {
    const domainsApi = this.$store.getters.domainsApi as DomainsApi;
    const domainName = this.$route.params.domainName; // this.domainName points to the current form value, so we have to get the current domain name from the route
    try {
      await domainsApi.updateDomainByName({
        name: domainName,
        domainUpdate: this.domainData,
      });
    } catch (e) {
      console.debug(e);
      this.error = true;
    }
  }

  public cancel() {
    this.$router.back();
  }
}
</script>
