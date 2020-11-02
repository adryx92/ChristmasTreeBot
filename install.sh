#!/bin/bash

# Thanks Pi-hole for the inspiration <3

# Set these values so the installer can still run in color
COL_NC='\e[0m' # No Color
COL_LIGHT_GREEN='\e[1;32m'
COL_LIGHT_RED='\e[1;31m'
COL_BLUE='\e[1;34m'
COL_YELLOW='\e[1;33m'
TICK="[${COL_LIGHT_GREEN}✓${COL_NC}]"
CROSS="[${COL_LIGHT_RED}✗${COL_NC}]"
INFO="[${COL_BLUE}i${COL_NC}]"
WARN="[${COL_YELLOW}!${COL_NC}]"
# shellcheck disable=SC2034
DONE="${COL_LIGHT_GREEN} done!${COL_NC}"
OVER="\\r\\033[K"

start_installation() {
    if  [ -x "$(command -v pip3)" ]; then
        printf "  %b %s is already installed\\n" "${TICK}" "pip"
    else
        printf "  %b %s not installed. Starting %s installation...\\n" "${INFO}" "pip" "pip"
        apt install python3-pip -y &> /dev/null
        if [ $? -eq 0 ]; then
            printf "  %b %s installed\\n\\n" "${TICK}" "pip"
        else
            return 0
        fi
    fi

    printf "\\n  %b Installing %s library\\n" "${INFO}" "pyTelegramBotAPI"
    pip3 install pyTelegramBotAPI &> /dev/null
    if [ $? -eq 0 ]; then
        printf "  %b %s installed\\n\\n" "${TICK}" "pyTelegramBotAPI"
    else
        return 0
    fi
    

    printf "\\n  %b Installing %s library\\n" "${INFO}" "emoji"
    pip3 install emoji --upgrade &> /dev/null
    if [ $? -eq 0 ]; then
        printf "  %b %s installed\\n\\n" "${TICK}" "emoji"
    else
        return 0
    fi

    printf "\\n  %b Installing %s library\\n" "${INFO}" "python3-gpiozero"
    apt install python3-gpiozero -y &> /dev/null
    if [ $? -eq 0 ]; then
        printf "  %b %s installed\\n\\n" "${TICK}" "python3-gpiozero"
    else
        return 0
    fi

    return 1
}

setup_permissions() {
    printf "\\n  %b Setting exec permissions to %s\\n" "${INFO}" "src.py"
    chmod +x src.py
}

    # If the user's id is zero,
if [[ "${EUID}" -eq 0 ]]; then
    # they are root and all is good
    printf "\\n  %b Running elevated. Starting installation... %s\\n\\n" "${TICK}"

    start_installation
    if [ $? -eq 1 ]; then
        setup_permissions
        printf "\\n\\n  %b Don't forget to add a cron to automatically start the bot!\\n" "${WARN}"
        printf "  %b Installation complete\\n\\n" "${TICK}"
    else
        printf "  %b Some error occurred during the installation.\\n\\n" "${CROSS}"
    fi

else
    printf "\\n %b Please run the command elevated!\\n" "${CROSS}"
    exit 1
    
fi

