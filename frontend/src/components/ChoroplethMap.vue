<template>
  <div id="choropleth-map">
    <l-map
      :center="[20, 0]"
      :zoom="2"
      style="height: 600px"
      :options="mapOptions"
    >
      <l-choropleth-layer
        :data="countryData"
        titleKey="value"
        idKey="value"
        :value="value"
        geojsonIdKey="iso_a2"
        :geojson="geojson"
        :colorScale="colorScale"
      >
        <template slot-scope="props">
          <l-info-control
            :item="props.currentItem"
            :unit="props.unit"
            title=""
          />
        </template>
      </l-choropleth-layer>
    </l-map>
  </div>
</template>

<script lang="ts">
import { InfoControl, ReferenceChart, ChoroplethLayer } from 'vue-choropleth';
import geojson from './data/world.geo.json';
import { Component, Prop, Vue } from 'vue-property-decorator';
import { LMap } from 'vue2-leaflet';
import { AggregateStat } from '@/generated';

@Component({
  components: {
    LMap,
    'l-info-control': InfoControl,
    'l-reference-chart': ReferenceChart,
    'l-choropleth-layer': ChoroplethLayer,
  },
})
export default class ChoroplethMap extends Vue {
  @Prop(Array) public mapData!: Array<AggregateStat>;

  get countryData(): Array<AggregateStat> {
    return this.mapData || [];
  }

  data(): Record<string, unknown> {
    return {
      geojson,
      colorScale: ['e7d090', 'e9ae7b', 'de7062'],
      value: {
        key: 'total_visits',
        metric: 'visit(s)',
      },
      mapOptions: {
        attributionControl: false,
      },
      currentStrokeColor: '3d3213',
    };
  }
}
</script>
<style src="leaflet/dist/leaflet.css"></style>
<style>
#choropleth-map {
  background-color: #eee;
}
</style>
