<script lang="ts">
import { Component, Mixins, Prop } from 'vue-property-decorator';
import { Line } from 'vue-chartjs';
import { ChartData, ChartOptions } from 'chart.js';
import { PageViewsPerDayStat } from '@/generated';

@Component({
  extends: Line,
})
export default class LineChart extends Mixins(Line) {
  @Prop() blockData!: Array<PageViewsPerDayStat>;
  @Prop() startDate!: Date;
  @Prop() endDate!: Date;

  get chartData(): ChartData {
    const labels: Array<string> = [];
    const data: Array<number> = [];

    this.blockData.forEach((row) => {
      labels.push(row.date);
      data.push(row.total_visits);
    });
    return {
      labels,
      datasets: [
        {
          backgroundColor: 'red',
          label: 'Page views',
          fill: true,
          data,
        },
      ],
    };
  }

  get options() {
    const options = {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              stepSize: 1,
            },
            gridLines: {
              display: false,
            },
          },
        ],
        xAxes: [
          {
            gridLines: {
              display: true,
            },
          },
        ],
      },
    };
    return options;
  }

  mounted() {
    console.log(this.options);
    this.renderChart(this.chartData, this.options);
  }
}
</script>
