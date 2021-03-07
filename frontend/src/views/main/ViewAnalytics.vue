<template>
  <div>
    <v-app-bar dark color="primary"></v-app-bar>
    <v-container fluid>
      <v-card class="ma-3 pa-3">
        <v-card-title primary-title>
          <div class="headline primary--text">View Analytics</div>
        </v-card-title>
        <v-card-text>
          <div class="headline font-weight-light ma-5">{{ domainName }}</div>
        </v-card-text>
        <ChoroplethMap></ChoroplethMap>
      </v-card>
    </v-container>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ChoroplethMap from '@/components/ChoroplethMap.vue';

@Component
export default class ViewAnalytics extends Vue {
  get domainName(): string {
    return this.$router.currentRoute.params.domainName;
  }
}
</script>
