import Vue from 'vue';
import * as Sentry from '@sentry/vue';

export function initSentry(): void {
  if (document.domain.includes('nocookieanalytics.com')) {
    Sentry.init({
      Vue,
      dsn:
        'https://eb3dddeea7f7489c82431af7fa74c7e0@o879403.ingest.sentry.io/6196685',
      integrations: [],
      tracesSampleRate: 1.0,
    });
  }
}
