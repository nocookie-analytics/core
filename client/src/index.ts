import objectHash from "object-hash";
import Perfume from "perfume.js";
import { IPerfumeNavigationTiming } from "perfume.js/dist/types/types";
import "whatwg-fetch";

const domain = "http://geektower.emoh";
const eventUrl = `${domain}/api/v1/e/`;

const perfume = new Perfume({
  resourceTiming: false,
  analyticsTracker: ({ metricName, data }) => {
    data = data as IPerfumeNavigationTiming;
    console.log(metricName, data);
    switch (metricName) {
      case "navigationTiming":
        {
          const performance = window.performance?.getEntriesByType(
            "navigation"
          )[0] as any;
          const { encodedBodySize } = performance;
          const { timeToFirstByte, totalTime, downloadTime } = data;

          let tz: string;
          try {
            tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
          } catch (e) {
            tz = "null";
          }
          const tzo = new Date().getTimezoneOffset();

          const urlParams = new URLSearchParams({
            url: document.URL,
            et: "page_view",
            pt: document.title,
            psb: encodedBodySize.toString(),
            ref: document.referrer,
            ttfb: timeToFirstByte?.toString() || "null",
            tt: totalTime?.toString() || "null",
            dt: downloadTime?.toString() || "null",
            tz: tz,
            tzo: tzo.toString(),
          });
          fetch(`${eventUrl}?${urlParams.toString()}`, {
            credentials: "omit",
          }).then((data) => console.log(data));
        }
        break;
      case "lcp":
        console.log(data, "lcp");
    }
  },
});
