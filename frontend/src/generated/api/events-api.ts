/* tslint:disable */
/* eslint-disable */
/**
 * No Cookie Analytics
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import globalAxios, { AxiosPromise, AxiosInstance } from 'axios';
import { Configuration } from '../configuration';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from '../common';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, RequestArgs, BaseAPI, RequiredError } from '../base';
// @ts-ignore
import { EventCreated } from '../models';
// @ts-ignore
import { EventType } from '../models';
// @ts-ignore
import { HTTPValidationError } from '../models';
// @ts-ignore
import { MetricType } from '../models';
/**
 * EventsApi - axios parameter creator
 * @export
 */
export const EventsApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Report a new event.
         * @summary New Event
         * @param {string} url 
         * @param {EventType} [et] Event type
         * @param {string} [pt] Page title
         * @param {string} [pvid] Page view ID
         * @param {number} [psb] Page size bytes
         * @param {string} [tz] Timezone
         * @param {number} [tzo] Timezone offset
         * @param {string} [ref] Referrer
         * @param {number} [ttfb] Time to first-byte
         * @param {number} [tt] Total time
         * @param {number} [dt] Download time
         * @param {MetricType} [mn] Metric name
         * @param {number} [mv] Metric value
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        newEvent: async (url: string, et?: EventType, pt?: string, pvid?: string, psb?: number, tz?: string, tzo?: number, ref?: string, ttfb?: number, tt?: number, dt?: number, mn?: MetricType, mv?: number, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'url' is not null or undefined
            assertParamExists('newEvent', 'url', url)
            const localVarPath = `/api/v1/e/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (et !== undefined) {
                localVarQueryParameter['et'] = et;
            }

            if (url !== undefined) {
                localVarQueryParameter['url'] = url;
            }

            if (pt !== undefined) {
                localVarQueryParameter['pt'] = pt;
            }

            if (pvid !== undefined) {
                localVarQueryParameter['pvid'] = pvid;
            }

            if (psb !== undefined) {
                localVarQueryParameter['psb'] = psb;
            }

            if (tz !== undefined) {
                localVarQueryParameter['tz'] = tz;
            }

            if (tzo !== undefined) {
                localVarQueryParameter['tzo'] = tzo;
            }

            if (ref !== undefined) {
                localVarQueryParameter['ref'] = ref;
            }

            if (ttfb !== undefined) {
                localVarQueryParameter['ttfb'] = ttfb;
            }

            if (tt !== undefined) {
                localVarQueryParameter['tt'] = tt;
            }

            if (dt !== undefined) {
                localVarQueryParameter['dt'] = dt;
            }

            if (mn !== undefined) {
                localVarQueryParameter['mn'] = mn;
            }

            if (mv !== undefined) {
                localVarQueryParameter['mv'] = mv;
            }


    
            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * EventsApi - functional programming interface
 * @export
 */
export const EventsApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = EventsApiAxiosParamCreator(configuration)
    return {
        /**
         * Report a new event.
         * @summary New Event
         * @param {string} url 
         * @param {EventType} [et] Event type
         * @param {string} [pt] Page title
         * @param {string} [pvid] Page view ID
         * @param {number} [psb] Page size bytes
         * @param {string} [tz] Timezone
         * @param {number} [tzo] Timezone offset
         * @param {string} [ref] Referrer
         * @param {number} [ttfb] Time to first-byte
         * @param {number} [tt] Total time
         * @param {number} [dt] Download time
         * @param {MetricType} [mn] Metric name
         * @param {number} [mv] Metric value
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async newEvent(url: string, et?: EventType, pt?: string, pvid?: string, psb?: number, tz?: string, tzo?: number, ref?: string, ttfb?: number, tt?: number, dt?: number, mn?: MetricType, mv?: number, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<EventCreated>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.newEvent(url, et, pt, pvid, psb, tz, tzo, ref, ttfb, tt, dt, mn, mv, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
    }
};

/**
 * EventsApi - factory interface
 * @export
 */
export const EventsApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = EventsApiFp(configuration)
    return {
        /**
         * Report a new event.
         * @summary New Event
         * @param {string} url 
         * @param {EventType} [et] Event type
         * @param {string} [pt] Page title
         * @param {string} [pvid] Page view ID
         * @param {number} [psb] Page size bytes
         * @param {string} [tz] Timezone
         * @param {number} [tzo] Timezone offset
         * @param {string} [ref] Referrer
         * @param {number} [ttfb] Time to first-byte
         * @param {number} [tt] Total time
         * @param {number} [dt] Download time
         * @param {MetricType} [mn] Metric name
         * @param {number} [mv] Metric value
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        newEvent(url: string, et?: EventType, pt?: string, pvid?: string, psb?: number, tz?: string, tzo?: number, ref?: string, ttfb?: number, tt?: number, dt?: number, mn?: MetricType, mv?: number, options?: any): AxiosPromise<EventCreated> {
            return localVarFp.newEvent(url, et, pt, pvid, psb, tz, tzo, ref, ttfb, tt, dt, mn, mv, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * EventsApi - interface
 * @export
 * @interface EventsApi
 */
export interface EventsApiInterface {
    /**
     * Report a new event.
     * @summary New Event
     * @param {string} url 
     * @param {EventType} [et] Event type
     * @param {string} [pt] Page title
     * @param {string} [pvid] Page view ID
     * @param {number} [psb] Page size bytes
     * @param {string} [tz] Timezone
     * @param {number} [tzo] Timezone offset
     * @param {string} [ref] Referrer
     * @param {number} [ttfb] Time to first-byte
     * @param {number} [tt] Total time
     * @param {number} [dt] Download time
     * @param {MetricType} [mn] Metric name
     * @param {number} [mv] Metric value
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof EventsApiInterface
     */
    newEvent(url: string, et?: EventType, pt?: string, pvid?: string, psb?: number, tz?: string, tzo?: number, ref?: string, ttfb?: number, tt?: number, dt?: number, mn?: MetricType, mv?: number, options?: any): AxiosPromise<EventCreated>;

}

/**
 * EventsApi - object-oriented interface
 * @export
 * @class EventsApi
 * @extends {BaseAPI}
 */
export class EventsApi extends BaseAPI implements EventsApiInterface {
    /**
     * Report a new event.
     * @summary New Event
     * @param {string} url 
     * @param {EventType} [et] Event type
     * @param {string} [pt] Page title
     * @param {string} [pvid] Page view ID
     * @param {number} [psb] Page size bytes
     * @param {string} [tz] Timezone
     * @param {number} [tzo] Timezone offset
     * @param {string} [ref] Referrer
     * @param {number} [ttfb] Time to first-byte
     * @param {number} [tt] Total time
     * @param {number} [dt] Download time
     * @param {MetricType} [mn] Metric name
     * @param {number} [mv] Metric value
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof EventsApi
     */
    public newEvent(url: string, et?: EventType, pt?: string, pvid?: string, psb?: number, tz?: string, tzo?: number, ref?: string, ttfb?: number, tt?: number, dt?: number, mn?: MetricType, mv?: number, options?: any) {
        return EventsApiFp(this.configuration).newEvent(url, et, pt, pvid, psb, tz, tzo, ref, ttfb, tt, dt, mn, mv, options).then((request) => request(this.axios, this.basePath));
    }
}
