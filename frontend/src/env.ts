const domain = document.domain;

const protocol = process.env.VUE_APP_ENV === 'development' ? 'http' : 'https';

const envApiUrl = `${protocol}://${domain}`;

export const apiUrl = envApiUrl;
export const appName = 'No Cookie Analytics';
