import { IUserProfile } from '@/interfaces';

export interface AppNotification {
  content: string;
  color?: string;
  showProgress?: boolean;
  timeout?: number;
}

export interface MainState {
  token: string;
  isLoggedIn: boolean | null;
  logInError: boolean;
  registrationError: string | null;
  userProfile: IUserProfile | null;
  dashboardMiniDrawer: boolean;
  notifications: AppNotification[];
}
