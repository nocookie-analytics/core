import Vue from 'vue';
import Vuetify from 'vuetify';
import colors from 'vuetify/lib/util/colors';

Vue.use(Vuetify);

const colors = {
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
                secondary: colors.newOrleans,
                primary: colors.flamePea,
            },
        },
    },
});
