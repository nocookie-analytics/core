import Vue from 'vue';
import Vuetify from 'vuetify/lib';

Vue.use(Vuetify);

const appColors = {
  newOrleans: '#edd693',
  lighterNewOrleans: '#fff4d8',
  flamePea: '#e75f3b',
};

import {
  mdiAccount,
  mdiAccountCircle,
  mdiAccountEdit,
  mdiAccountPlus,
  mdiAlertCircle,
  mdiCalendar,
  mdiCheck,
  mdiCheckboxBlankOutline,
  mdiCheckboxMarked,
  mdiChevronLeft,
  mdiChevronRight,
  mdiClockOutline,
  mdiClose,
  mdiDelete,
  mdiDns,
  mdiDotsVertical,
  mdiGroup,
  mdiLock,
  mdiLogin,
  mdiMenu,
  mdiOpenInNew,
  mdiPencil,
  mdiWeb,
} from '@mdi/js';

export default new Vuetify({
  icons: {
    values: {
      checkboxOff: mdiCheckboxBlankOutline,
      checkboxOn: mdiCheckboxMarked,
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
      menu: mdiMenu,
      pencil: mdiPencil,
      web: mdiWeb,
      login: mdiLogin,
      openInNew: mdiOpenInNew,
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
