<template>
  <div v-if="isLoggedIn">
    <v-navigation-drawer
      persistent
      :mini-variant="miniDrawer"
      v-model="showDrawer"
      fixed
      app
    >
      <v-layout column fill-height>
        <v-list dense>
          <v-list-item>Welcome {{ greetedUser }} </v-list-item>
          <v-list-item to="/domains">
            <v-list-item-action>
              <v-icon>{{ $vuetify.icons.values.dns }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Domains</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-group :prepend-icon="$vuetify.icons.values.accountCircle">
            <template v-slot:activator>
              <v-list-item-title>Account</v-list-item-title>
            </template>
            <v-list-item to="/main/profile/view">
              <v-list-item-action>
                <v-icon> {{ $vuetify.icons.values.account }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>Profile</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item to="/main/profile/edit">
              <v-list-item-action>
                <v-icon> {{ $vuetify.icons.values.accountEdit }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>Edit Profile</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item to="/main/profile/password">
              <v-list-item-action>
                <v-icon> {{ $vuetify.icons.values.lock }}</v-icon>
              </v-list-item-action>
              <v-list-item-content>
                <v-list-item-title>Change Password</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list-group>
        </v-list>
        <v-divider></v-divider>
        <v-list subheader v-show="hasAdminAccess">
          <v-subheader>Admin</v-subheader>
          <v-list-item to="/main/admin/users/all">
            <v-list-item-action>
              <v-icon> {{ $vuetify.icons.values.group }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Manage Users</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item to="/main/admin/users/create">
            <v-list-item-action>
              <v-icon> {{ $vuetify.icons.values.accountPlus }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Create User</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-spacer></v-spacer>
        <v-list>
          <v-list-item @click="logout">
            <v-list-item-action>
              <v-icon> {{ $vuetify.icons.values.close }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="switchMiniDrawer">
            <v-list-item-action>
              <v-icon v-if="miniDrawer">
                {{ $vuetify.icons.values.chevronRight }}</v-icon
              >
              <v-icon v-else> {{ $vuetify.icons.values.chevronLeft }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Collapse</v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-layout>
    </v-navigation-drawer>
    <v-app-bar dark color="secondary" app>
      <v-img
        alt="No Cookie Analytics"
        class="shrink mr-2"
        contain
        src="/img/logo.png"
        transition="scale-transition"
        width="40"
      />

      <v-img
        alt="No Cookie Analytics"
        src="/img/wordmark.png"
        class="shrink mt-1 hidden-sm-and-down"
        contain
        min-width="200"
        width="200"
      />
      <v-spacer></v-spacer>
      <v-menu bottom left offset-y>
        <template v-slot:activator="{ on }">
          <v-btn v-on="on" icon>
            <v-icon> {{ $vuetify.icons.values.moreVert }}</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item to="/main/profile">
            <v-list-item-content>
              <v-list-item-title>Profile</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon> {{ $vuetify.icons.values.person }}</v-icon>
            </v-list-item-action>
          </v-list-item>
          <v-list-item @click="logout">
            <v-list-item-content>
              <v-list-item-title>Logout</v-list-item-title>
            </v-list-item-content>
            <v-list-item-action>
              <v-icon> {{ $vuetify.icons.values.close }}</v-icon>
            </v-list-item-action>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
    <v-footer class="pa-3" fixed app>
      <v-spacer></v-spacer>
      <span>&copy; {{ appName }}</span>
    </v-footer>
  </div>
  <div v-else class="pt-16">
    <router-view></router-view>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'vue-property-decorator';

import { appName } from '@/env';
import {
  readDashboardMiniDrawer,
  readDashboardShowDrawer,
  readHasAdminAccess,
  readIsLoggedIn,
  readUserProfile,
} from '@/store/main/getters';
import {
  commitSetDashboardShowDrawer,
  commitSetDashboardMiniDrawer,
} from '@/store/main/mutations';
import {
  dispatchCheckLoggedIn,
  dispatchUserLogOut,
} from '@/store/main/actions';
import store from '@/store';

const startRouteGuard = async (to, from, next) => {
  await dispatchCheckLoggedIn(store);
  if (readIsLoggedIn(store)) {
    if (to.path === '/login' || to.path === '/') {
      next('/main/');
    } else {
      next();
    }
  } else if (readIsLoggedIn(store) === false) {
    if (
      to.path === '/' ||
      (to.path as string).startsWith('/main') ||
      (to.path as string).startsWith('/domains')
    ) {
      next('/login');
    } else {
      next();
    }
  }
};

@Component
export default class Main extends Vue {
  public appName = appName;

  public beforeRouteEnter(to, from, next) {
    startRouteGuard(to, from, next);
  }

  public beforeRouteUpdate(to, from, next) {
    startRouteGuard(to, from, next);
  }

  get miniDrawer() {
    return readDashboardMiniDrawer(this.$store);
  }

  get showDrawer() {
    return readDashboardShowDrawer(this.$store);
  }

  set showDrawer(value) {
    commitSetDashboardShowDrawer(this.$store, value);
  }

  public switchShowDrawer() {
    commitSetDashboardShowDrawer(
      this.$store,
      !readDashboardShowDrawer(this.$store),
    );
  }

  public switchMiniDrawer() {
    commitSetDashboardMiniDrawer(
      this.$store,
      !readDashboardMiniDrawer(this.$store),
    );
  }

  public get hasAdminAccess() {
    return readHasAdminAccess(this.$store);
  }

  public async logout() {
    await dispatchUserLogOut(this.$store);
  }

  get isLoggedIn() {
    return readIsLoggedIn(this.$store);
  }

  get greetedUser() {
    const userProfile = readUserProfile(this.$store);
    if (userProfile) {
      if (userProfile.full_name) {
        return userProfile.full_name;
      } else {
        return userProfile.email;
      }
    }
    return '';
  }
}
</script>
