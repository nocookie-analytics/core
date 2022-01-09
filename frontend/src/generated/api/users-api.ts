/* tslint:disable */
/* eslint-disable */
/**
 * No Cookie Analytics
 *  ## Javascript snippet  Integrate No Cookie Analytics on your website with a simple snippet. Add this script tag on your page and you\'re good to go:  ```javascript  <script async defer src=\"https://nocookieanalytics.com/latest.js\"></script> ```   ## OpenAPI documentation  The following routes are generated from the OpenAPI schema. 
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
import { BodyCreateUserOpenApiV1UsersOpenPost } from '../models';
// @ts-ignore
import { BodyUpdateUserMeApiV1UsersMePut } from '../models';
// @ts-ignore
import { HTTPValidationError } from '../models';
// @ts-ignore
import { User } from '../models';
/**
 * UsersApi - axios parameter creator
 * @export
 */
export const UsersApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Create new user without the need to be logged in.
         * @summary Create User Open
         * @param {BodyCreateUserOpenApiV1UsersOpenPost} bodyCreateUserOpenApiV1UsersOpenPost 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserOpen: async (bodyCreateUserOpenApiV1UsersOpenPost: BodyCreateUserOpenApiV1UsersOpenPost, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'bodyCreateUserOpenApiV1UsersOpenPost' is not null or undefined
            assertParamExists('createUserOpen', 'bodyCreateUserOpenApiV1UsersOpenPost', bodyCreateUserOpenApiV1UsersOpenPost)
            const localVarPath = `/api/v1/users/open`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(bodyCreateUserOpenApiV1UsersOpenPost, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Delete current user.
         * @summary Delete User Me
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteUserMe: async (options: any = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/users/me`;
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
         * Get a specific user by id.
         * @summary Read User By Id
         * @param {number} userId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readUserById: async (userId: number, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'userId' is not null or undefined
            assertParamExists('readUserById', 'userId', userId)
            const localVarPath = `/api/v1/users/{user_id}`
                .replace(`{${"user_id"}}`, encodeURIComponent(String(userId)));
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
         * Get current user.
         * @summary Read User Me
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readUserMe: async (options: any = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/users/me`;
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
         * Update own user.
         * @summary Update User Me
         * @param {BodyUpdateUserMeApiV1UsersMePut} [bodyUpdateUserMeApiV1UsersMePut] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateUserMe: async (bodyUpdateUserMeApiV1UsersMePut?: BodyUpdateUserMeApiV1UsersMePut, options: any = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/users/me`;
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
            localVarRequestOptions.data = serializeDataIfNeeded(bodyUpdateUserMeApiV1UsersMePut, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * UsersApi - functional programming interface
 * @export
 */
export const UsersApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = UsersApiAxiosParamCreator(configuration)
    return {
        /**
         * Create new user without the need to be logged in.
         * @summary Create User Open
         * @param {BodyCreateUserOpenApiV1UsersOpenPost} bodyCreateUserOpenApiV1UsersOpenPost 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createUserOpen(bodyCreateUserOpenApiV1UsersOpenPost: BodyCreateUserOpenApiV1UsersOpenPost, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<User>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createUserOpen(bodyCreateUserOpenApiV1UsersOpenPost, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Delete current user.
         * @summary Delete User Me
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async deleteUserMe(options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<User>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.deleteUserMe(options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Get a specific user by id.
         * @summary Read User By Id
         * @param {number} userId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readUserById(userId: number, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<User>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.readUserById(userId, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Get current user.
         * @summary Read User Me
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readUserMe(options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<User>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.readUserMe(options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * Update own user.
         * @summary Update User Me
         * @param {BodyUpdateUserMeApiV1UsersMePut} [bodyUpdateUserMeApiV1UsersMePut] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async updateUserMe(bodyUpdateUserMeApiV1UsersMePut?: BodyUpdateUserMeApiV1UsersMePut, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<User>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.updateUserMe(bodyUpdateUserMeApiV1UsersMePut, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
    }
};

/**
 * UsersApi - factory interface
 * @export
 */
export const UsersApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = UsersApiFp(configuration)
    return {
        /**
         * Create new user without the need to be logged in.
         * @summary Create User Open
         * @param {BodyCreateUserOpenApiV1UsersOpenPost} bodyCreateUserOpenApiV1UsersOpenPost 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserOpen(bodyCreateUserOpenApiV1UsersOpenPost: BodyCreateUserOpenApiV1UsersOpenPost, options?: any): AxiosPromise<User> {
            return localVarFp.createUserOpen(bodyCreateUserOpenApiV1UsersOpenPost, options).then((request) => request(axios, basePath));
        },
        /**
         * Delete current user.
         * @summary Delete User Me
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deleteUserMe(options?: any): AxiosPromise<User> {
            return localVarFp.deleteUserMe(options).then((request) => request(axios, basePath));
        },
        /**
         * Get a specific user by id.
         * @summary Read User By Id
         * @param {number} userId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readUserById(userId: number, options?: any): AxiosPromise<User> {
            return localVarFp.readUserById(userId, options).then((request) => request(axios, basePath));
        },
        /**
         * Get current user.
         * @summary Read User Me
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readUserMe(options?: any): AxiosPromise<User> {
            return localVarFp.readUserMe(options).then((request) => request(axios, basePath));
        },
        /**
         * Update own user.
         * @summary Update User Me
         * @param {BodyUpdateUserMeApiV1UsersMePut} [bodyUpdateUserMeApiV1UsersMePut] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updateUserMe(bodyUpdateUserMeApiV1UsersMePut?: BodyUpdateUserMeApiV1UsersMePut, options?: any): AxiosPromise<User> {
            return localVarFp.updateUserMe(bodyUpdateUserMeApiV1UsersMePut, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * Request parameters for createUserOpen operation in UsersApi.
 * @export
 * @interface UsersApiCreateUserOpenRequest
 */
export interface UsersApiCreateUserOpenRequest {
    /**
     * 
     * @type {BodyCreateUserOpenApiV1UsersOpenPost}
     * @memberof UsersApiCreateUserOpen
     */
    readonly bodyCreateUserOpenApiV1UsersOpenPost: BodyCreateUserOpenApiV1UsersOpenPost
}

/**
 * Request parameters for readUserById operation in UsersApi.
 * @export
 * @interface UsersApiReadUserByIdRequest
 */
export interface UsersApiReadUserByIdRequest {
    /**
     * 
     * @type {number}
     * @memberof UsersApiReadUserById
     */
    readonly userId: number
}

/**
 * Request parameters for updateUserMe operation in UsersApi.
 * @export
 * @interface UsersApiUpdateUserMeRequest
 */
export interface UsersApiUpdateUserMeRequest {
    /**
     * 
     * @type {BodyUpdateUserMeApiV1UsersMePut}
     * @memberof UsersApiUpdateUserMe
     */
    readonly bodyUpdateUserMeApiV1UsersMePut?: BodyUpdateUserMeApiV1UsersMePut
}

/**
 * UsersApi - object-oriented interface
 * @export
 * @class UsersApi
 * @extends {BaseAPI}
 */
export class UsersApi extends BaseAPI {
    /**
     * Create new user without the need to be logged in.
     * @summary Create User Open
     * @param {UsersApiCreateUserOpenRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public createUserOpen(requestParameters: UsersApiCreateUserOpenRequest, options?: any) {
        return UsersApiFp(this.configuration).createUserOpen(requestParameters.bodyCreateUserOpenApiV1UsersOpenPost, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Delete current user.
     * @summary Delete User Me
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public deleteUserMe(options?: any) {
        return UsersApiFp(this.configuration).deleteUserMe(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get a specific user by id.
     * @summary Read User By Id
     * @param {UsersApiReadUserByIdRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public readUserById(requestParameters: UsersApiReadUserByIdRequest, options?: any) {
        return UsersApiFp(this.configuration).readUserById(requestParameters.userId, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get current user.
     * @summary Read User Me
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public readUserMe(options?: any) {
        return UsersApiFp(this.configuration).readUserMe(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Update own user.
     * @summary Update User Me
     * @param {UsersApiUpdateUserMeRequest} requestParameters Request parameters.
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UsersApi
     */
    public updateUserMe(requestParameters: UsersApiUpdateUserMeRequest = {}, options?: any) {
        return UsersApiFp(this.configuration).updateUserMe(requestParameters.bodyUpdateUserMeApiV1UsersMePut, options).then((request) => request(this.axios, this.basePath));
    }
}
