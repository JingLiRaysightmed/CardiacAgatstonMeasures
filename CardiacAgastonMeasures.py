from __main__ import vtk, qt, ctk, slicer
import SimpleITK as sitk
import sitkUtils as su

#
# CardiacAgastonMeasures
#

class CardiacAgastonMeasures:
    def __init__(self, parent):
        parent.title = "Cardiac Agaston Measures"
        parent.categories = ["Cardiac Agaston Measures"]
        parent.dependencies = []
        parent.contributors = ["Jessica Forbes (SINAPSE)",
                               "Hans Johnson (SINAPSE)"]
        parent.helpText = """
                                   This module will auto-segment the calcium deposits in Cardiac CT scans.  The user selects calcium clusters that represent calcium plaques.  The user then selects calcium clusters that do not represent calcium plaques and that should not be included in the final calculations.  Slicer will take the mean, peak, variance, mass and threshold and put the values into an Excel (or Excel compatible) file.
                                   """
        parent.acknowledgementText = """
                                   This file was originally developed by Jessica Forbes and Hans Johnson of the SINAPSE Lab at the University of Iowa.""" # replace with organization, grant and thanks.
        self.parent = parent

#
# CardiacAgastonMeasuresWidget
#

class CardiacAgastonMeasuresWidget:
    def __init__(self, parent = None):
        self.currentRegistrationInterface = None
        self.thresholdValue = 130
        if not parent:
            self.parent = slicer.qMRMLWidget()
            self.parent.setLayout(qt.QVBoxLayout())
            self.parent.setMRMLScene(slicer.mrmlScene)
        else:
            self.parent = parent
        self.layout = self.parent.layout()
        if not parent:
            self.setup()
            self.parent.show()

    def setup(self):
        # Instantiate and connect widgets ...
        
        #
        # Reload and Test area
        #
        if True:
            """Developer interface"""
            reloadCollapsibleButton = ctk.ctkCollapsibleButton()
            reloadCollapsibleButton.text = "Advanced - Reload && Test"
            reloadCollapsibleButton.collapsed = False
            self.layout.addWidget(reloadCollapsibleButton)
            reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)
            
            # reload button
            # (use this during development, but remove it when delivering
            #  your module to users)
            self.reloadButton = qt.QPushButton("Reload")
            self.reloadButton.toolTip = "Reload this module."
            self.reloadButton.name = "CardiacAgastonMeasures Reload"
            reloadFormLayout.addWidget(self.reloadButton)
            #self.reloadButton.connect('clicked(bool)',self.onHelloWorldButtonClicked)
            self.reloadButton.connect('clicked()', self.onReload)
        
        
        # Collapsible button
        self.measuresCollapsibleButton = ctk.ctkCollapsibleButton()
        self.measuresCollapsibleButton.text = "Cardiac Agaston Measures"
        self.layout.addWidget(self.measuresCollapsibleButton)
        
        # Layout within the sample collapsible button
        self.measuresFormLayout = qt.QFormLayout(self.measuresCollapsibleButton)

        # The Input Volume Selector
        self.inputFrame = qt.QFrame(self.measuresCollapsibleButton)
        self.inputFrame.setLayout(qt.QHBoxLayout())
        self.measuresFormLayout.addRow(self.inputFrame)
        self.inputSelector = qt.QLabel("Input Volume: ", self.inputFrame)
        self.inputFrame.layout().addWidget(self.inputSelector)
        self.inputSelector = slicer.qMRMLNodeComboBox(self.inputFrame)
        self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
        self.inputSelector.addEnabled = False
        self.inputSelector.removeEnabled = False
        self.inputSelector.setMRMLScene( slicer.mrmlScene )
        self.inputFrame.layout().addWidget(self.inputSelector)

        # Threshold button
        thresholdButton = qt.QPushButton("Threshold Volume")
        thresholdButton.toolTip = "Threshold the selected Input Volume"
        self.measuresFormLayout.addRow(thresholdButton)
        thresholdButton.connect('clicked(bool)', self.onThresholdButtonClicked)

        # The Input Left Main (LM) Label Selector
        self.LMFrame = qt.QFrame(self.measuresCollapsibleButton)
        self.LMFrame.setLayout(qt.QHBoxLayout())
        self.measuresFormLayout.addRow(self.LMFrame)
        self.LMSelector = qt.QLabel("Label - Left Main (LM):\t\t", self.LMFrame)
        self.LMFrame.layout().addWidget(self.LMSelector)
        self.LMSelector = slicer.qMRMLNodeComboBox(self.LMFrame)
        self.LMSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
        self.LMSelector.addEnabled = False
        self.LMSelector.removeEnabled = False
        self.LMSelector.setMRMLScene( slicer.mrmlScene )
        self.LMFrame.layout().addWidget(self.LMSelector)

        # The Input Left Arterial Descending (LAD) Label Selector
        self.LADFrame = qt.QFrame(self.measuresCollapsibleButton)
        self.LADFrame.setLayout(qt.QHBoxLayout())
        self.measuresFormLayout.addRow(self.LADFrame)
        self.LADSelector = qt.QLabel("Label - Left Arterial Descending (LAD):\t", self.LADFrame)
        self.LADFrame.layout().addWidget(self.LADSelector)
        self.LADSelector = slicer.qMRMLNodeComboBox(self.LADFrame)
        self.LADSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
        self.LADSelector.addEnabled = False
        self.LADSelector.removeEnabled = False
        self.LADSelector.setMRMLScene( slicer.mrmlScene )
        self.LADFrame.layout().addWidget(self.LADSelector)

        # The Input Left Circumflex (LCX) Label Selector
        self.LCXFrame = qt.QFrame(self.measuresCollapsibleButton)
        self.LCXFrame.setLayout(qt.QHBoxLayout())
        self.measuresFormLayout.addRow(self.LCXFrame)
        self.LCXSelector = qt.QLabel("Label - Left Circumflex (LCX):\t\t", self.LCXFrame)
        self.LCXFrame.layout().addWidget(self.LCXSelector)
        self.LCXSelector = slicer.qMRMLNodeComboBox(self.LCXFrame)
        self.LCXSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
        self.LCXSelector.addEnabled = False
        self.LCXSelector.removeEnabled = False
        self.LCXSelector.setMRMLScene( slicer.mrmlScene )
        self.LCXFrame.layout().addWidget(self.LCXSelector)

        # The Input Left Circumflex (RCA) Label Selector
        self.RCAFrame = qt.QFrame(self.measuresCollapsibleButton)
        self.RCAFrame.setLayout(qt.QHBoxLayout())
        self.measuresFormLayout.addRow(self.RCAFrame)
        self.RCASelector = qt.QLabel("Label - Right Coronary Artery (RCA):\t", self.RCAFrame)
        self.RCAFrame.layout().addWidget(self.RCASelector)
        self.RCASelector = slicer.qMRMLNodeComboBox(self.RCAFrame)
        self.RCASelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
        self.RCASelector.addEnabled = False
        self.RCASelector.removeEnabled = False
        self.RCASelector.setMRMLScene( slicer.mrmlScene )
        self.RCAFrame.layout().addWidget(self.RCASelector)
        
        # Add vertical spacer
        self.layout.addStretch(1)
        
        # Set local var as instance attribute
        self.thresholdButton = thresholdButton

    def onThresholdButtonClicked(self):
        print "Thresholding at {0}".format(self.thresholdValue)
        qt.QMessageBox.information( slicer.util.mainWindow(), 'Slicer Python', 'Thresholding at {0}'.format(self.thresholdValue))
        inputVolumeName = su.PullFromSlicer(self.inputSelector.currentNode().GetName())
        thresholdImage = sitk.BinaryThreshold(inputVolumeName, self.thresholdValue, 2000)
        castedThresholdImage = sitk.Cast(thresholdImage, sitk.sitkInt16)
        su.PushLabel(castedThresholdImage,'calcium')

    def onReload(self,moduleName="CardiacAgastonMeasures"):
        """Generic reload method for any scripted module.
            ModuleWizard will subsitute correct default moduleName.
            Note: customized for use in LandmarkRegistration
            """
        import imp, sys, os, slicer
        import SimpleITK as sitk
        import sitkUtils as su

        # first, destroy the current plugin, since it will
        # contain subclasses of the RegistrationLib modules
        if self.currentRegistrationInterface:
            self.currentRegistrationInterface.destroy()

        # now reload the RegistrationLib source code
        # - set source file path
        # - load the module to the global space
        filePath = eval('slicer.modules.%s.path' % moduleName.lower())
        p = os.path.dirname(filePath)
        if not sys.path.__contains__(p):
            sys.path.insert(0,p)
        for subModuleName in ("pqWidget", "Visualization", "Landmarks", ):
            fp = open(filePath, "r")
            globals()[subModuleName] = imp.load_module(subModuleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
            fp.close()

        # # now reload all the support code and have the plugins
        # # re-register themselves with slicer
        # oldPlugins = slicer.modules.registrationPlugins
        # slicer.modules.registrationPlugins = {}
        # for plugin in oldPlugins.values():
        #     pluginModuleName = plugin.__module__.lower()
        #     if hasattr(slicer.modules,pluginModuleName):
        #         # for a plugin from an extension, need to get the source path
        #         # from the module
        #         module = getattr(slicer.modules,pluginModuleName)
        #         sourceFile = module.path
        #     else:
        #         # for a plugin built with slicer itself, the file path comes
        #         # from the pyc path noted as __file__ at startup time
        #         sourceFile = plugin.sourceFile.replace('.pyc', '.py')
        #     imp.load_source(plugin.__module__, sourceFile)
        # oldPlugins = None

        widgetName = moduleName + "Widget"

        # now reload the widget module source code
        # - set source file path
        # - load the module to the global space
        filePath = eval('slicer.modules.%s.path' % moduleName.lower())
        p = os.path.dirname(filePath)
        if not sys.path.__contains__(p):
            sys.path.insert(0,p)
        fp = open(filePath, "r")
        globals()[moduleName] = imp.load_module(
            moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
        fp.close()

        # rebuild the widget
        # - find and hide the existing widget
        # - create a new widget in the existing parent
        parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
        for child in parent.children():
          try:
            child.hide()
          except AttributeError:
            pass
        # Remove spacer items
        item = parent.layout().itemAt(0)
        while item:
          parent.layout().removeItem(item)
          item = parent.layout().itemAt(0)

        # # delete the old widget instance
        # if hasattr(globals()['slicer'].modules, widgetName):
        #   getattr(globals()['slicer'].modules, widgetName).cleanup()

        # create new widget inside existing parent
        globals()[widgetName.lower()] = eval(
            'globals()["%s"].%s(parent)' % (moduleName, widgetName))
        globals()[widgetName.lower()].setup()
        setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])

