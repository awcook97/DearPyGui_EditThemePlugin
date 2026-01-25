"""
ChooseFontsPlugin Module

This plugin provides a font selection interface for DearPyGui applications.
It allows users to browse, preview, and apply custom fonts (.ttf, .otf) to the entire application.
The plugin includes support for system fonts (Windows), user fonts, and font size/scale configuration.
Font selections are persisted to disk for automatic restoration on application restart.
"""

import dearpygui.dearpygui as dpg
import os
import logging

logger = logging.getLogger(__name__)


class ChooseFontsPlugin():
    """
    A plugin for managing and applying custom fonts in DearPyGui applications.
    
    This class provides functionality to:
    - Discover and load custom fonts from the Fonts directory
    - Load system fonts from Windows font directories
    - Display a UI for font selection, size, and scale configuration
    - Persist font preferences to disk
    """

    def __init__(self):
        """
        Initialize the ChooseFontsPlugin.
        
        Sets up the font registry, creates necessary directories and files,
        builds the font library, and creates the UI components.
        """
        self.ignore = 'NO CUSTOM FONT, IGNORE'
        self.font_registry = dpg.add_font_registry()
        self.fontDict = dict()
        self.create_folders()
        self.create_font_library()
        self.create_font_window()
        self.create_font_menu()

    def create_folders(self):
        """
        Create necessary directories and configuration files for font management.
        
        Creates a Fonts directory and initializes three configuration files:
        - USERFONT: stores the currently selected font name
        - USERSIZE: stores the current font size
        - USERSCALE: stores the current font scale
        """
        if not os.path.exists('Fonts'):
            os.mkdir('Fonts')
        if not os.path.exists('Fonts/USERFONT'):
            with open('Fonts/USERFONT', 'w') as f:
                f.write(self.ignore)
        if not os.path.exists('Fonts/USERSIZE'):
            with open('Fonts/USERSIZE', 'w') as f:
                f.write("16")
        if not os.path.exists('Fonts/USERSCALE'):
            with open('Fonts/USERSCALE', 'w') as f:
                f.write("1")

    def create_font_library(self):
        """
        Build the font library by scanning for available fonts.
        
        Loads user font preferences from configuration files and searches for fonts in:
        - The Fonts directory (user-provided fonts)
        - Windows system fonts (if available)
        
        Initializes the font registry with found fonts and applies the saved user font settings.
        """
        with open('Fonts/USERFONT', 'r') as f:
            self.userFont = f.read()
            if not self.userFont:
                self.userFont = self.ignore
        with open('Fonts/USERSIZE', 'r') as f:
            try:
                self.userSize = int(f.read())
            except ValueError as e:
                logger.warning(f"Failed to parse user font size: {e}. Using default size 16.")
                self.userSize = 16
            if not self.userSize:
                self.userSize = 16
        with open('Fonts/USERSCALE', 'r') as f:
            try:
                self.userScale = float(f.read())
            except ValueError as e:
                logger.warning(f"Failed to parse user font scale: {e}. Using default scale 1.0.")
                self.userScale = 1
            if not self.userScale:
                self.userScale = 1
        self.fontDict["YOUR FONTS"] = None
        for filename in os.listdir('Fonts'):
            if filename.endswith((".ttf", "otf")):
                self.fontDict[filename] = f"Fonts/{filename}"
                with dpg.font(self.fontDict[filename], 16, parent=self.font_registry) as f:
                    dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                    dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
                    dpg.add_font_range(0x0, 0xF)
                    dpg.add_font_range(0x00, 0xFF)
                    dpg.add_font_range(0x000, 0xFFF)
                    dpg.add_font_range(0x0000, 0xFFFF)
        self.fontDict["WINDOWS FONTS"] = None
        try:
            for filename in os.listdir('C:\\Windows\\Fonts'):
                if filename.endswith((".ttf", "otf")):
                    self.fontDict[filename] = f"C:\\Windows\\Fonts\\{filename}"
        except FileNotFoundError:
            logger.debug("Windows Fonts directory not found. Skipping system fonts.")
            self.fontDict.pop("WINDOWS FONTS")
        if len(self.fontDict) > 0:
            if self.userFont in self.fontDict:
                dpg.add_font(self.fontDict[self.userFont], size=self.userSize, parent=self.font_registry, tag="fntCFPNewFont")
                dpg.add_font_chars([0x2013, 0x2014, 0x2015, 0x2017, 0x2018, 0x2019, 0x201A, 0x201B, 0x201C, 0x201D, 0x201E, 0x2020, 0x2021, 0x2022, 0x2026, 0x2030, 0x2032, 0x2033, 0x2039, 0x203A, 0x203C, 0x203E, 0x2044, 0x204A], parent="fntCFPNewFont")
                dpg.bind_font("fntCFPNewFont")

    def create_font_window(self):
        """
        Create the UI window for font selection and configuration.
        
        Provides controls for:
        - Font type selection via dropdown
        - Font size adjustment
        - Font scale slider
        - Font preview area
        - Autosize checkbox
        - Buttons for changing, saving, and resetting fonts
        """
        with dpg.window(label="Font Menu", width=400, height=400, show=False, tag="winCFPFontWindow", pos=(int(dpg.get_viewport_width() / 2 - 200), int(dpg.get_viewport_height() / 2 - 200))):
            with dpg.child_window(autosize_x=True, height=-120):
                dpg.add_text("This is the font window. To use it, find your Fonts folder, and put in any .ttf or .otf font, and they will show up here.", wrap=0)
                dpg.add_text("Whatever font you choose will be applied to the whole application. Sometimes it's best to close and reopen the application after setting a font, in case things get weird.", wrap=0)
                dpg.add_combo(list(self.fontDict.keys()), label="Font Type", callback=self.build_fonts, tag="cmbCFPFontType")
                dpg.add_input_int(label="Size", default_value=self.userSize, callback=self.build_fonts, tag="intCFPSize")
                dpg.add_slider_float(default_value=self.userScale, label="Scale", callback=self.build_fonts, tag="slideCFPFontScale", min_value=0.0, max_value=2.0, clamped=True)
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="Autosize?", tag="chkbxCFPAutosize", default_value=True)
                    dpg.add_button(label="Change Font", callback=self.btnBuild)

            with dpg.child_window(autosize_x=True, height=100):
                dpg.add_text("the quick brown fox jumped over the lazy dog", wrap=0)
                dpg.add_text("THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG", wrap=0)
            with dpg.group(horizontal=True):
                dpg.add_button(label="Close", callback=lambda: dpg.configure_item("winCFPFontWindow", show=False))
                dpg.add_button(label="Save", callback=self.save_fonts)
                dpg.add_button(label="Reset to Default (Your Saves Won't Be Changed)", callback=lambda: dpg.bind_font("DEFAULT") and dpg.set_global_font_scale(1.0))

    def create_font_menu(self):
        """
        Create the Font menu in the menu bar.
        
        Adds a menu item to open the font selection window.
        """
        self.font_menu = dpg.add_menu(label="Font")
        dpg.add_menu_item(label="Edit", callback=lambda: dpg.configure_item("winCFPFontWindow", show=True), parent=self.font_menu)

    def btnBuild(self):
        """
        Build fonts with autosize temporarily enabled.
        
        This method temporarily enables autosize to rebuild fonts with new settings,
        then disables autosize again to prevent continuous updates.
        """
        dpg.set_value("chkbxCFPAutosize", True)
        self.build_fonts()
        dpg.set_value("chkbxCFPAutosize", False)

    def build_fonts(self):
        """
        Build and apply the selected font to the application.
        
        Only applies fonts if autosize is enabled. Loads the font from disk,
        configures font ranges and hints, binds the font to DearPyGui,
        and applies the font scale.
        
        If errors occur during font loading, logs the error for debugging.
        """
        if not dpg.get_value("chkbxCFPAutosize"):
            return
        self.userFont = dpg.get_value("cmbCFPFontType")
        self.userSize = dpg.get_value("intCFPSize")
        if self.userFont not in self.fontDict:
            return
        if not self.fontDict[self.userFont]:
            return
        try:
            if dpg.does_item_exist("fntCFPNewFont"):
                dpg.delete_item("fntCFPNewFont")
            newFont = dpg.add_font(self.fontDict[self.userFont], size=self.userSize, parent=self.font_registry, tag="fntCFPNewFont")
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent="fntCFPNewFont")
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent="fntCFPNewFont")
            dpg.add_font_chars([0x2013, 0x2014, 0x2015, 0x2017, 0x2018, 0x2019, 0x201A, 0x201B, 0x201C, 0x201D, 0x201E, 0x2020, 0x2021, 0x2022, 0x2026, 0x2030, 0x2032, 0x2033, 0x2039, 0x203A, 0x203C, 0x203E, 0x2044, 0x204A], parent="fntCFPNewFont")
            dpg.add_font_range(0x0, 0xF, parent="fntCFPNewFont")
            dpg.add_font_range(0x00, 0xFF, parent="fntCFPNewFont")
            dpg.add_font_range(0x000, 0xFFF, parent="fntCFPNewFont")
            dpg.add_font_range(0x0000, 0xFFFF, parent="fntCFPNewFont")
            dpg.bind_font(newFont)
            self.userScale = float(dpg.get_value("slideCFPFontScale"))
            dpg.set_global_font_scale(self.userScale)
        except Exception as e:
            logger.exception("Error building font")

    def save_fonts(self):
        """
        Save the current font settings to configuration files.
        
        Persists the current font selection, size, and scale to disk
        so they can be restored on the next application launch.
        Closes the font window after saving.
        """
        with open('Fonts/USERFONT', 'w') as f:
            f.write(str(self.userFont))
        with open('Fonts/USERSIZE', 'w') as f:
            f.write(str(self.userSize))
        with open('Fonts/USERSCALE', 'w') as f:
            f.write(str(self.userScale))
        dpg.configure_item("winCFPFontWindow", show=False)


