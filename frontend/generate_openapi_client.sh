#!/bin/bash


# run.sh script from Github here: https://raw.githubusercontent.com/OpenAPITools/openapi-generator/master/bin/utils/openapi-generator-cli.sh

# Using snapshot temporarily until a typescript-axios bug is released: https://github.com/OpenAPITools/openapi-generator/pull/8772
export OPENAPI_GENERATOR_VERSION=5.1.0-SNAPSHOT

bash $HOME/bin/openapi-generator/run.sh generate \
    -i <(curl "http://localhost/api/v1/openapi.json") \
    -g typescript-axios \
    -o ./src/generated/ \
    -p withSeparateModelsAndApi=true,apiPackage=api,modelPackage=models,useSingleRequestParameter=true

# https://github.com/OpenAPITools/openapi-generator/issues/7474
sed -i 's/_public/public/' ./src/generated/models/*.ts
