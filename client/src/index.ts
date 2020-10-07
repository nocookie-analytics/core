import Fingerprint2, { Component } from "fingerprintjs2";
import objectHash from "object-hash";
import Perfume from "perfume.js";
import { IPerfumeNavigationTiming } from "perfume.js/dist/types/types";
import "whatwg-fetch";

const domain = "http://localhost";
const eventUrl = `${domain}/api/v1/e/`;

const getComponents = () => {
  Fingerprint2.getPromise().then(handleComponents);
};

const perfume = new Perfume({
  resourceTiming: true,
  analyticsTracker: ({ metricName, data }) => {
    data = data as IPerfumeNavigationTiming;
    if (metricName == "navigationTiming") {
      const performance = window.performance?.getEntriesByType(
        "navigation"
      )[0] as any;
      const { encodedBodySize } = performance;
      const {
        dnsLookupTime,
        downloadTime,
        fetchTime,
        timeToFirstByte,
        totalTime,
      } = data;

      const urlParams = new URLSearchParams({
        uid: "aaaa",
        url: document.URL,
        et: "page_view",
        uas: navigator.userAgent,
        pt: document.title,
        psb: encodedBodySize.toString(),
        ref: document.referrer,
        ttfb: timeToFirstByte?.toString() || "null",
      });
      fetch(`${eventUrl}?${urlParams.toString()}`, {
        credentials: "omit",
      }).then((data) => console.log(data));
      console.log(
        encodedBodySize,
        dnsLookupTime,
        downloadTime,
        fetchTime,
        timeToFirstByte,
        totalTime
      );
    }
  },
});

const handleComponents = (components: Component[]) => {
  const userIdentifier: string = objectHash(components);
  console.log(userIdentifier);
};

if (window.requestIdleCallback) {
  window.requestIdleCallback(getComponents);
} else {
  setTimeout(getComponents, 500);
}
