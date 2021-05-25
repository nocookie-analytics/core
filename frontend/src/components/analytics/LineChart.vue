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

  mounted(): void {
    this.renderChart(this.chartData, this.options);
  }
}
</script>
