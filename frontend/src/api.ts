import axios, { AxiosResponse } from 'axios';
import { apiUrl } from '@/env';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}

export const api = {
  async logInGetToken(
    username: string,
    password: string,
  ): Promise<AxiosResponse> {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async register(data: IUserProfileCreate): Promise<AxiosResponse> {
    return axios.post<IUserProfile>(`${apiUrl}/api/v1/users/open`, data);
  },
  async getMe(token: string): Promise<AxiosResponse> {
    return axios.get<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      authHeaders(token),
    );
  },
  async updateMe(
    token: string,
    data: IUserProfileUpdate,
  ): Promise<AxiosResponse> {
    return axios.put<IUserProfile>(
      `${apiUrl}/api/v1/users/me`,
      data,
      authHeaders(token),
    );
  },
  async getUsers(token: string): Promise<AxiosResponse> {
    return axios.get<IUserProfile[]>(
      `${apiUrl}/api/v1/users/`,
      authHeaders(token),
    );
  },
  async updateUser(
    token: string,
    userId: number,
    data: IUserProfileUpdate,
  ): Promise<AxiosResponse> {
    return axios.put(
      `${apiUrl}/api/v1/users/${userId}`,
      data,
      authHeaders(token),
    );
  },
  async createUser(
    token: string,
    data: IUserProfileCreate,
  ): Promise<AxiosResponse> {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string): Promise<AxiosResponse> {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string): Promise<AxiosResponse> {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
};
