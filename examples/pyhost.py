from popsicle import juce_gui_basics, juce_audio_utils
from popsicle import juce, juce_multi, START_JUCE_APPLICATION
import cppyy


class MainWindow(juce.DocumentWindow):
    def __init__(self):
        super().__init__(juce.JUCEApplication.getInstance().getApplicationName(),
                         juce.Colours.black,
                         juce.DocumentWindow.allButtons,
                         True)

        path = "/Library/Audio/Plug-Ins/Components/ANA2.component"

        # 1 - Get plugin description from plugin file
        pdArray = juce.OwnedArray[juce.PluginDescription]()
        auPluginFormat = juce.AudioUnitPluginFormat()
        auPluginFormat.findAllTypesForFile(pdArray, path)
        desc = pdArray.getFirst()

        if pdArray.size() == 0:
            print("Failed to read plugin description")
            juce.JUCEApplication.getInstance().systemRequestedQuit()
            return

        # 2 - Instantiate plugin from plugin description
        error = juce.String()
        fm = juce.AudioPluginFormatManager()
        fm.addDefaultFormats()
        plugin_instance = fm.createPluginInstance(desc, 44100, 512, error)

        if plugin_instance is None:
            print("Failed to instantiate plugin: " + error)
            juce.JUCEApplication.getInstance().systemRequestedQuit()
            return

        # 3 - Create Plugin View
        self.component = plugin_instance.createEditorIfNeeded()
        self.setResizable(True, True)
        self.setContentOwned(self.component, True)
        self.setVisible(True)

    def __del__(self):
        if hasattr(self, "component"):
            del self.component

    def closeButtonPressed(self):
        self.clearContentComponent()
        juce.JUCEApplication.getInstance().systemRequestedQuit()


class Application(juce.JUCEApplication):
    def getApplicationName(self):
        return "PyHost"

    def getApplicationVersion(self):
        return "0.1"

    def initialise(self, commandLine):
        self.window = MainWindow()

    def shutdown(self):
        if hasattr(self, "window"):
            del self.window

if __name__ == "__main__":
    START_JUCE_APPLICATION(Application)
