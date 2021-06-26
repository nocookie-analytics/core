<template>
  <div ref="wrapper">
    <UplotVue :data="chartData" :options="options" />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
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

  width: number = window.innerWidth;

  get options(): uPlot.Options {
    return {
      id: 'chart1',
      class: 'page-views-chart',
      width: this.width,
      height: 400,
      axes: [{}, { space: 50 }],
      legend: {
        show: true,
      },
      hooks: {
        setSelect: [
          (u: uPlot) => {
            let min = u.posToVal(u.select.left, 'x');
            let max = u.posToVal(u.select.left + u.select.width, 'x');
            const start = new Date(min * 1000);
            const end = new Date(max * 1000);
            this.$router.replace({
              query: {
                ...this.$route.query,
                start: start.toISOString(),
                end: end.toISOString(),
              },
            });
          },
        ],
      },
      series: [
        {
          value: (self, rawValue) => new Date(rawValue * 1000).toDateString(),
          label: 'Date',
        },
        {
          points: {
            size: 10,
          },

          spanGaps: false,

          // in-legend display
          label: 'Page views',

          // series style
          stroke: '#e52c3c',
          width: 2,
          fill: '#fa506c',
        },
        {
          points: {
            size: 10,
          },
          show: true,

          spanGaps: false,

          // in-legend display
          label: 'Visitors',

          // series style
          stroke: '#f7b1ab',
          width: 2,
          fill: '#f8c4d8',
        },
      ],
      focus: {
        alpha: 0.6,
      },
      cursor: {
        focus: {
          prox: 5,
        },
        drag: {
          x: true,
          y: true,
        },
      },
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

  created(): void {
    window.addEventListener('resize', this.resizeChart);
  }

  mounted(): void {
    this.width = (this.$refs.wrapper as Element).clientWidth;
  }

  destroyed(): void {
    window.removeEventListener('resize', this.resizeChart);
  }

  resizeChart(): void {
    this.width = (this.$refs.wrapper as Element).clientWidth;
  }
}
</script>
