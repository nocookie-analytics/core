<template>
  <div id="map">
    <l-map
      :center="[-23.752961, -57.854357]"
      :zoom="6"
      style="height: 500px"
      :options="mapOptions"
    >
      <l-choropleth-layer
        :data="pyDepartmentsData"
        titleKey="department_name"
        idKey="department_id"
        :value="value"
        :extraValues="extraValues"
        geojsonIdKey="dpto"
        :geojson="geojson"
        :colorScale="colorScale"
      >
        <template slot-scope="props">
          <l-info-control
            :item="props.currentItem"
            :unit="props.unit"
            title="Department"
            placeholder="Hover over a department"
          />
          <l-reference-chart
            title="Girls school enrolment"
            :colorScale="colorScale"
            :min="props.min"
            :max="props.max"
            position="topright"
          />
        </template>
      </l-choropleth-layer>
    </l-map>
  </div>
</template>

<script>
import { InfoControl, ReferenceChart, ChoroplethLayer } from 'vue-choropleth';
import { geojson } from './data/py-departments-geojson';
import { Component, Prop, Vue } from 'vue-property-decorator';
import paraguayGeojson from './data/paraguay.json';
import { pyDepartmentsData } from './data/py-departments-data';
import { LMap } from 'vue2-leaflet';

@Component({
  components: {
    LMap,
    'l-info-control': InfoControl,
    'l-reference-chart': ReferenceChart,
    'l-choropleth-layer': ChoroplethLayer,
  },
})
export default class ChoroplethMap extends Vue {
  data() {
    return {
      pyDepartmentsData,
      geojson,
      colorScale: ['e7d090', 'e9ae7b', 'de7062'],
      value: {
        key: 'amount_w',
        metric: '% girls',
      },
      extraValues: [
        {
          key: 'amount_m',
          metric: '% boys',
        },
      ],
      mapOptions: {
        attributionControl: false,
      },
      currentStrokeColor: '3d3213',
    };
  }
}
</script>
<style src='leaflet/dist/leaflet.css'></style>
<style>
body {
  background-color: #e7d090;
  margin-left: 100px;
  margin-right: 100px;
}
#map {
  background-color: #eee;
}
</style>
