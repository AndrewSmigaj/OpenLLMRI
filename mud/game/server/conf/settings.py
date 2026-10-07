r"""
Evennia settings file.

The available options are found in the default settings file found
here:

https://www.evennia.com/docs/latest/Setup/Settings-Default.html

Remember:

Don't copy more from the default file than you actually intend to
change; this will make sure that you don't overload upstream updates
unnecessarily.

When changing a setting requiring a file system path (like
path/to/actual/file.py), use GAME_DIR and EVENNIA_DIR to reference
your game folder and the Evennia library folders respectively. Python
paths (path.to.module) should be given relative to the game's root
folder (typeclasses.foo) whereas paths within the Evennia library
needs to be given explicitly (evennia.foo).

If you want to share your game dir, including its settings, you can
put secret game- or server-specific settings in secret_settings.py.

"""

# Use the defaults from Evennia unless explicitly overridden
from evennia.settings_default import *

######################################################################
# Evennia base server config
######################################################################

import os

# This is the name of your game. Make it catchy!
SERVERNAME = "Whiteout"

######################################################################
# Database — PostgreSQL. Credentials come from the container env
# (docker-compose.yml env_file: .env). The base image ships psycopg2.
######################################################################
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB", "whiteout"),
        "USER": os.environ.get("POSTGRES_USER", "whiteout"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
        "HOST": os.environ.get("POSTGRES_HOST", "postgres"),
        "PORT": os.environ.get("POSTGRES_PORT", "5432"),
    }
}

######################################################################
# Networking — bind all interfaces so the host can reach the container
# (telnet 4000, website 4001, websocket client 4002).
######################################################################
TELNET_INTERFACES = ["0.0.0.0"]
WEBSOCKET_CLIENT_INTERFACE = "0.0.0.0"
ALLOWED_HOSTS = ["*"]  # dev only

######################################################################
# Whiteout subsystems.
#   world.sim is PURE PYTHON (no Django app) — imported directly, never installed.
#   Register a scenario's Django app here ONLY if it needs its own DB tables, e.g.:
#       INSTALLED_APPS += ("world.scenarios.whiteout.app",)
######################################################################


######################################################################
# Settings given in secret_settings.py override those in this file.
######################################################################
try:
    from server.conf.secret_settings import *
except ImportError:
    print("secret_settings.py file not found or failed to import.")
