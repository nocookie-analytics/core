import { AggregateStat, CustomEventStat } from '@/generated';

export interface DeclarativeAnalyticsBlock {
  data: AggregateStat[] | CustomEventStat[];
  title: string;
  urlParamName?: string;
  urlExclude?: Array<string>;
  noIcon?: boolean;
  transformValue?: CallableFunction; // Function to map values (eg: capitalise)
}
