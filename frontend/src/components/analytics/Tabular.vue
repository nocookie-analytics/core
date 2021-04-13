<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Name</th>
          <th class="text-left">Visits</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.value">
          <td>{{ item.value }}</td>
          <td>{{ item.total_visits }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Tabular extends Vue {
  @Prop() public data;
}
</script>
