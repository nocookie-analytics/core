export interface IUserProfile {
  email: string;
  is_active: boolean;
  is_superuser: boolean;
  full_name: string;
  id: number;
}

export interface IUserProfileUpdate {
  email?: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface IUserProfileCreate {
  email: string;
  full_name?: string;
  password?: string;
  is_active?: boolean;
  is_superuser?: boolean;
}

export interface ISummaryBlock {
  title: string;
  value: string;
  change: number | undefined;
  changeSign: number; // Things like bounce rate need a "reversed" logic for deciding if it's a good thing or not
  class: string;
  icon: string;
}
