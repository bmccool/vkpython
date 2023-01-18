# Installation
- This package relies on a Vulkan SDK, for our purposes, check the one at https://vulkan.lunarg.com/
# Notes
- There is currently a bug in the vulkan python package.
    - In vulkan\_vulkan.py, there is the line:
        `import collections as _collections`
    - It needs to be changed to
        `import collections.abc as _collections`
