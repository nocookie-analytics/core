import axios, { AxiosResponse } from 'axios';
import { EventCreated } from './generated';

export const getLocalToken = () => localStorage.getItem('token');

export const saveLocalToken = (token: string) =>
  localStorage.setItem('token', token);

let lastPageViewId: string | undefined = undefined;

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

const apiBase = 'https://nocookieanalytics.com';

export const trackPageView = async (): Promise<undefined> => {
  const eventUrl = `${apiBase}/api/v1/e/page_view`;
  if (!document.domain.includes('nocookieanalytics.com')) {
    return;
  }
  const urlParams = new URLSearchParams({
    url: document.URL,
    ref: document.referrer,
    tz: getTimezone(),
    w: screen.width.toString(),
    h: screen.height.toString(),
  });
  const url = eventUrl + '?' + urlParams.toString();
  const response: AxiosResponse<EventCreated> = await axios.get(url);
  lastPageViewId = response.data.page_view_id;
};

export const trackCustomEvent = (eventName: string): undefined => {
  const eventUrl = `${apiBase}/api/v1/e/custom`;
  if (!document.domain.includes('nocookieanalytics.com')) {
    return;
  }
  if (lastPageViewId) {
    const urlParams = new URLSearchParams({
      url: document.URL,
      page_view_id: lastPageViewId,
      event_name: eventName,
    });
    const url = eventUrl + '?' + urlParams.toString();
    axios.get(url);
  } else {
    console.error('No page view id found, but custom event function called');
  }
};
