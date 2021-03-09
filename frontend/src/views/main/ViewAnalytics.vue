<template>
  <div>
    <v-app-bar dark color="primary"></v-app-bar>
    <v-container fluid>
      <v-card class="ma-3 pa-3">
        <v-card-title primary-title>
          <div class="headline primary--text">View Analytics</div>
        </v-card-title>
        <v-card-text>
          <div class="headline font-weight-light ma-5">
            {{ domainName }}
            <span v-if="domainError"
              >- {{ domainError }} (You might need to
              <a href="/login">log-in</a>)</span
            >
          </div>
        </v-card-text>
      </v-card>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { Domain, DomainsApi } from '@/generated';

@Component
export default class ViewAnalytics extends Vue {
  public domainInfo: Domain | null = null;
  public domainError = '';

  public async mounted(): Promise<void> {
    const api: DomainsApi = this.$store.getters.domainsApi;
    try {
      const response = await api.readDomainByName(this.domainName);
      this.domainInfo = response.data;
    } catch (error) {
      this.domainError = 'Domain not found';
    }
  }

  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }
}
</script>
