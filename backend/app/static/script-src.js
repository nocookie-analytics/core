(function () {
  var pageViewId = '';
  var reportServer = 'nocookieanalytics.com';
  var protocol = 'https';
  var me = document.currentScript;
  if (me && me.attributes['data-domain']) {
    reportServer = me.attributes['data-domain'].value;
  }
  var eventUrl = protocol + '://' + reportServer + '/api/v1/e/';

  function getTimezone() {
    var tz = '';
    try {
      tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    } catch (e) {}
    return tz;
  }

  function httpGet(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send(null);
  }

  function reportMetric(metricName, metricValue) {
    var urlParams = new URLSearchParams({
      et: 'metric',
      url: document.URL,
      pvid: pageViewId,
      mn: metricName,
      mv: metricValue.toString(),
    });
    var url = eventUrl + '?' + urlParams.toString();
    httpGet(url);
  }

  function trackPageView() {
    var urlParams = new URLSearchParams({
      et: 'page_view',
      url: document.URL,
      ref: document.referrer,
      tz: getTimezone(),
      w: screen.width.toString(),
      h: screen.height.toString(),
    });
    var url = eventUrl + '?' + urlParams.toString();
    httpGet(url);
  }

  function trackURLChanges() {
    var historyPushState = history.pushState;
    if (historyPushState) {
      history.pushState = function (state, title, url) {
        trackPageView();
        historyPushState.apply(this, [state, title, url]);
      };
      addEventListener('popstate', trackPageView);
    }
  }

  trackPageView();
  trackURLChanges();
})();
