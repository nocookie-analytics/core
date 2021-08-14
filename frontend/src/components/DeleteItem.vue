<template>
  <v-dialog max-width="600px">
    <template v-slot:activator="{ on, attrs }">
      <v-container>
        <v-icon>{{ mdiAlertCircle }}</v-icon>
        Warning! This action is irreversible.
      </v-container>
      <v-btn class="ma-3" color="error" v-bind="attrs" v-on="on"
        >Delete {{ itemName }}</v-btn
      >
    </template>
    <v-card>
      <v-card-title>
        <span class="text-h5">Enter "delete me" to confirm</span>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field
                label="Confirmation message"
                v-model="confirmationMessage"
                required
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-btn
                class="ma-3"
                :disabled="confirmationMessage.toLowerCase() !== 'delete me'"
                color="error"
                @click="deleteFunction"
                >Delete {{ itemName }}</v-btn
              >
            </v-col>
          </v-row>
        </v-container>
      </v-card-title>
    </v-card>
  </v-dialog>
</template>

<script lang="ts">
import { mdiAlertCircle } from '@mdi/js';
import { Component, Prop, Vue } from 'vue-property-decorator';

@Component
export default class DeleteItem extends Vue {
  @Prop() public itemName!: string;
  @Prop() public deleteFunction!: () => void;
  public confirmationMessage = '';
  mdiAlertCircle = mdiAlertCircle;
}
</script>
