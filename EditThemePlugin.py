"""
EditThemePlugin for DearPyGui

A plugin that allows users to create, edit, save, and load custom themes
for DearPyGui applications. Themes are stored as .ini files in the themes/ folder.
"""

import dearpygui.dearpygui as dpg
import configparser
import os


class EditThemePlugin():
    """A DearPyGui plugin for editing and managing themes."""

    def __init__(self):
        """Initialize the theme plugin and create the UI."""
        self.confParser = configparser.ConfigParser()
        self._create_folders()
        self.all_saved_colors()
        self._create_UI()

    def _create_folders(self):
        """Create the themes folder and default theme file if they don't exist."""
        if not os.path.exists('themes'):
            os.mkdir('themes')
        if not os.path.exists('themes/default.ini'):
            self.createDefaultTheme()

    def _create_UI(self):
        """Create the theme UI and load the default theme."""
        dpg.add_theme(tag="glob")
        self.createMenu()
        self.loadAll(None, {"file_path_name": 'themes/default.ini'})

    def __str__(self) -> str:
        """Return the theme tag identifier."""
        return "glob"

    def createTheme(self):
        """Create and bind a theme with all configured colors."""
        with dpg.theme_component(dpg.mvAll, parent="glob"):
            self._add_theme_colors()
        dpg.bind_theme("glob")

    def createDefaultTheme(self):
        """Create a default theme configuration and save it to themes/default.ini."""
        self.confParser['Theme'] = {}
        self.confParser['Theme']['mvthemecol_text'] = "255.0, 254.99607849121094, 254.99607849121094, 255.0"
        self.confParser['Theme']['mvthemecol_tabactive'] = "177.51373291015625, 26.478431701660156, 26.48627471923828, 255.0"
        self.confParser['Theme']['mvthemecol_slidergrabactive'] = "249.0, 66.0, 72.062744140625, 255.0"
        self.confParser['Theme']['mvthemecol_textdisabled'] = "127.0, 127.0, 127.0, 255.0"
        self.confParser['Theme']['mvthemecol_tabunfocused'] = "53.53333282470703, 22.77254867553711, 22.776470184326172, 247.0"
        self.confParser['Theme']['mvthemecol_button'] = "123.97647094726562, 0.6823529601097107, 0.6901960968971252, 255.0"
        self.confParser['Theme']['mvthemecol_windowbg'] = "12.678431510925293, 12.607843399047852, 12.607843399047852, 239.0"
        self.confParser['Theme']['mvthemecol_tabunfocusedactive'] = "107.0, 35.0, 35.00392150878906, 255.0"
        self.confParser['Theme']['mvthemecol_buttonhovered'] = "231.04705810546875, 17.870588302612305, 24.937253952026367, 255.0"
        self.confParser['Theme']['mvthemecol_childbg'] = "0.0, 0.0, 0.0, 26.764705657958984"
        self.confParser['Theme']['mvthemecol_dockingpreview'] = "249.0, 66.0, 66.00784301757812, 178.0"
        self.confParser['Theme']['mvthemecol_buttonactive'] = "249.0, 15.0, 15.011764526367188, 255.0"
        self.confParser['Theme']['mvthemecol_border'] = "109.0, 109.0, 127.0, 127.0"
        self.confParser['Theme']['mvthemecol_dockingemptybg'] = "51.0, 51.0, 51.0, 255.0"
        self.confParser['Theme']['mvthemecol_header'] = "249.0, 66.0, 66.00784301757812, 79.0"
        self.confParser['Theme']['mvthemecol_popupbg'] = "20.0, 20.0, 20.0, 239.0"
        self.confParser['Theme']['mvthemecol_plotlines'] = "155.0, 155.0, 155.0, 255.0"
        self.confParser['Theme']['mvthemecol_headerhovered'] = "249.0, 66.0, 66.00784301757812, 204.0"
        self.confParser['Theme']['mvthemecol_bordershadow'] = "0.0, 0.0, 0.0, 0.0"
        self.confParser['Theme']['mvthemecol_plotlineshovered'] = "255.0, 109.0, 89.0, 255.0"
        self.confParser['Theme']['mvthemecol_headeractive'] = "249.0, 66.0, 66.00784301757812, 255.0"
        self.confParser['Theme']['mvthemecol_framebg'] = "82.19215393066406, 83.32157135009766, 84.52941131591797, 137.0"
        self.confParser['Theme']['mvthemecol_plothistogram'] = "229.0, 178.0, 0.0, 255.0"
        self.confParser['Theme']['mvthemecol_separator'] = "109.0, 109.0, 127.0, 127.0"
        self.confParser['Theme']['mvthemecol_framebghovered'] = "249.0, 66.0, 66.00784301757812, 102.0"
        self.confParser['Theme']['mvthemecol_plothistogramhovered'] = "255.0, 153.0, 0.0, 255.0"
        self.confParser['Theme']['mvthemecol_separatorhovered'] = "191.0, 24.713726043701172, 24.713726043701172, 200.0"
        self.confParser['Theme']['mvthemecol_framebgactive'] = "255.0, 0.0, 0.0117647061124444, 195.82745361328125"
        self.confParser['Theme']['mvthemecol_tableheaderbg'] = "48.0, 48.0, 51.0, 255.0"
        self.confParser['Theme']['mvthemecol_separatoractive'] = "191.0, 25.0, 25.007843017578125, 255.0"
        self.confParser['Theme']['mvthemecol_titlebg'] = "10.0, 10.0, 10.0, 255.0"
        self.confParser['Theme']['mvthemecol_tableborderstrong'] = "79.0, 79.0, 89.0, 255.0"
        self.confParser['Theme']['mvthemecol_resizegrip'] = "249.0, 66.0, 66.00784301757812, 51.0"
        self.confParser['Theme']['mvthemecol_titlebgactive'] = "122.0, 40.0, 40.00392150878906, 255.0"
        self.confParser['Theme']['mvthemecol_tableborderlight'] = "67.67058563232422, 67.67058563232422, 76.07450866699219, 255.0"
        self.confParser['Theme']['mvthemecol_resizegriphovered'] = "249.0, 66.0, 66.00784301757812, 170.0"
        self.confParser['Theme']['mvthemecol_titlebgcollapsed'] = "0.0, 0.0, 0.0, 130.0"
        self.confParser['Theme']['mvthemecol_tablerowbg'] = "0.0, 0.0, 0.0, 0.0"
        self.confParser['Theme']['mvthemecol_resizegripactive'] = "236.68235778808594, 36.61176300048828, 36.62352752685547, 242.0"
        self.confParser['Theme']['mvthemecol_menubarbg'] = "35.0, 35.0, 35.0, 255.0"
        self.confParser['Theme']['mvthemecol_tablerowbgalt'] = "255.0, 255.0, 255.0, 15.0"
        self.confParser['Theme']['mvthemecol_tab'] = "147.0, 44.99607849121094, 45.00392150878906, 219.0"
        self.confParser['Theme']['mvthemecol_scrollbarbg'] = "5.0, 5.0, 5.0, 135.0"
        self.confParser['Theme']['mvthemecol_textselectedbg'] = "249.0, 66.0, 114.52941131591797, 89.0"
        self.confParser['Theme']['mvthemecol_tabhovered'] = "249.0, 66.0, 66.00784301757812, 204.0"
        self.confParser['Theme']['mvthemecol_scrollbargrab'] = "79.0, 79.0, 79.0, 255.0"
        self.confParser['Theme']['mvthemecol_dragdroptarget'] = "255.0, 255.0, 0.0, 229.0"
        self.confParser['Theme']['mvthemecol_scrollbargrabhovered'] = "104.0, 104.0, 104.0, 255.0"
        self.confParser['Theme']['mvthemecol_navhighlight'] = "249.0, 66.0, 66.00784301757812, 255.0"
        self.confParser['Theme']['mvthemecol_scrollbargrabactive'] = "130.0, 130.0, 130.0, 255.0"
        self.confParser['Theme']['mvthemecol_navwindowinghighlight'] = "255.0, 255.0, 255.0, 178.0"
        self.confParser['Theme']['mvthemecol_checkmark'] = "249.0, 66.0, 66.00784301757812, 255.0"
        self.confParser['Theme']['mvthemecol_navwindowingdimbg'] = "204.0, 204.0, 204.0, 51.0"
        self.confParser['Theme']['mvthemecol_slidergrab'] = "224.0, 60.99607849121094, 61.007843017578125, 255.0"
        self.confParser['Theme']['mvthemecol_modalwindowdimbg'] = "204.0, 204.0, 204.0, 89.0"
        with open('themes/default.ini', 'w') as f: 
            self.confParser.write(f, True)
        return

    def createMenu(self):
        pluginMenu = dpg.add_menu(label="Theme")
        self.loadTheme()
        self.saveTheme()
        self.editTheme()
        dpg.add_menu_item(label="Configure Theme", callback=lambda: dpg.configure_item('editThemeWindow', show=True), parent=pluginMenu)
        dpg.add_menu_item(label="Load Theme", callback=lambda: dpg.configure_item("loadThemeFileSelector", show=True), parent=pluginMenu)
        dpg.add_menu_item(label="Save Theme", callback=lambda: dpg.configure_item("saveThemeFileSelector", show=True), parent=pluginMenu)

    def editTheme(self):
        """Create the theme editor window with color editing controls for all theme colors."""
        dpg.add_window(tag="editThemeWindow", show=False, autosize=True, no_title_bar=True, max_size=[1080, 720])
        dpg.add_button(parent="editThemeWindow", label="Close", callback=self._close_edit_window)
        dpg.add_button(label="Load Theme", callback=self._show_load_dialog, parent="editThemeWindow")
        dpg.add_button(label="Save Theme", callback=self._show_save_dialog, parent="editThemeWindow")
        
        # Create color editors for each theme color
        for color_name in self.theColors:
            self._create_color_editor(color_name)
    
    def loadAll(self, a=None, sentFileDict=None):
        try:
            self.confParser.read(sentFileDict["file_path_name"])
            dpg.delete_item("editThemeWindow")
            self.createTheme()
            self.editTheme()
        except Exception as e:
            print(f"Error loading theme: {e}")
            return

        
    
    def loadTheme(self):
        try:
            with dpg.file_dialog(callback=self.loadAll, directory_selector=False, width=700, height=400, default_path="themes", default_filename="default.ini", show=False, tag="loadThemeFileSelector", cancel_callback=doNothing):
                dpg.add_file_extension(".ini")
        except Exception as e:
            print(f"Error creating load theme dialog: {e}")
            return
    
    def saveTheme(self):
        try:
            with dpg.file_dialog(default_path="themes", default_filename=".ini", callback=self.saveAll, directory_selector=False, width=700, height=400, show=False, tag="saveThemeFileSelector", cancel_callback=doNothing):
                dpg.add_file_extension(".ini")
                dpg.add_button(label="save")
        except Exception as e:
            print(f"Error creating save theme dialog: {e}")
            return

    def saveAll(self, a, b):
        if "file_path_name" not in b:
            return
        try:
            self._save_theme_colors()
            with open(b["file_path_name"], 'w') as f:
                self.confParser.write(f, True)
        except Exception as e:
            print(f"Error saving theme: {e}")
            return

    def getThemeColor(self, themeCol):
        try:
            itm = self.confParser['Theme'][themeCol]
            itm = itm.removeprefix('[')
            itm = itm.removesuffix(']')
            thrIntAsStr = itm
            a = thrIntAsStr.split(',')
            return (int(float(a[0].strip())), int(float(a[1].strip())), int(float(a[2].strip())), int(float(a[3].strip())))
        except (KeyError, ValueError, IndexError) as e:
            print(f"Error parsing theme color for {themeCol}: {e}")
            return (255, 255, 255, 255)


    def _add_theme_colors(self):
        """Add theme colors using DearPyGui API directly, avoiding exec()."""
        for color_name in self.theColors:
            try:
                color_constant = getattr(dpg, color_name, None)
                if color_constant is None:
                    continue
                color_value = self.getThemeColor(color_name)
                dpg.add_theme_color(color_constant, color_value, category=dpg.mvThemeCat_Core)
            except Exception as e:
                print(f"Error adding theme color for {color_name}: {e}")

    def _save_theme_colors(self):
        """Save current theme colors from color edit widgets to config."""
        for color_name in self.theColors:
            try:
                widget_id = f"colEdit{color_name}"
                if dpg.does_item_exist(widget_id):
                    value = dpg.get_value(widget_id)
                    if "Theme" not in self.confParser:
                        self.confParser["Theme"] = {}
                    self.confParser["Theme"][color_name] = str(value)
            except Exception as e:
                print(f"Error saving theme color for {color_name}: {e}")

    def _create_color_editor(self, color_name):
        """Create a color editor widget for a specific theme color."""
        try:
            color_value = self.getThemeColor(color_name)
            tag = f"colEdit{color_name}"
            
            def on_color_change():
                """Callback when color is changed."""
                try:
                    color_constant = getattr(dpg, color_name, None)
                    if color_constant is None:
                        return
                    new_value = dpg.get_value(tag)
                    dpg.add_theme_color(
                        color_constant,
                        new_value,
                        parent=dpg.add_theme_component(dpg.mvAll, parent="glob")
                    )
                    dpg.bind_theme("glob")
                except Exception as e:
                    print(f"Error updating color {color_name}: {e}")
            
            dpg.add_color_edit(
                color_value,
                source=self.confParser['Theme'].get(color_name, "255, 255, 255, 255"),
                display_type=dpg.mvColorEdit_uint8,
                alpha_bar=True,
                alpha_preview=dpg.mvColorEdit_AlphaPreviewHalf,
                tag=tag,
                parent='editThemeWindow',
                label=color_name,
                callback=on_color_change
            )
        except Exception as e:
            print(f"Error creating color editor for {color_name}: {e}")

    def _close_edit_window(self):
        """Close the edit theme window."""
        dpg.configure_item("editThemeWindow", show=False)

    def _show_load_dialog(self):
        """Show the load theme file dialog."""
        dpg.configure_item("loadThemeFileSelector", show=True)

    def _show_save_dialog(self):
        """Show the save theme file dialog."""
        dpg.configure_item("saveThemeFileSelector", show=True)


    def all_saved_colors(self):
        self.theColors = [
            "mvThemeCol_Text",
            "mvThemeCol_TextSelectedBg",
            "mvThemeCol_TextDisabled",
            "mvThemeCol_TabActive",
            "mvThemeCol_TabUnfocused",
            "mvThemeCol_TabUnfocusedActive",
            "mvThemeCol_TabHovered",
            "mvThemeCol_Tab",
            "mvThemeCol_Button",
            "mvThemeCol_ButtonHovered",
            "mvThemeCol_ButtonActive",
            "mvThemeCol_WindowBg",
            "mvThemeCol_ChildBg",
            "mvThemeCol_PopupBg",
            "mvThemeCol_FrameBg",
            "mvThemeCol_FrameBgHovered",
            "mvThemeCol_FrameBgActive",
            "mvThemeCol_TitleBg",
            "mvThemeCol_TitleBgActive",
            "mvThemeCol_TitleBgCollapsed",
            "mvThemeCol_MenuBarBg",
            "mvThemeCol_DockingEmptyBg",
            "mvThemeCol_ScrollbarBg",
            "mvThemeCol_ResizeGripActive",
            "mvThemeCol_ScrollbarGrab",
            "mvThemeCol_ScrollbarGrabHovered",
            "mvThemeCol_ScrollbarGrabActive",
            "mvThemeCol_Border",
            "mvThemeCol_BorderShadow",
            "mvThemeCol_SliderGrabActive",
            "mvThemeCol_DockingPreview",
            "mvThemeCol_Header",
            "mvThemeCol_PlotLines",
            "mvThemeCol_HeaderHovered",
            "mvThemeCol_PlotLinesHovered",
            "mvThemeCol_HeaderActive",
            "mvThemeCol_PlotHistogram",
            "mvThemeCol_Separator",
            "mvThemeCol_PlotHistogramHovered",
            "mvThemeCol_SeparatorHovered",
            "mvThemeCol_TableHeaderBg",
            "mvThemeCol_SeparatorActive",
            "mvThemeCol_TableBorderStrong",
            "mvThemeCol_ResizeGrip",
            "mvThemeCol_TableBorderLight",
            "mvThemeCol_ResizeGripHovered",
            "mvThemeCol_TableRowBg",
            "mvThemeCol_TableRowBgAlt",
            "mvThemeCol_DragDropTarget",
            "mvThemeCol_NavHighlight",
            "mvThemeCol_NavWindowingHighlight",
            "mvThemeCol_CheckMark",
            "mvThemeCol_NavWindowingDimBg",
            "mvThemeCol_SliderGrab",
            "mvThemeCol_ModalWindowDimBg",
        ]

