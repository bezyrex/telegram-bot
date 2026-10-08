#!/bin/bash
set -euo pipefail

## Colors
green="\e[32m"
red="\e[31m"
reset="\e[0m"

## Building Directory
BUILD_DIRECTORY="./dist/"

## .env
DOCKERHUB_PROJECT_NAME=$(grep -v '^#' .env | grep '^DOCKERHUB_PROJECT_NAME=' | cut -d '=' -f2- | tr -d '"'\')


if [ ! -f "$BUILD_DIRECTORY.setuped" ]; then
    printf "${red}You need to run ./build/setup.sh${reset}\n"

else
    DOCKERHUB_PROJECT_NAME=$(grep -v '^#' .env | grep '^DOCKERHUB_PROJECT_NAME=' | cut -d '=' -f2- | tr -d '"'\')
    printf "${green}Building Docker image.${reset}\n"
    docker build -t $DOCKERHUB_PROJECT_NAME .
    printf "${green}The image was created. Name of the Image = $DOCKERHUB_PROJECT_NAME.${reset}\n"

    ## Verification for publish.sh
    touch $BUILD_DIRECTORY/.builded
fi