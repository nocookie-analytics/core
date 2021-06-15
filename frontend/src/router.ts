import Vue from 'vue';
import Router from 'vue-router';

import RouterComponent from './components/RouterComponent.vue';

if (process.env.NODE_ENV !== 'test') {
  // Using vue router in tests means we cannot mock it
  Vue.use(Router);
}

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () =>
        import(/* webpackChunkName: start */ './views/main/Main.vue'),
      children: [
        {
          path: 'login',
          // route level code-splitting
          // this generates a separate chunk (about.[hash].js) for this route
          // which is lazy-loaded when the route is visited.
          component: () =>
            import(/* webpackChunkName: "users-login" */ './views/Login.vue'),
        },
        {
          path: 'register',
          component: () =>
            import(
              /* webpackChunkName: "users-register" */ './views/Register.vue'
            ),
        },
        {
          path: 'recover-password',
          component: () =>
            import(
              /* webpackChunkName: "users-recover-password" */ './views/PasswordRecovery.vue'
            ),
        },
        {
          path: 'reset-password',
          component: () =>
            import(
              /* webpackChunkName: "users-reset-password" */ './views/ResetPassword.vue'
            ),
        },
        {
          path: 'main',
          component: () =>
            import(/* webpackChunkName: "main-dummy" */ './views/Dummy.vue'),
          children: [
            {
              path: 'profile',
              component: RouterComponent,
              redirect: 'profile/view',
              children: [
                {
                  path: 'view',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-profile" */ './views/main/profile/UserProfile.vue'
                    ),
                },
                {
                  path: 'edit',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-profile-edit" */ './views/main/profile/UserProfileEdit.vue'
                    ),
                },
                {
                  path: 'password',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-profile-password" */ './views/main/profile/UserProfileEditPassword.vue'
                    ),
                },
              ],
            },
            {
              path: 'admin',
              component: () =>
                import(
                  /* webpackChunkName: "main-admin" */ './views/main/admin/Admin.vue'
                ),
              redirect: 'admin/users/all',
              children: [
                {
                  path: 'users',
                  redirect: 'users/all',
                },
                {
                  path: 'users/all',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-admin-users" */ './views/main/admin/AdminUsers.vue'
                    ),
                },
                {
                  path: 'users/edit/:id',
                  name: 'main-admin-users-edit',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-admin-users-edit" */ './views/main/admin/EditUser.vue'
                    ),
                },
                {
                  path: 'users/create',
                  name: 'main-admin-users-create',
                  component: () =>
                    import(
                      /* webpackChunkName: "main-admin-users-create" */ './views/main/admin/CreateUser.vue'
                    ),
                },
              ],
            },
          ],
        },
        {
          path: 'domains',
          component: () =>
            import(/* webpackChunkName: "domains" */ './views/Dummy.vue'),
          children: [
            {
              path: '/',
              name: 'list-domains',
              component: () =>
                import(
                  /* webpackChunkName: "domains-list-domains" */ './views/main/domains/ListDomains.vue'
                ),
            },
            {
              path: 'create',
              name: 'create-domain',
              component: () =>
                import(
                  /* webpackChunkName: "domains-create-domain" */ './views/main/domains/EditDomain.vue'
                ),
            },
            {
              path: ':domainName',
              name: 'edit-domain',
              component: () =>
                import(
                  /* webpackChunkName: "domains-edit-domain" */ './views/main/domains/EditDomain.vue'
                ),
            },
          ],
        },
        {
          // This route is a pokemon route, it should always be last
          path: ':domainName',
          component: () =>
            import(
              /* webpackChunkName: view-analytics */ './views/main/ViewAnalytics.vue'
            ),
        },
      ],
    },
    {
      path: '/*',
      redirect: '/',
    },
  ],
});
