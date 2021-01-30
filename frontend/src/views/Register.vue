<template>
  <v-content>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card class="elevation-12">
            <v-toolbar dark color="primary">
              <v-toolbar-title>Register</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form @keyup.enter="register">
                <v-text-field
                  @keyup.enter="register"
                  v-model="email"
                  prepend-icon="person"
                  name="register"
                  label="E-mail"
                  type="text"
                ></v-text-field>
                <v-text-field
                  @keyup.enter="register"
                  v-model="password"
                  prepend-icon="lock"
                  name="password"
                  label="Password"
                  id="password"
                  type="password"
                ></v-text-field>
              </v-form>
              <div v-if="registrationError">
                <v-alert
                  :value="hasRegistrationError"
                  transition="fade-transition"
                  type="error"
                >
                  {{ registrationError }}
                </v-alert>
              </div>
              <v-flex class="caption text-xs-right"
                ><router-link to="/login">Login</router-link></v-flex
              >
              <v-flex class="caption text-xs-right"
                ><router-link to="/recover-password"
                  >Forgot your password?</router-link
                ></v-flex
              >
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="register">Register</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-content>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { api } from '@/api';
import { appName } from '@/env';
import { readRegistrationError } from '@/store/main/getters';
import { IUserProfileCreate } from '@/interfaces';
import { dispatchRegister } from '@/store/main/actions';

@Component
export default class Register extends Vue {
  public email: string = '';
  public password: string = '';
  public appName = appName;

  public get hasRegistrationError() {
    return Boolean(this.registrationError);
  }

  public get registrationError() {
    return readRegistrationError(this.$store);
  }

  public register() {
    const payload: IUserProfileCreate = {
      email: this.email,
      password: this.password,
    };
    dispatchRegister(this.$store, {
      email: this.email,
      password: this.password,
    });
  }
}
</script>

<style></style>
