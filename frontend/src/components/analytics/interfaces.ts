import { AggregateStat } from '@/generated';

export interface DeclarativeAnalyticsBlock {
  data: AggregateStat[];
  title: string;
  urlParamName?: string;
  urlExclude?: Array<string>;
  cols: number;
}
