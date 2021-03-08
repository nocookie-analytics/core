#!/bin/bash

openapi-generator generate \
    -i <(curl "http://localhost/api/v1/openapi.json") \
    -g typescript-axios \
    -o ./src/generated/ \
    -p withSeparateModelsAndApi=true,apiPackage=api,modelPackage=models,withInterfaces=true
