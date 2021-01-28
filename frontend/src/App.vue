<template>
    <div id="app">
        <v-app>
            <v-app-bar app color="primary" dark>
                <div class="d-flex align-center">
                    <v-img
                        alt="No Cookie Analytics"
                        class="shrink mr-2"
                        contain
                        src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
                        transition="scale-transition"
                        width="40"
                    />

                    No Cookie Analytics
                </div>

                <v-spacer></v-spacer>
            </v-app-bar>

            <v-main v-if="loggedIn === null">
                <v-container fill-height>
                    <v-layout align-center justify-center>
                        <v-flex>
                            <div class="text-xs-center">
                                <div class="headline my-5">Loading...</div>
                                <v-progress-circular
                                    size="100"
                                    indeterminate
                                    color="primary"
                                ></v-progress-circular>
                            </div>
                        </v-flex>
                    </v-layout>
                </v-container>
            </v-main>
            <router-view v-else />
            <NotificationsManager></NotificationsManager>
        </v-app>
    </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import NotificationsManager from '@/components/NotificationsManager.vue';
import { readIsLoggedIn } from '@/store/main/getters';
import { dispatchCheckLoggedIn } from '@/store/main/actions';

@Component({
    components: {
        NotificationsManager,
    },
})
export default class App extends Vue {
    get loggedIn() {
        return readIsLoggedIn(this.$store);
    }

    public async created() {
        await dispatchCheckLoggedIn(this.$store);
    }
}
</script>


<!--
<template>
    <v-app>
        <v-app-bar app color="primary" dark>
            <div class="d-flex align-center">
                <v-img
                    alt="Vuetify Logo"
                    class="shrink mr-2"
                    contain
                    src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
                    transition="scale-transition"
                    width="40"
                />

                <v-img
                    alt="Vuetify Name"
                    class="shrink mt-1 hidden-sm-and-down"
                    contain
                    min-width="100"
                    src="https://cdn.vuetifyjs.com/images/logos/vuetify-name-dark.png"
                    width="100"
                />
            </div>

            <v-spacer></v-spacer>

            <v-btn
                href="https://github.com/vuetifyjs/vuetify/releases/latest"
                target="_blank"
                text
            >
                <span class="mr-2">Latest Release</span>
                <v-icon>mdi-open-in-new</v-icon>
            </v-btn>
        </v-app-bar>

        <v-main>
            <router-view />
        </v-main>
    </v-app>
</template>

<script lang="ts">
import Vue from 'vue';

export default Vue.extend({
    name: 'App',

    data: () => ({
        //
    }),
});
</script>
-->
