"""Declare all global constants."""

COMMANDS = {
    "start" : "Check whether I am alive",
    "forward" : "Set a new forward",
    "remove" : "Remove an existing forward",
    "help" : "Learn usage",
}

REGISTER_COMMANDS = True

KEEP_LAST_MANY = 10000

CONFIG_FILE_NAME = "tomtrix.config.json"
CONFIG_ENV_VAR_NAME = "tomtrix_CONFIG"

MONGO_DB_NAME = "tomtrix-config"
MONGO_COL_NAME = "tomtrix-instance-0"
