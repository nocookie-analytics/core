<template>
  <UplotVue :data="chartData" :options="options" />
</template>


<script lang="ts">
import { Component, Mixins, Prop, Vue } from 'vue-property-decorator';
import { PageViewsPerDayStat } from '@/generated';
import uPlot from 'uplot';
import UplotVue from 'uplot-vue';
import 'uplot/dist/uPlot.min.css';

@Component({
  components: {
    UplotVue,
  },
})
export default class LineChart extends Vue {
  @Prop() blockData!: Array<PageViewsPerDayStat>;

  width: number = window.innerWidth - 200;

  get options(): uPlot.Options {
    return {
      title: 'Visitors',
      id: 'chart1',
      class: 'page-views-chart',
      width: this.width,
      height: 600,
      series: [
        {},
        {
          // initial toggled state (optional)
          show: true,

          spanGaps: false,

          // in-legend display
          label: 'Page views',
          value: (self, rawValue) => rawValue.toFixed(2),

          // series style
          stroke: '#e52c3c',
          width: 1,
          fill: '#fa506c',
          dash: [10, 5],
        },
        {
          // initial toggled state (optional)
          show: true,

          spanGaps: false,

          // in-legend display
          label: 'Visitors',
          value: (self, rawValue) => rawValue.toFixed(2),

          // series style
          stroke: '#f7b1ab',
          width: 1,
          fill: '#f8c4d8',
          dash: [10, 5],
        },
      ],
    };
  }

  get chartData(): uPlot.AlignedData {
    const labels: Array<number> = [];
    const totalVisits: Array<number> = [];
    const visitors: Array<number> = [];

    this.blockData.forEach((row) => {
      labels.push(new Date(row.date).getTime() / 1000);
      totalVisits.push(row.total_visits);
      visitors.push(row.visitors);
    });
    const data: uPlot.AlignedData = [labels, totalVisits, visitors];
    return data;
  }

  created() {
    window.addEventListener('resize', this.resizeChart);
  }

  destroyed() {
    window.removeEventListener('resize', this.resizeChart);
  }

  resizeChart(): void {
    this.width = window.innerWidth - 200;
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
  */

  /*
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
          },
        ],
        xAxes: [
          {
            gridLines: {
              display: false,
            },
          },
        ],
      },
    };
    return options;
  }
  */
}
</script>
