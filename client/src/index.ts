import Fingerprint2, { Component } from "fingerprintjs2";
import objectHash from "object-hash";
import Perfume from "perfume.js";
import { IPerfumeNavigationTiming } from "perfume.js/dist/types/types";

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
