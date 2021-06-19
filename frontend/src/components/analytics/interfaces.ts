import { AggregateStat } from '@/generated';

export enum DeclarativeBlockType {
  AggregateStat,
  ArrayAvgMetricPerDayStat,
  PageViewStat,
  ArrayPageViewsPerDayStat,
}

export interface DeclarativeAnalyticsBlock {
  data: AggregateStat[];
  type: DeclarativeBlockType;
  title: string;
  urlParamName?: string;
  urlExclude?: Array<string>;
  cols: number;
}
