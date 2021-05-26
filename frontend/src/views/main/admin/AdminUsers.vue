<template>
  <div>
    <v-toolbar light>
      <v-toolbar-title> Manage Users </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn color="primary" to="/main/admin/users/create">Create User</v-btn>
    </v-toolbar>
    <v-data-table :headers="headers" :items="users">
      <template #[`item.isActive`]="{ item }">
        <v-icon v-if="item.is_active">
          {{ $vuetify.icons.values.check }}</v-icon
        >
      </template>
      <template #[`item.isSuperuser`]="{ item }">
        <v-icon v-if="item.is_superuser">
          {{ $vuetify.icons.values.check }}</v-icon
        >
      </template>
      <template #[`item.id`]="{ item }">
        <v-tooltip top>
          <span>Edit</span>
          <template v-slot:activator="{ on }">
            <v-btn
              v-on="on"
              text
              :to="{
                name: 'main-admin-users-edit',
                params: { id: item.id },
              }"
            >
              <v-icon>{{ $vuetify.icons.values.edit }}</v-icon>
            </v-btn>
          </template>
        </v-tooltip>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import { readAdminUsers } from '@/store/admin/getters';
import { dispatchGetUsers } from '@/store/admin/actions';

@Component
export default class AdminUsers extends Vue {
  public headers = [
    {
      text: 'Email',
      sortable: true,
      value: 'email',
      align: 'left',
    },
    {
      text: 'Full Name',
      sortable: true,
      value: 'full_name',
      align: 'left',
    },
    {
      text: 'Is Active',
      sortable: true,
      value: 'isActive',
      align: 'left',
    },
    {
      text: 'Is Superuser',
      sortable: true,
      value: 'isSuperuser',
      align: 'left',
    },
    {
      text: 'Actions',
      value: 'id',
    },
  ];
  get users() {
    return readAdminUsers(this.$store);
  }

  public async mounted() {
    await dispatchGetUsers(this.$store);
  }
}
</script>
