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
    <ChoroplethMap :mapData="mapData"></ChoroplethMap>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { AnalyticsApi, AnalyticsData, Domain, DomainsApi } from '@/generated';
import ChoroplethMap from '@/components/ChoroplethMap.vue';

@Component({
  components: {
    ChoroplethMap,
  },
})
export default class ViewAnalytics extends Vue {
  public domainInfo: Domain | null = null;
  public analyticsData: AnalyticsData | null = null;
  public domainError = '';

  get mapData() {
    return this.analyticsData?.countries;
  }

  public async mounted(): Promise<void> {
    const domainsApi: DomainsApi = this.$store.getters.domainsApi;
    const analyticsApi: AnalyticsApi = this.$store.getters.analyticsApi;
    try {
      const domainInfoResponse = await domainsApi.readDomainByName(
        this.domainName,
      );
      this.domainInfo = domainInfoResponse.data;
    } catch (error) {
      this.domainError = 'Domain not found';
    }

    try {
      const response = await analyticsApi.getAnalytics(
        this.domainName,
        'countries',
        '2020-03-11T17:11:24.931589+00:00',
      );
      this.analyticsData = response.data;
    } catch (error) {
      this.domainError = 'Domain not found';
    }
  }

  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }
}
</script>
