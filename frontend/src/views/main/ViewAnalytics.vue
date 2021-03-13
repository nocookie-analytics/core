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
            <span v-if="analyticsError"
              >- {{ analyticsError }} (You might need to
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
import ChoroplethMap from '@/components/ChoroplethMap.vue';
import { dispatchUpdateActiveDomain } from '@/store/analytics/actions';
import { readAnalyticsData } from '@/store/analytics/getters';
import { AggregateStat } from '@/generated';
import { AnalyticsState } from '@/store/analytics/state';

@Component({
  components: {
    ChoroplethMap,
  },
})
export default class ViewAnalytics extends Vue {
  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }

  get analyticsError(): string | null {
    return (this.$store.state as AnalyticsState).analyticsError;
  }

  public async mounted(): Promise<void> {
    dispatchUpdateActiveDomain(
      this.$store,
      this.$router.currentRoute.params.domainName,
    );
  }

  get mapData(): Array<AggregateStat> {
    return readAnalyticsData(this.$store)?.countries || [];
  }
}
</script>
