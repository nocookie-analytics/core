import { IUserProfile } from '@/interfaces';
import { AdminState } from './state';
import { getStoreAccessors } from 'typesafe-vuex';
import { RootState } from '../state';

export const mutations = {
  setUsers(state: AdminState, payload: IUserProfile[]) {
    state.users = payload;
  },
  setUser(state: AdminState, payload: IUserProfile) {
    const users = state.users.filter(
      (user: IUserProfile) => user.id !== payload.id,
    );
    users.push(payload);
    state.users = users;
  },
};

const { commit } = getStoreAccessors<AdminState, RootState>('');

export const commitSetUser = commit(mutations.setUser);
export const commitSetUsers = commit(mutations.setUsers);
