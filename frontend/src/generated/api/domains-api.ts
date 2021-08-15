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
import { Domain } from '../models';
// @ts-ignore
import { DomainCreate } from '../models';
// @ts-ignore
import { DomainUpdate } from '../models';
// @ts-ignore
import { HTTPValidationError } from '../models';
/**
 * DomainsApi - axios parameter creator
 * @export
 */
export const DomainsApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Create new domain.
         * @summary Create Domain
         * @param {DomainCreate} domainCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createDomain: async (domainCreate: DomainCreate, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'domainCreate' is not null or undefined
            assertParamExists('createDomain', 'domainCreate', domainCreate)
            const localVarPath = `/api/v1/domains/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(domainCreate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Delete a domain.
         * @summary Delete Domain
         * @param {string} name 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteDomain: async (name: string, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'name' is not null or undefined
            assertParamExists('deleteDomain', 'name', name)
            const localVarPath = `/api/v1/domains/by-name/{name}`
                .replace(`{${"name"}}`, encodeURIComponent(String(name)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'DELETE', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Get domain by name
         * @summary Read Domain By Name
         * @param {string} name 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readDomainByName: async (name: string, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'name' is not null or undefined
            assertParamExists('readDomainByName', 'name', name)
            const localVarPath = `/api/v1/domains/by-name/{name}`
                .replace(`{${"name"}}`, encodeURIComponent(String(name)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Retrieve domains.
         * @summary Read Domains
         * @param {number} [skip] 
         * @param {number} [limit] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readDomains: async (skip?: number, limit?: number, options: any = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/domains/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)

            if (skip !== undefined) {
                localVarQueryParameter['skip'] = skip;
            }

            if (limit !== undefined) {
                localVarQueryParameter['limit'] = limit;
            }


    
            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Update a domain by name
         * @summary Update Domain By Name
         * @param {string} name 
         * @param {DomainUpdate} domainUpdate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateDomainByName: async (name: string, domainUpdate: DomainUpdate, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'name' is not null or undefined
            assertParamExists('updateDomainByName', 'name', name)
            // verify required parameter 'domainUpdate' is not null or undefined
            assertParamExists('updateDomainByName', 'domainUpdate', domainUpdate)
            const localVarPath = `/api/v1/domains/by-name/{name}`
                .replace(`{${"name"}}`, encodeURIComponent(String(name)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'PUT', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(domainUpdate, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * DomainsApi - functional programming interface
 * @export
 */
export const DomainsApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = DomainsApiAxiosParamCreator(configuration)
    return {
        /**
         * Create new domain.
         * @summary Create Domain
         * @param {DomainCreate} domainCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createDomain(domainCreate: DomainCreate, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Domain>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createDomain(domainCreate, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Delete a domain.
         * @summary Delete Domain
         * @param {string} name 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async deleteDomain(name: string, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Domain>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.deleteDomain(name, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Get domain by name
         * @summary Read Domain By Name
         * @param {string} name 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readDomainByName(name: string, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Domain>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.readDomainByName(name, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Retrieve domains.
         * @summary Read Domains
         * @param {number} [skip] 
         * @param {number} [limit] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readDomains(skip?: number, limit?: number, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<Domain>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.readDomains(skip, limit, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Update a domain by name
         * @summary Update Domain By Name
         * @param {string} name 
         * @param {DomainUpdate} domainUpdate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async updateDomainByName(name: string, domainUpdate: DomainUpdate, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Domain>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.updateDomainByName(name, domainUpdate, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
    }
};

/**
 * DomainsApi - factory interface
 * @export
 */
export const DomainsApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = DomainsApiFp(configuration)
    return {
        /**
         * Create new domain.
         * @summary Create Domain
         * @param {DomainCreate} domainCreate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createDomain(domainCreate: DomainCreate, options?: any): AxiosPromise<Domain> {
            return localVarFp.createDomain(domainCreate, options).then((request) => request(axios, basePath));
        },
        /**
         * Delete a domain.
         * @summary Delete Domain
         * @param {string} name 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteDomain(name: string, options?: any): AxiosPromise<Domain> {
            return localVarFp.deleteDomain(name, options).then((request) => request(axios, basePath));
        },
        /**
         * Get domain by name
         * @summary Read Domain By Name
         * @param {string} name 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readDomainByName(name: string, options?: any): AxiosPromise<Domain> {
            return localVarFp.readDomainByName(name, options).then((request) => request(axios, basePath));
        },
        /**
         * Retrieve domains.
         * @summary Read Domains
         * @param {number} [skip] 
         * @param {number} [limit] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readDomains(skip?: number, limit?: number, options?: any): AxiosPromise<Array<Domain>> {
            return localVarFp.readDomains(skip, limit, options).then((request) => request(axios, basePath));
        },
        /**
         * Update a domain by name
         * @summary Update Domain By Name
         * @param {string} name 
         * @param {DomainUpdate} domainUpdate 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateDomainByName(name: string, domainUpdate: DomainUpdate, options?: any): AxiosPromise<Domain> {
            return localVarFp.updateDomainByName(name, domainUpdate, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * Request parameters for createDomain operation in DomainsApi.
 * @export
 * @interface DomainsApiCreateDomainRequest
 */
export interface DomainsApiCreateDomainRequest {
    /**
     * 
     * @type {DomainCreate}
     * @memberof DomainsApiCreateDomain
     */
    readonly domainCreate: DomainCreate
}

/**
 * Request parameters for deleteDomain operation in DomainsApi.
 * @export
 * @interface DomainsApiDeleteDomainRequest
 */
export interface DomainsApiDeleteDomainRequest {
    /**
     * 
     * @type {string}
     * @memberof DomainsApiDeleteDomain
     */
    readonly name: string
}

/**
 * Request parameters for readDomainByName operation in DomainsApi.
 * @export
 * @interface DomainsApiReadDomainByNameRequest
 */
export interface DomainsApiReadDomainByNameRequest {
    /**
     * 
     * @type {string}
     * @memberof DomainsApiReadDomainByName
     */
    readonly name: string
}

/**
 * Request parameters for readDomains operation in DomainsApi.
 * @export
 * @interface DomainsApiReadDomainsRequest
 */
export interface DomainsApiReadDomainsRequest {
    /**
     * 
     * @type {number}
     * @memberof DomainsApiReadDomains
     */
    readonly skip?: number

    /**
     * 
     * @type {number}
     * @memberof DomainsApiReadDomains
     */
    readonly limit?: number
}

/**
 * Request parameters for updateDomainByName operation in DomainsApi.
 * @export
 * @interface DomainsApiUpdateDomainByNameRequest
 */
export interface DomainsApiUpdateDomainByNameRequest {
    /**
     * 
     * @type {string}
     * @memberof DomainsApiUpdateDomainByName
     */
    readonly name: string

    /**
     * 
     * @type {DomainUpdate}
     * @memberof DomainsApiUpdateDomainByName
     */
    readonly domainUpdate: DomainUpdate
}

/**
 * DomainsApi - object-oriented interface
 * @export
 * @class DomainsApi
 * @extends {BaseAPI}
 */
export class DomainsApi extends BaseAPI {
    /**
     * Create new domain.
     * @summary Create Domain
     * @param {DomainsApiCreateDomainRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DomainsApi
     */
    public createDomain(requestParameters: DomainsApiCreateDomainRequest, options?: any) {
        return DomainsApiFp(this.configuration).createDomain(requestParameters.domainCreate, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Delete a domain.
     * @summary Delete Domain
     * @param {DomainsApiDeleteDomainRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DomainsApi
     */
    public deleteDomain(requestParameters: DomainsApiDeleteDomainRequest, options?: any) {
        return DomainsApiFp(this.configuration).deleteDomain(requestParameters.name, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get domain by name
     * @summary Read Domain By Name
     * @param {DomainsApiReadDomainByNameRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DomainsApi
     */
    public readDomainByName(requestParameters: DomainsApiReadDomainByNameRequest, options?: any) {
        return DomainsApiFp(this.configuration).readDomainByName(requestParameters.name, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Retrieve domains.
     * @summary Read Domains
     * @param {DomainsApiReadDomainsRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DomainsApi
     */
    public readDomains(requestParameters: DomainsApiReadDomainsRequest = {}, options?: any) {
        return DomainsApiFp(this.configuration).readDomains(requestParameters.skip, requestParameters.limit, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Update a domain by name
     * @summary Update Domain By Name
     * @param {DomainsApiUpdateDomainByNameRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DomainsApi
     */
    public updateDomainByName(requestParameters: DomainsApiUpdateDomainByNameRequest, options?: any) {
        return DomainsApiFp(this.configuration).updateDomainByName(requestParameters.name, requestParameters.domainUpdate, options).then((request) => request(this.axios, this.basePath));
    }
}
