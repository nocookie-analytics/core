import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { RootState } from '../state';

export const getters = {
  adminUsers: (state: AdminState) => state.users,
  adminOneUser: (state: AdminState) => (userId: number) => {
    const filteredUsers = state.users.filter((user) => user.id === userId);
    if (filteredUsers.length > 0) {
      return { ...filteredUsers[0] };
    }
  },
};

const { read } = getStoreAccessors<AdminState, RootState>('');

export const readAdminOneUser = read(getters.adminOneUser);
export const readAdminUsers = read(getters.adminUsers);
