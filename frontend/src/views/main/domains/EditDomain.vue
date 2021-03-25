<template>
  <v-container fluid>
    <v-card class="ma-3 pa-3">
      <v-card-title primary-title>
        <div class="headline primary--text" v-if="isCreate">Add new domain</div>
        <div class="headline primary--text" v-else>Edit domain</div>
      </v-card-title>
      <v-card-text>
        <template>
          <v-form v-model="valid" ref="form" lazy-validation>
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
        <v-btn @click="submit" :disabled="!valid" color="primary"> Save </v-btn>
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
  public error = '';

  domainNameRules = [(name: string): boolean => isValidDomain(name)];

  created(): void {
    this.domainName = this.$router.currentRoute.params.domainName;
  }

  data(): Record<string, boolean | string> {
    return {
      isCreate: this.$router.currentRoute.name === 'create-domain',
    };
  }

  public async submit(): Promise<void> {
    if (await this.$validator.validateAll()) {
      const domainsApi = this.$store.getters.domainsApi as DomainsApi;
      try {
        this.error = '';
        const response = await domainsApi.createDomain({
          domain_name: this.domainName,
        });
        const data = response.data;
        this.$router.push(`/domains/${data.domain_name}`);
      } catch (e) {
        this.error = 'Something went wrong, try again later';
      }
    }
  }

  public cancel() {
    this.$router.back();
  }
}
</script>
