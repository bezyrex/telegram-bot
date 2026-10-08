set -euo pipefail

### Hi. Im Zyrex from the past. 6/10/26. I wanna to say, this project is VibeCoded, with OpenCode. I didn't have time, to make manually. 

ENV_FILE=".env"

## Colors
green="\e[32m"
red="\e[31m"
reset="\e[0m"

## Build
BUILD_DIRECTORY="./dist"

printf "${green}Verifying .env variables for building.${reset}\n"
if [ -f "$BUILD_DIRECTORY/.setuped" ]; then
    printf "${red}You need to delete the file $BUILD_DIRECTORY/.setuped for run setup.sh again${reset}\n"
else
    REQUIRED_VARS=("DOCKERHUB_PROJECT_NAME" "GHCR_PROJECT_NAME" "DOCKERHUB_PROJECT_BUILD" "GHCR_PROJECT_BUILD")

    # 2. Check if the .env file exists
    if [ ! -f "$ENV_FILE" ]; then
        echo -e "${red}Error: File $ENV_FILE does not exist.${reset}"
        exit 1
    fi

    # 3. Verify each variable one by one
    MISSING_VARS=0
    for var in "${REQUIRED_VARS[@]}"; do
        # Search for the variable pattern (e.g., MY_VAR=value)
        if ! grep -q "^${var}=" "$ENV_FILE" || [ -z "$(grep "^${var}=" "$ENV_FILE" | cut -d'=' -f2-)" ]; then
            echo -e "${red} [✗] Missing or empty: $var${reset}"
            MISSING_VARS=$((MISSING_VARS + 1))
        else
            echo -e "${green} [✓] Present: $var${reset}"
        fi
    done

    # 4. If any variable is missing, abort execution
    if [ "$MISSING_VARS" -gt 0 ]; then
        echo -e "${red}\nError: Incomplete configuration in $ENV_FILE. Aborting.${reset}"
        exit 1
    fi

    # 5. Verification
    if [ ! -d "$BUILD_DIRECTORY" ]; then
        mkdir -p $BUILD_DIRECTORY
    fi

    touch $BUILD_DIRECTORY/.setuped
fi