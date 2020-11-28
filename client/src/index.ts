import objectHash from "object-hash";
import Perfume from "perfume.js";
import { IPerfumeNavigationTiming } from "perfume.js/dist/types/types";
import "whatwg-fetch";
import { http } from "./utils";

const domain = "http://geektower.emoh";
const eventUrl = `${domain}/api/v1/e/`;

const perfume = new Perfume({
  resourceTiming: false,
  analyticsTracker: async ({ metricName, data }) => {
    let pageViewId: string = "";
    data = data as IPerfumeNavigationTiming;
    console.log("pageViewId:", pageViewId);
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
          const url = `${eventUrl}?${urlParams.toString()}`;
          const resp = await http(url);
          const result = await resp.json();
          pageViewId = result.pvid;
          console.log("pageViewId:", pageViewId);
        }
        break;
      case "lcp":
        const metricData = JSON.stringify({ lcp: data });
        console.log("pageViewId:", pageViewId);
        const urlParams = new URLSearchParams({
          url: document.URL,
          et: "metric",
          pvid: pageViewId,
          metric: metricData,
        });
        const url = `${eventUrl}?${urlParams.toString()}`;
        const resp = await http(url);
        const result = await resp.json();
        console.log(result);
    }
  },
});
