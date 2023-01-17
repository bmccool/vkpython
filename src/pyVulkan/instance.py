from pyVulkan.config import *

def supported(extensions, layers, debug):

    """
        ExtensionProperties( std::array<char, VK_MAX_EXTENSION_NAME_SIZE> const & extensionName_ = {},
                           uint32_t                                             specVersion_ = {} )
    """
        
    #check extension support
    supportedExtensions = [extension.extensionName for extension in vkEnumerateInstanceExtensionProperties(None)]

    logger.debug("Device can support the following extensions:")
    logger.pretty(Logger.DEBUG, supportedExtensions)
    
    for extension in extensions:
        
        if extension in supportedExtensions:
            logger.debug(f"Extension \"{extension}\" is supported!")
        else:
            logger.debug(f"Extension \"{extension}\" is not supported!")
            return False

    #check layer support
    supportedLayers = [layer.layerName for layer in vkEnumerateInstanceLayerProperties()]

    logger.debug("Device can support the following layers:")
    logger.pretty(Logger.DEBUG, supportedLayers)

    for layer in layers:
        if layer in supportedLayers:
            logger.debug(f"Layer \"{layer}\" is supported!")
        else:
            logger.debug(f"Layer \"{layer}\" is not supported!")
            return False

    return True

def make_instance(applicationName, debug=True):

    logger.debug("Making an instance...")

    """
    An instance stores all per-application state info, it is a vulkan handle
    (An opaque integer or pointer value used to refer to a Vulkan object)
    """

    """
    We can scan the system and check which version it will support up to,
    as of vulkan 1.1

    VkResult vkEnumerateInstanceVersion(
        uint32_t*       pApiVersion);
    """
    version = vkEnumerateInstanceVersion()
    logger.debug(f"System can support vulkan (Variant.M.m.p): {version >> 29}.{VK_VERSION_MAJOR(version)}.{VK_VERSION_MINOR(version)}.{VK_VERSION_PATCH(version)}")

    """ For our use, we will specify a lower (less bleeding edge) version """
    version = VK_MAKE_VERSION(1, 0, 0)
    logger.debug(f"System will target vulkan (Variant.M.m.p): {version >> 29}.{VK_VERSION_MAJOR(version)}.{VK_VERSION_MINOR(version)}.{VK_VERSION_PATCH(version)}")

    """
        from _vulkan.py:
        def VkApplicationInfo(
            sType=VK_STRUCTURE_TYPE_APPLICATION_INFO,
            pNext=None,
            pApplicationName=None,
            applicationVersion=None,
            pEngineName=None,
            engineVersion=None,
            apiVersion=None,
        )
    """
    appInfo = VkApplicationInfo(
            pApplicationName=applicationName,
            applicationVersion=None,
            pEngineName="Doing it the hard way",
            engineVersion=version,
            apiVersion=version,
    )

    """
        Everything with Vulkan is "opt-in", so we need to query which extensions glfw needs
        in order to interface with vulkan.
    """
    extensions = glfw.get_required_instance_extensions()

    if debug:
        extensions.append(VK_EXT_DEBUG_REPORT_EXTENSION_NAME)


    logger.debug("glfw requires the following instance extensions:")
    logger.pretty(Logger.DEBUG, extensions)

    layers = []
    if debug:
        layers.append("VK_LAYER_KHRONOS_validation")

    supported(extensions, layers, debug)

    """
        from _vulkan.py:
        def VkInstanceCreateInfo(
            sType=VK_STRUCTURE_TYPE_INSTANCE_CREATE_INFO,
            pNext=None,
            flags=None,
            pApplicationInfo=None,
            enabledLayerCount=None,ppEnabledLayerNames=None,
            enabledExtensionCount=None,ppEnabledExtensionNames=None,
        )
    """
    createInfo = VkInstanceCreateInfo(
        pApplicationInfo = appInfo,
        enabledLayerCount = len(layers), ppEnabledLayerNames = layers,
        enabledExtensionCount = len(extensions), ppEnabledExtensionNames = extensions
    )

    """
        def vkCreateInstance(
            pCreateInfo,
            pAllocator,
            pInstance=None,
        )
        
        throws exception on failure
    """
    try:
        return vkCreateInstance(createInfo, None)
    except:
        logger.error("Failed to create Instance!")
        return None