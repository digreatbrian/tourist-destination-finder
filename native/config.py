"""
Duck Native project configuration.

This file contains application, platform, appearance, and build settings
for the project.
"""


# APPLICATION

# Human-readable name displayed by the native application.
APP_NAME = "Tour Zim"


# Unique identifier used to identify the application on the target platform.
# For Android, this becomes the application's package name.
PACKAGE_NAME = "com.org.tourzim"


# Application version presented to users and app stores.
VERSION = "1.0.0"


# Internal numeric version used by the platform to determine whether a newer
# build has been installed.
VERSION_CODE = 1


# PERMISSIONS

# Native platform permissions requested by the application.
#
# Only declare permissions that the application actually requires. Duck Native
# uses this list when generating the platform-specific application manifest.
PERMISSIONS = [
    "android.permission.INTERNET",
]


# APPLICATION ICON

# Path to the application's icon.
#
# Duck Native uses this asset when generating the platform-specific application
# resources and launcher icons.
ICON = "native/assets/icon.png"


# SPLASH SCREEN

# Path to the image displayed while the native application is starting.
# SPLASH_IMAGE = "assets/splash.png"


# Background colour displayed behind the splash screen.
SPLASH_BACKGROUND = "#FFFFFF"


# ANDROID

# Minimum Android API level supported by the application.
MIN_SDK = 23


# Android API level used when compiling and targeting the application.
TARGET_SDK = 35


# Android SDK API level used to compile the application.
# Determines which Android APIs are available at compile time.
COMPILE_SDK = 34


# BUILD

# Target native platform for this project.
PLATFORM = "android"


# CPU architecture for which the native application will be built.
ARCHITECTURE = "arm64-v8a"


# Enables development-oriented build behaviour such as debugging information.
# Set this to False when producing a release build.
DEBUG = True


# Accepts invalid HTTPS certificates (self-signed, expired, wrong host) from
# your own server. Never leave this on for a public app.
ALLOW_INSECURE_CERTIFICATES = True


# Directory where Duck Native places generated build files and artifacts.
BUILD_DIR = "build"


# Java / Kotlin

# Java language and JVM bytecode version used to compile the native
# application. Duck Native applies this version to both Java and Kotlin.
JAVA_VERSION = 17


# SIGNING

# Path to the signing keystore used for release builds.
#
# Leave this unset or None during development. A release build must be signed
# before it can be distributed through an app store or installed as a trusted
# production application.
SIGNING_KEYSTORE = None


# Alias of the signing key inside the keystore.
SIGNING_KEY_ALIAS = None
