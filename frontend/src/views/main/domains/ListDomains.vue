<template>
  <div>
    <v-container>
      <v-toolbar light flat outlined>
        <v-toolbar-title> Domains </v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn color="primary" to="/domains/create">Add new domain</v-btn>
      </v-toolbar>
      <v-data-table
        loading="isLoading"
        :loading-text="loadingText"
        :headers="headers"
        :items="domainsList"
        :items-per-page="50"
        class="elevation-1"
        :server-items-length="domainsList.length"
        hide-default-footer
      >
        <template #[`item.domain_name`]="{ item }">
          <router-link :to="'/' + item.domain_name">
            <span class="text-subtitle-1 dark-link">{{
              item.domain_name
            }}</span>
          </router-link>
        </template>
        <template #[`item.actions`]="{ item }">
          <v-btn title="View analytics" icon :to="'/' + item.domain_name">
            <v-icon medium> {{ mdiChartAreaspline }}</v-icon>
          </v-btn>
          <v-btn title="Edit" icon :to="'/domains/' + item.domain_name">
            <v-icon medium> {{ $vuetify.icons.values.pencil }}</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Domain, DomainsApi } from '@/generated';
import { mdiChartAreaspline } from '@mdi/js';
import { Component, Vue } from 'vue-property-decorator';
import { DataTableHeader } from 'vuetify';

@Component
export default class ListDomains extends Vue {
  fetchDomainsError: string | null = null;
  domainsList: Array<Domain> = [];
  isLoading = true;
  mdiChartAreaspline = mdiChartAreaspline;

  async mounted(): Promise<void> {
    await this.fetchDomains();
    this.isLoading = false;
  }

  async fetchDomains(): Promise<void> {
    const domainsApi = this.$store.getters.domainsApi as DomainsApi;
    try {
      const response = await domainsApi.readDomains({ skip: 0, limit: 50 });
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

  public goToAnalytics(url: string): void {
    this.$router.push(url);
  }
}
</script>

<style scoped>
.dark-link {
  color: #ad3515;
}
</style>
