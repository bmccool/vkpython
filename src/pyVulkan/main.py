from pyVulkan.config import *
from pyVulkan.instance import make_instance
from pyVulkan.vk_logging import make_debug_messenger

APPLICATION_NAME = "ID Tech 12"

class Engine:

    
    def __init__(self):

        
        #whether to print debug messages in functions
        self.debugMode = True

        #glfw window parameters
        self.width = 640
        self.height = 480

        logger.debug("Making a graphics engine")
        
        self.build_gflw_window()
        self.make_instance()
        self.make_debug_messenger()

    def build_gflw_window(self):

        #initialize glfw
        glfw.init()

        #no default rendering client, we'll hook vulkan up to the window later
        glfw.window_hint(GLFW_CONSTANTS.GLFW_CLIENT_API, GLFW_CONSTANTS.GLFW_NO_API)
        #resizing breaks the swapchain, we'll disable it for now
        glfw.window_hint(GLFW_CONSTANTS.GLFW_RESIZABLE, GLFW_CONSTANTS.GLFW_FALSE)
        
        #create_window(int width, int height, const char *title, GLFWmonitor *monitor, GLFWwindow *share)
        self.window = glfw.create_window(self.width, self.height, APPLICATION_NAME, None, None)
        if self.window is not None:
            logger.debug(f"Successfully made a glfw window called {APPLICATION_NAME}, width: {self.width}, height: {self.height}")
        else:
            logger.error("GLFW window creation failed")

    def make_instance(self):
        self.instance = make_instance(APPLICATION_NAME)

    def make_debug_messenger(self):
        if self.debugMode:
            self.debugMessenger = make_debug_messenger(self.instance)

    def close(self):

        logger.debug("Goodbye see you!\n")

        if self.debugMode:
            destruction_function = vkGetInstanceProcAddr(self.instance, "vkDestroyDebugReportCallbackEXT")
            """ def vkDestroyDebugReportCallbackEXT(instance, callback, pAllocator): """
            destruction_function(self.instance, self.debugMessenger, None)

        vkDestroyInstance(self.instance, None)

	    #terminate glfw
        glfw.terminate()

if __name__ == "__main__":

    graphicsEngine = Engine()

    graphicsEngine.close()