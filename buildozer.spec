[app]

# (str) Title of your application
title = Route POS Merchant

# (str) Package name
package.name = routeposmerchant

# (str) Package domain (needed for android/ios packaging)
package.domain = com.node.routepos

# (str) Source code where the main.py lives
source.dir = app

# (list) Source files to include
source.include_exts = py,png,jpg,svg,json

# (str) Application versioning
version = 1.0.0

# (list) Application requirements
requirements = python3,flet

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33
android.minapi = 21

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

[buildozer]
log_level = 2
warn_on_root = 1
