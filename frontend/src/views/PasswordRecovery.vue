<template>
  <v-main>
    <v-container fluid fill-height>
      <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
          <v-card>
            <v-toolbar dark color="primary" class="white--text" flat>
              <v-toolbar-title
                >{{ appName }} - Password Recovery</v-toolbar-title
              >
            </v-toolbar>
            <v-card-text>
              <p class="subheading">
                A password recovery email will be sent to the registered account
              </p>
              <v-form
                @keyup.enter="submit"
                v-model="valid"
                ref="form"
                @submit.prevent=""
                lazy-validation
              >
                <v-text-field
                  @keyup.enter="submit"
                  label="Email"
                  type="text"
                  :prepend-icon="$vuetify.icons.values.account"
                  v-model="username"
                  v-validate="'required'"
                  data-vv-name="username"
                  :error-messages="errors.collect('username')"
                  required
                ></v-text-field>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn class="ma-3" @click="cancel">Cancel</v-btn>
              <v-btn
                class="ma-3"
                color="primary"
                @click.prevent="submit"
                :disabled="!valid"
              >
                Recover Password
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </v-main>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { appName } from '@/env';
import { dispatchPasswordRecovery } from '@/store/main/actions';
import { trackPageView } from '@/utils';

@Component
export default class Login extends Vue {
  public valid = true;
  public username = '';
  public appName = appName;

  public mounted() {
    trackPageView();
  }

  public cancel() {
    this.$router.back();
  }

  public submit() {
    dispatchPasswordRecovery(this.$store, { username: this.username });
  }
}
</script>

<style></style>
