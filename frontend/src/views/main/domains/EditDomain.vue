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
        <v-alert
          :value="success"
          transition="fade-transition"
          type="success"
          icon="check_circle"
        >
          Changes saved successfully
        </v-alert>
        <template>
          <v-form
            v-model="valid"
            ref="form"
            lazy-validation
            @submit="submit"
            @submit.prevent=""
          >
            <v-text-field
              label="Domain name"
              v-model="domainName"
              required
              :rules="domainNameRules"
              append-icon="web"
            ></v-text-field>
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
import { DomainsApi } from '@/generated';

@Component
export default class EditDomain extends Vue {
  public valid = false;
  public domainName = '';
  public error = false;
  public success = false;

  public domainNameRules = [(name: string): boolean => isValidDomain(name)];

  created(): void {
    this.domainName = this.$router.currentRoute.params.domainName;
  }

  data(): Record<string, boolean | string> {
    return {
      isCreate: this.$router.currentRoute.name === 'create-domain',
    };
  }

  public async submit(): Promise<void> {
    this.error = false;
    this.success = false;
    if (await this.$validator.validateAll()) {
      const domainsApi = this.$store.getters.domainsApi as DomainsApi;
      try {
        const response = await domainsApi.createDomain({
          domain_name: this.domainName,
        });
        const data = response.data;
        this.$router.push(`/domains/${data.domain_name}`);
        this.success = true;
      } catch (e) {
        this.error = true;
      }
    }
  }

  public cancel() {
    this.$router.back();
  }
}
</script>
