import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';

Vue.use(Vuetify);

const appColors = {
    newOrleans: '#edd693',
    flamePea: '#e75f3b',
};

export default new Vuetify({
    icons: {
        iconfont: 'mdi',
    },
    theme: {
        themes: {
            light: {
                secondary: appColors.newOrleans,
                primary: appColors.flamePea,
            },
        },
    },
});
