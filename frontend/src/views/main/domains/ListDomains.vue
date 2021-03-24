<template>
  <div>
    <v-container fluid>
      <v-data-table
        loading="isLoading"
        :loading-text="loadingText"
        :headers="headers"
        :items="domainsList"
        :items-per-page="50"
        class="elevation-1"
        :server-items-length="domainsList.length"
      >
        <template #item.actions="{ item }">
          <v-btn title="Edit" icon :to="'/domains/' + item.domain_name">
            <span class="group pa-2">
              <v-icon medium>edit</v-icon>
            </span>
          </v-btn>
        </template>
      </v-data-table>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Domain, DomainsApi } from '@/generated';
import { Component, Vue } from 'vue-property-decorator';
import { DataTableHeader } from 'vuetify';

@Component
export default class ListDomains extends Vue {
  fetchDomainsError: string | null = null;
  domainsList: Array<Domain> = [];
  isLoading = true;

  async mounted(): Promise<void> {
    await this.fetchDomains();
    this.isLoading = false;
  }

  async fetchDomains(): Promise<void> {
    const domainsApi = this.$store.getters.domainsApi as DomainsApi;
    try {
      const response = await domainsApi.readDomains(0, 50);
      this.domainsList = response.data;
    } catch (e) {
      this.fetchDomainsError =
        'Could not fetch list of domains, something went wrong. Please try again';
    }
  }

  get headers(): Array<DataTableHeader> {
    return [
      {
        text: 'Domain Name',
        align: 'start',
        sortable: false,
        value: 'domain_name',
      },
      { text: 'Actions', align: 'center', value: 'actions' },
    ];
  }

  get loadingText(): string {
    if (this.isLoading) {
      return 'Loading, please wait';
    } else if (this.domainsList.length === 0) {
      return 'Nothing found';
    }
    return '';
  }
}
</script>
