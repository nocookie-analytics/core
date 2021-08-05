import { AggregateStat } from '@/generated';

export interface DeclarativeAnalyticsBlock {
  data: AggregateStat[];
  title: string;
  urlParamName?: string;
  urlExclude?: Array<string>;
  noIcon?: boolean;
  transformValue?: CallableFunction; // Function to map values (eg: capitalise)
}