def doNothing(*args):
    """Placeholder callback function for canceled file dialogs."""
    return

if __name__=="__main__":
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=1200, height=800)
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll) as gtc:
            dpg.add_theme_color(dpg.mvThemeCol_Text,                    (0,0,0,255),                        category=dpg.mvThemeCat_Core, tag="globcolor")
    dpg.bind_theme(global_theme)
    def bind():
        dpg.add_theme_color(dpg.mvThemeCol_Text, dpg.get_value("ve"), parent=dpg.add_theme_component(dpg.mvAll, parent="glob"))
        dpg.bind_theme("glob")
    with dpg.window(tag="main", show=False):
        dpg.add_color_edit(parent="main",tag='ve', callback=bind)
        dpg.add_text(dpg.get_item_info("main"), wrap=0)
        dpg.add_text(dpg.get_app_configuration(), wrap=0)
    with dpg.value_registry():
        dpg.add_color_value(source="ve", tag="vete")
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
            dpg.add_menu_item(label="Show About",             callback=lambda:dpg.show_tool(dpg.mvTool_About))
            dpg.add_menu_item(label="Show Metrics",         callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
            dpg.add_menu_item(label="Show Documentation",     callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
            dpg.add_menu_item(label="Show Debug",             callback=lambda:dpg.show_tool(dpg.mvTool_Debug))
            dpg.add_menu_item(label="Show Style Editor",     callback=lambda:dpg.show_tool(dpg.mvTool_Style))
            dpg.add_menu_item(label="Show Font Manager",     callback=lambda:dpg.show_tool(dpg.mvTool_Font))
            dpg.add_menu_item(label="Show Item Registry",     callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))
        EditThemePlugin()
    dpg.set_primary_window("main2", True)
    dpg.setup_dearpygui()

    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()