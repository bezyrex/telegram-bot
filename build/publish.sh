#!/bin/bash
set -u

## Colors
green="\e[32m"
red="\e[31m"
reset="\e[0m"

printf "${green}Publishing images to Docker HUB and GHCR${reset}\n"

## .env
DOCKERHUB_PROJECT_NAME=$(grep -v '^#' .env | grep '^DOCKERHUB_PROJECT_NAME=' | cut -d '=' -f2- | tr -d '"'\')
DOCKERHUB_PROJECT_BUILD=$(grep -v '^#' .env | grep '^DOCKERHUB_PROJECT_BUILD=' | cut -d '=' -f2- | tr -d '"'\')
GHCR_PROJECT_NAME=$(grep -v '^#' .env | grep '^GHCR_PROJECT_NAME=' | cut -d '=' -f2- | tr -d '"'\')
GHCR_PROJECT_BUILD=$(grep -v '^#' .env | grep '^GHCR_PROJECT_BUILD=' | cut -d '=' -f2- | tr -d '"'\')
VERSION=$(grep -v '^#' .env | grep '^VERSION=' | cut -d '=' -f2- | tr -d '"'\')

## Builded?
BUILD_FILE="./dist/.builded"

if [ -f "$BUILD_FILE" ]; then
    BUILD_EXECUTED=true
else
    BUILD_EXECUTED=false
fi

if $BUILD_EXECUTED; then
    
    # 1. DOCKER HUB
    if $DOCKERHUB_PROJECT_BUILD; then
        echo " "
        printf "${green}[✓] Uploading to Docker Hub...${reset}\n"
        docker push "$DOCKERHUB_PROJECT_NAME:latest"
        docker tag "$DOCKERHUB_PROJECT_NAME" "$DOCKERHUB_PROJECT_NAME:$VERSION"
        docker push "$DOCKERHUB_PROJECT_NAME:$VERSION"
        
        # $? checks the result of the previous docker push command
        if [ $? -eq 0 ]; then
            printf "${green}[✓] Published to Docker Hub as $DOCKERHUB_PROJECT_NAME${reset}\n"
        else
            printf "${red}[✗] ERROR: Docker Hub upload failed. Continuing with the flow...${reset}\n"
        fi
    else
        printf "${red}[✗] Skipped Docker Hub${reset}\n"
    fi
    
    # 2. GHCR (Runs always, regardless of what happened above)
    if $GHCR_PROJECT_BUILD; then
        echo " "
        printf "${green}[✓] Uploading to GHCR...${reset}\n"
        docker tag "$DOCKERHUB_PROJECT_NAME" "$GHCR_PROJECT_NAME:latest"
        docker push "$GHCR_PROJECT_NAME:latest"
        docker tag "$DOCKERHUB_PROJECT_NAME" "$GHCR_PROJECT_NAME:$VERSION"
        docker push "$GHCR_PROJECT_NAME:$VERSION"
        
        if [ $? -eq 0 ]; then
            printf "${green}[✓] Published to GHCR as $GHCR_PROJECT_NAME:latest${reset}\n"
        else
            printf "${red}[✗] ERROR: GHCR upload failed.${reset}\n"
        fi
    else
        printf "${red}[✗] Skipped GHCR${reset}\n"
    fi
else 
    printf "${red}[✗] You need to run ./build/build.sh${reset}\n"
fi
