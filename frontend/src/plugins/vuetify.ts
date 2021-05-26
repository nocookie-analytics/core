import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

const appColors = {
  newOrleans: '#edd693',
  lighterNewOrleans: '#fff4d8',
  flamePea: '#e75f3b',
};

import {
  mdiAccountCircle,
  mdiAccountEdit,
  mdiAccountPlus,
  mdiAlertCircle,
  mdiChevronLeft,
  mdiChevronRight,
  mdiDelete,
  mdiDns,
  mdiGroup,
  mdiDotsVertical,
  mdiWeb,
  mdiCalendar,
  mdiCheck,
  mdiClockOutline,
  mdiClose,
  mdiLock,
  mdiAccount,
} from '@mdi/js';

export default new Vuetify({
  icons: {
    iconfont: 'mdiSvg',
    values: {
      account: mdiAccount,
      accountCircle: mdiAccountCircle,
      accountEdit: mdiAccountEdit,
      accountPlus: mdiAccountPlus,
      alertCircle: mdiAlertCircle,
      calendar: mdiCalendar,
      check: mdiCheck,
      chevronLeft: mdiChevronLeft,
      chevronRight: mdiChevronRight,
      clockOutline: mdiClockOutline,
      close: mdiClose,
      delete: mdiDelete,
      dns: mdiDns,
      dotsVertical: mdiDotsVertical,
      group: mdiGroup,
      lock: mdiLock,
      web: mdiWeb,
    },
  },
  theme: {
    themes: {
      light: {
        secondary: appColors.lighterNewOrleans,
        primary: appColors.flamePea,
      },
    },
  },
});
