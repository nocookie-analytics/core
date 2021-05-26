<template>
  <v-simple-table>
    <template v-slot:default>
      <thead>
        <tr>
          <th class="text-left">Name</th>
          <th class="text-left">Visitors</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data" :key="item.value">
          <td>
            <slot name="itemName" v-bind:item="item">{{ item.value }}</slot>
          </td>
          <td>{{ item.visitors }}</td>
        </tr>
      </tbody>
    </template>
  </v-simple-table>
</template>

<script lang="ts">
import { AggregateStat } from '@/generated';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class Tabular extends Vue {
  @Prop() public data!: Array<AggregateStat>;
}
</script>
