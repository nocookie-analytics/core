let envApiUrl = '';

const domain = document.domain;

let env = '';

if (domain === 'test.nocookieanalytics.com') {
  env = 'test';
} else if (domain === 'stag.nocookieanalytics.com') {
  env = 'staging';
} else if (domain === 'www.nocookieanalytics.com') {
  env = 'production';
}

if (env === 'production') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_PROD}`;
} else if (env === 'staging') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_STAG}`;
} else if (env == 'test') {
  envApiUrl = `https://${process.env.VUE_APP_DOMAIN_TEST}`;
} else {
  envApiUrl = `http://${process.env.VUE_APP_DOMAIN_DEV}`;
}

console.log(env, envApiUrl);

export const apiUrl = envApiUrl;
export const appName = 'No Cookie Analytics';