if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=1200, height=800)
    dpg.show_debug()
    try:
        with dpg.window(tag="main2"):
            with dpg.child_window():
                dpg.add_text("This is text")
                dpg.add_button(tag="This is a button", label="THIS IS A BUTTON")
                dpg.add_checkbox(label="Check Box")
                with dpg.child_window(autosize_x=True, autosize_y=True):
                    with dpg.tab_bar():
                        with dpg.tab(label="THIS IS A TAB"):
                            with dpg.tree_node(label="THIS IS A TREE NODE"):
                                randListOfStuff = ['THIS', 'IS', 'A', 'LIST']
                                dpg.add_combo(randListOfStuff)
                                dpg.add_listbox(randListOfStuff)
        with dpg.viewport_menu_bar():
            with dpg.menu(label="Tools"):
                dpg.add_menu_item(label="Show About", callback=lambda: dpg.show_tool(dpg.mvTool_About))
                dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_tool(dpg.mvTool_Metrics))
                dpg.add_menu_item(label="Show Documentation", callback=lambda: dpg.show_tool(dpg.mvTool_Doc))
                dpg.add_menu_item(label="Show Debug", callback=lambda: dpg.show_tool(dpg.mvTool_Debug))
                dpg.add_menu_item(label="Show Style Editor", callback=lambda: dpg.show_tool(dpg.mvTool_Style))
                dpg.add_menu_item(label="Show Font Manager", callback=lambda: dpg.show_tool(dpg.mvTool_Font))
                dpg.add_menu_item(label="Show Item Registry", callback=lambda: dpg.show_tool(dpg.mvTool_ItemRegistry))
            myFonts = ChooseFontsPlugin()
    except Exception as e:
        logger.error(f"Failed to initialize application: {e}")
    dpg.set_primary_window("main2", True)
    dpg.setup_dearpygui()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
