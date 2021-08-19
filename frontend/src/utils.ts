import axios from 'axios';

export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token: string) =>
  localStorage.setItem('token', token);

export const removeLocalToken = () => localStorage.removeItem('token');

function getTimezone() {
  let tz = '';
  try {
    tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
  } catch (e) {
    return '';
  }
  return tz;
}

export const trackPageView = () => {
  const eventUrl = 'https://nocookieanalytics.com/api/v1/e/';
  if (!document.domain.includes('nocookieanalytics.com')) {
    return;
  }
  const urlParams = new URLSearchParams({
    et: 'page_view',
    url: document.URL,
    ref: document.referrer,
    tz: getTimezone(),
    w: screen.width.toString(),
    h: screen.height.toString(),
  });
  const url = eventUrl + '?' + urlParams.toString();
  axios.get(url);
};
