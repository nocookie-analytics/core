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
import { commitSetActiveDomain } from '@/store/analytics/mutations';

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
    commitSetActiveDomain(
      this.$store,
      this.$router.currentRoute.params.domainName,
    );
  }

  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }
}
</script>
