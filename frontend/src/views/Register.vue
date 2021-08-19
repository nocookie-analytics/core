<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card>
            <v-toolbar color="primary" class="white--text" flat>
              <v-toolbar-title>{{ appName }} - Register</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
            <v-card-text>
              <v-form @keyup.enter="register">
                <v-text-field
                  @keyup.enter="register"
                  v-model="email"
                  :prepend-icon="$vuetify.icons.values.account"
                  name="register"
                  label="Email"
                  type="text"
                ></v-text-field>
                <v-text-field
                  @keyup.enter="register"
                  v-model="password"
                  :prepend-icon="$vuetify.icons.values.lock"
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
              <v-flex>
                <router-link to="/login">Go back to login</router-link></v-flex
              >
            </v-card-text>
            <v-card-actions>
              <v-btn to="/recover-password"> Forgot your password? </v-btn>
              <v-spacer></v-spacer>
              <v-btn @click.prevent="register" color="primary">Register</v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { api } from '@/api';
import { appName } from '@/env';
import { readRegistrationError } from '@/store/main/getters';
import { IUserProfileCreate } from '@/interfaces';
import { dispatchRegister } from '@/store/main/actions';
import { trackPageView } from '@/utils';

@Component
export default class Register extends Vue {
  public email = '';
  public password = '';
  public appName = appName;

  public mounted() {
    trackPageView();
  }

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
