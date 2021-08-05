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
         * @param {number} [w] 
         * @param {number} [h] 
         * @param {string} [pvid] Page view ID
         * @param {string} [tz] Timezone
         * @param {string} [ref] Referrer
         * @param {MetricType} [mn] Metric name
         * @param {number} [mv] Metric value
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        newEvent: async (url: string, et?: EventType, w?: number, h?: number, pvid?: string, tz?: string, ref?: string, mn?: MetricType, mv?: number, options: any = {}): Promise<RequestArgs> => {
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

            if (w !== undefined) {
                localVarQueryParameter['w'] = w;
            }

            if (h !== undefined) {
                localVarQueryParameter['h'] = h;
            }

            if (pvid !== undefined) {
                localVarQueryParameter['pvid'] = pvid;
            }

            if (tz !== undefined) {
                localVarQueryParameter['tz'] = tz;
            }

            if (url !== undefined) {
                localVarQueryParameter['url'] = url;
            }

            if (ref !== undefined) {
                localVarQueryParameter['ref'] = ref;
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
         * @param {number} [w] 
         * @param {number} [h] 
         * @param {string} [pvid] Page view ID
         * @param {string} [tz] Timezone
         * @param {string} [ref] Referrer
         * @param {MetricType} [mn] Metric name
         * @param {number} [mv] Metric value
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async newEvent(url: string, et?: EventType, w?: number, h?: number, pvid?: string, tz?: string, ref?: string, mn?: MetricType, mv?: number, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<EventCreated>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.newEvent(url, et, w, h, pvid, tz, ref, mn, mv, options);
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
         * @param {number} [w] 
         * @param {number} [h] 
         * @param {string} [pvid] Page view ID
         * @param {string} [tz] Timezone
         * @param {string} [ref] Referrer
         * @param {MetricType} [mn] Metric name
         * @param {number} [mv] Metric value
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        newEvent(url: string, et?: EventType, w?: number, h?: number, pvid?: string, tz?: string, ref?: string, mn?: MetricType, mv?: number, options?: any): AxiosPromise<EventCreated> {
            return localVarFp.newEvent(url, et, w, h, pvid, tz, ref, mn, mv, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * Request parameters for newEvent operation in EventsApi.
 * @export
 * @interface EventsApiNewEventRequest
 */
export interface EventsApiNewEventRequest {
    /**
     * 
     * @type {string}
     * @memberof EventsApiNewEvent
     */
    readonly url: string

    /**
     * Event type
     * @type {EventType}
     * @memberof EventsApiNewEvent
     */
    readonly et?: EventType

    /**
     * 
     * @type {number}
     * @memberof EventsApiNewEvent
     */
    readonly w?: number

    /**
     * 
     * @type {number}
     * @memberof EventsApiNewEvent
     */
    readonly h?: number

    /**
     * Page view ID
     * @type {string}
     * @memberof EventsApiNewEvent
     */
    readonly pvid?: string

    /**
     * Timezone
     * @type {string}
     * @memberof EventsApiNewEvent
     */
    readonly tz?: string

    /**
     * Referrer
     * @type {string}
     * @memberof EventsApiNewEvent
     */
    readonly ref?: string

    /**
     * Metric name
     * @type {MetricType}
     * @memberof EventsApiNewEvent
     */
    readonly mn?: MetricType

    /**
     * Metric value
     * @type {number}
     * @memberof EventsApiNewEvent
     */
    readonly mv?: number
}

/**
 * EventsApi - object-oriented interface
 * @export
 * @class EventsApi
 * @extends {BaseAPI}
 */
export class EventsApi extends BaseAPI {
    /**
     * Report a new event.
     * @summary New Event
     * @param {EventsApiNewEventRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof EventsApi
     */
    public newEvent(requestParameters: EventsApiNewEventRequest, options?: any) {
        return EventsApiFp(this.configuration).newEvent(requestParameters.url, requestParameters.et, requestParameters.w, requestParameters.h, requestParameters.pvid, requestParameters.tz, requestParameters.ref, requestParameters.mn, requestParameters.mv, options).then((request) => request(this.axios, this.basePath));
    }
}
