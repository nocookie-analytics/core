<template>
  <v-chart class="chart" :option="options" />
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { PageViewsPerDayStat } from '@/generated';

import VChart, { THEME_KEY } from 'vue-echarts';
import { CanvasRenderer } from 'echarts/renderers';
import { use } from 'echarts/core';
import { LineChart as EChartsLineChart } from 'echarts/lib/chart/line';
import {
  TooltipComponent,
  GridComponent,
  TitleComponent,
} from 'echarts/components';
import { EChartsOption } from 'echarts/types/dist/shared';

use([
  CanvasRenderer,
  EChartsLineChart,
  TooltipComponent,
  TitleComponent,
  GridComponent,
]);

import 'echarts/theme/sakura';

@Component({
  components: {
    VChart,
  },
  provide: { [THEME_KEY]: 'sakura' },
})
export default class LineChart extends Vue {
  @Prop() blockData!: Array<PageViewsPerDayStat>;

  get options(): EChartsOption {
    const dates: Array<string> = [];
    const totalVisits: Array<number> = [];
    const visitors: Array<number> = [];

    this.blockData.forEach((row) => {
      dates.push(row.date);
      totalVisits.push(row.total_visits);
      visitors.push(row.visitors);
    });

    return {
      title: {
        text: 'Visitors',
      },
      grid: {
        left: 50,
        right: 0,
      },
      series: [
        { name: 'Page views', type: 'line', areaStyle: {}, data: totalVisits },
        { name: 'Visitors', type: 'line', areaStyle: {}, data: visitors },
      ],
      xAxis: [
        {
          data: dates,
          axisPointer: {
            snap: true,
          },
        },
      ],
      yAxis: [
        {
          type: 'value',
          axisPointer: {
            snap: true,
          },
          splitLine: {
            show: false,
          },
        },
      ],
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          label: {
            backgroundColor: '#6a7985',
            precision: 0,
          },
          snap: true,
        },
      },
    };
  }

  /*
  get chartData(): ChartData {
    const labels: Array<string> = [];
    const totalVisits: Array<number> = [];
    const visitors: Array<number> = [];

    this.blockData.forEach((row) => {
      labels.push(row.date);
      totalVisits.push(row.total_visits);
      visitors.push(row.visitors);
    });
    return {
      labels,
      datasets: [
        {
          backgroundColor: '#4d698c',
          label: 'Visitors',
          fill: true,
          data: visitors,
        },
        {
          backgroundColor: '#94d2ee',
          label: 'Total visits',
          fill: true,
          data: totalVisits,
        },
      ],
    };
  }

  get options(): ChartOptions {
    const options: ChartOptions = {
      maintainAspectRatio: false,
      legend: {
        display: false,
      },
      responsive: true,
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              precision: 0,
            },
            gridLines: {
              display: false,
            },
            minInterval: 1,
          },
        ],
        xAxes: [
          {
            gridLines: {
              display: false,
            },
            type: 'time'
          },
        ],
      },
    };
    return options;
  }

  mounted(): void {
    this.renderChart(this.chartData, this.options);
  }
  */
}
</script>

<style scoped>
.chart {
  height: 400px;
}
</style>
