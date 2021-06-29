import { AggregateStat } from '@/generated';

export enum DeclarativeBlockType {
  AggregateStat,
}

export interface DeclarativeAnalyticsBlock {
  data: AggregateStat[];
  type: DeclarativeBlockType;
  title: string;
  urlParamName?: string;
  urlExclude?: Array<string>;
  cols: number;
}
