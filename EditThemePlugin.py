"""
EditThemePlugin — DearPyGui 2.x compatible theme editor.
Adapted from https://github.com/awcook97/DearPyGui_EditThemePlugin
"""
import dearpygui.dearpygui as dpg
import configparser
import os
import pathlib


# All themeable color constants
THEME_COLORS = [
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


def _do_nothing(*args):
    pass


class EditThemePlugin:
    def __init__(self, menu_parent=None):
        self.confParser = configparser.ConfigParser()
        self._themes_dir = pathlib.Path(__file__).parent.parent / "themes"
        self._create_folders()
        self._glob_tag = "glob_theme"
        self._create_ui(menu_parent)

    def _create_folders(self):
        self._themes_dir.mkdir(parents=True, exist_ok=True)
        default = self._themes_dir / "default.ini"
        if not default.exists():
            self._create_default_theme()

    def _create_ui(self, menu_parent):
        # Create the global theme
        if dpg.does_item_exist(self._glob_tag):
            dpg.delete_item(self._glob_tag)

        self._create_menu(menu_parent)
        self._load_all(sent_file=str(self._themes_dir / "default.ini"))

    def __str__(self) -> str:
        return self._glob_tag

    # ----- theme creation -----

    def _apply_theme(self):
        """Create and bind the theme from current confParser settings."""
        if dpg.does_item_exist(self._glob_tag):
            dpg.delete_item(self._glob_tag)

        with dpg.theme(tag=self._glob_tag):
            with dpg.theme_component(dpg.mvAll):
                for color_name in THEME_COLORS:
                    try:
                        color_val = self._get_theme_color(color_name)
                        color_const = getattr(dpg, color_name, None)
                        if color_const is not None:
                            dpg.add_theme_color(
                                color_const,
                                color_val,
                                category=dpg.mvThemeCat_Core,
                            )
                    except Exception:
                        pass
        dpg.bind_theme(self._glob_tag)

    def _create_default_theme(self):
        self.confParser["Theme"] = {
            "mvthemecol_text": "255.0, 254.99, 254.99, 255.0",
            "mvthemecol_tabactive": "177.51, 26.48, 26.49, 255.0",
            "mvthemecol_slidergrabactive": "249.0, 66.0, 72.06, 255.0",
            "mvthemecol_textdisabled": "127.0, 127.0, 127.0, 255.0",
            "mvthemecol_tabunfocused": "53.53, 22.77, 22.78, 247.0",
            "mvthemecol_button": "123.98, 0.68, 0.69, 255.0",
            "mvthemecol_windowbg": "12.68, 12.61, 12.61, 239.0",
            "mvthemecol_tabunfocusedactive": "107.0, 35.0, 35.0, 255.0",
            "mvthemecol_buttonhovered": "231.05, 17.87, 24.94, 255.0",
            "mvthemecol_childbg": "0.0, 0.0, 0.0, 26.76",
            "mvthemecol_dockingpreview": "249.0, 66.0, 66.01, 178.0",
            "mvthemecol_buttonactive": "249.0, 15.0, 15.01, 255.0",
            "mvthemecol_border": "109.0, 109.0, 127.0, 127.0",
            "mvthemecol_dockingemptybg": "51.0, 51.0, 51.0, 255.0",
            "mvthemecol_header": "249.0, 66.0, 66.01, 79.0",
            "mvthemecol_popupbg": "20.0, 20.0, 20.0, 239.0",
            "mvthemecol_plotlines": "155.0, 155.0, 155.0, 255.0",
            "mvthemecol_headerhovered": "249.0, 66.0, 66.01, 204.0",
            "mvthemecol_bordershadow": "0.0, 0.0, 0.0, 0.0",
            "mvthemecol_plotlineshovered": "255.0, 109.0, 89.0, 255.0",
            "mvthemecol_headeractive": "249.0, 66.0, 66.01, 255.0",
            "mvthemecol_framebg": "82.19, 83.32, 84.53, 137.0",
            "mvthemecol_plothistogram": "229.0, 178.0, 0.0, 255.0",
            "mvthemecol_separator": "109.0, 109.0, 127.0, 127.0",
            "mvthemecol_framebghovered": "249.0, 66.0, 66.01, 102.0",
            "mvthemecol_plothistogramhovered": "255.0, 153.0, 0.0, 255.0",
            "mvthemecol_separatorhovered": "191.0, 24.71, 24.71, 200.0",
            "mvthemecol_framebgactive": "255.0, 0.0, 0.01, 195.83",
            "mvthemecol_tableheaderbg": "48.0, 48.0, 51.0, 255.0",
            "mvthemecol_separatoractive": "191.0, 25.0, 25.01, 255.0",
            "mvthemecol_titlebg": "10.0, 10.0, 10.0, 255.0",
            "mvthemecol_tableborderstrong": "79.0, 79.0, 89.0, 255.0",
            "mvthemecol_resizegrip": "249.0, 66.0, 66.01, 51.0",
            "mvthemecol_titlebgactive": "122.0, 40.0, 40.0, 255.0",
            "mvthemecol_tableborderlight": "67.67, 67.67, 76.07, 255.0",
            "mvthemecol_resizegriphovered": "249.0, 66.0, 66.01, 170.0",
            "mvthemecol_titlebgcollapsed": "0.0, 0.0, 0.0, 130.0",
            "mvthemecol_tablerowbg": "0.0, 0.0, 0.0, 0.0",
            "mvthemecol_resizegripactive": "236.68, 36.61, 36.62, 242.0",
            "mvthemecol_menubarbg": "35.0, 35.0, 35.0, 255.0",
            "mvthemecol_tablerowbgalt": "255.0, 255.0, 255.0, 15.0",
            "mvthemecol_tab": "147.0, 45.0, 45.0, 219.0",
            "mvthemecol_scrollbarbg": "5.0, 5.0, 5.0, 135.0",
            "mvthemecol_textselectedbg": "249.0, 66.0, 114.53, 89.0",
            "mvthemecol_tabhovered": "249.0, 66.0, 66.01, 204.0",
            "mvthemecol_scrollbargrab": "79.0, 79.0, 79.0, 255.0",
            "mvthemecol_dragdroptarget": "255.0, 255.0, 0.0, 229.0",
            "mvthemecol_scrollbargrabhovered": "104.0, 104.0, 104.0, 255.0",
            "mvthemecol_navhighlight": "249.0, 66.0, 66.01, 255.0",
            "mvthemecol_scrollbargrabactive": "130.0, 130.0, 130.0, 255.0",
            "mvthemecol_navwindowinghighlight": "255.0, 255.0, 255.0, 178.0",
            "mvthemecol_checkmark": "249.0, 66.0, 66.01, 255.0",
            "mvthemecol_navwindowingdimbg": "204.0, 204.0, 204.0, 51.0",
            "mvthemecol_slidergrab": "224.0, 61.0, 61.01, 255.0",
            "mvthemecol_modalwindowdimbg": "204.0, 204.0, 204.0, 89.0",
        }
        with open(self._themes_dir / "default.ini", "w") as f:
            self.confParser.write(f, True)

    # ----- color helpers -----

    def _get_theme_color(self, theme_col: str) -> tuple[int, int, int, int]:
        key = theme_col.lower()
        itm = self.confParser["Theme"][key]
        itm = itm.removeprefix("[").removesuffix("]")
        parts = itm.split(",")
        return (
            int(float(parts[0].strip())),
            int(float(parts[1].strip())),
            int(float(parts[2].strip())),
            int(float(parts[3].strip())),
        )

    # ----- menu -----

    def _create_menu(self, parent):
        if parent is not None:
            dpg.add_menu_item(
                label="Configure Theme",
                callback=lambda: dpg.configure_item("editThemeWindow", show=True),
                parent=parent,
            )
            dpg.add_menu_item(
                label="Load Theme",
                callback=lambda: dpg.configure_item("loadThemeFileSelector", show=True),
                parent=parent,
            )
            dpg.add_menu_item(
                label="Save Theme",
                callback=lambda: dpg.configure_item("saveThemeFileSelector", show=True),
                parent=parent,
            )

        self._load_theme_dialog()
        self._save_theme_dialog()
        self._edit_theme_window()

    def _edit_theme_window(self):
        if dpg.does_item_exist("editThemeWindow"):
            dpg.delete_item("editThemeWindow")

        with dpg.window(
            tag="editThemeWindow",
            show=False,
            label="Theme Editor",
            width=600,
            height=700,
            no_title_bar=False,
        ):
            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Close",
                    callback=lambda: dpg.configure_item("editThemeWindow", show=False),
                )
                dpg.add_button(
                    label="Load...",
                    callback=lambda: dpg.configure_item("loadThemeFileSelector", show=True),
                )
                dpg.add_button(
                    label="Save...",
                    callback=lambda: dpg.configure_item("saveThemeFileSelector", show=True),
                )
            dpg.add_separator()

            with dpg.child_window(autosize_x=True, autosize_y=True):
                for color_name in THEME_COLORS:
                    tag = f"colEdit{color_name}"
                    try:
                        default_val = self._get_theme_color(color_name)
                    except Exception:
                        default_val = (128, 128, 128, 255)

                    dpg.add_color_edit(
                        default_value=default_val,
                        tag=tag,
                        label=color_name.replace("mvThemeCol_", ""),
                        callback=lambda s, a, u=color_name: self._on_color_changed(u),
                        alpha_bar=True,
                        no_inputs=False,
                        width=300,
                    )

    def _on_color_changed(self, color_name: str):
        """Called when user edits a color in the theme editor."""
        tag = f"colEdit{color_name}"
        val = dpg.get_value(tag)
        if val:
            # Update config
            key = color_name.lower()
            self.confParser["Theme"][key] = f"{val[0]}, {val[1]}, {val[2]}, {val[3]}"
            # Rebuild and rebind theme
            self._apply_theme()

    def _load_theme_dialog(self):
        try:
            with dpg.file_dialog(
                callback=lambda s, a: self._load_all(sent_file=a.get("file_path_name", "")),
                directory_selector=False,
                width=700,
                height=400,
                default_path=str(self._themes_dir),
                default_filename="default.ini",
                show=False,
                tag="loadThemeFileSelector",
                cancel_callback=_do_nothing,
            ):
                dpg.add_file_extension(".ini")
        except Exception:
            pass

    def _save_theme_dialog(self):
        try:
            with dpg.file_dialog(
                callback=lambda s, a: self._save_all(a),
                directory_selector=False,
                width=700,
                height=400,
                default_path=str(self._themes_dir),
                default_filename="custom.ini",
                show=False,
                tag="saveThemeFileSelector",
                cancel_callback=_do_nothing,
            ):
                dpg.add_file_extension(".ini")
        except Exception:
            pass

    def _load_all(self, sent_file: str = ""):
        if not sent_file:
            return
        try:
            self.confParser.read(sent_file)
            self._apply_theme()
            # Rebuild editor to reflect loaded colors
            self._edit_theme_window()
        except Exception as e:
            print(f"[EditThemePlugin] Load error: {e}")

    def _save_all(self, file_data: dict):
        if "file_path_name" not in file_data:
            return
        try:
            # Read current colors from editor widgets
            for color_name in THEME_COLORS:
                tag = f"colEdit{color_name}"
                if dpg.does_item_exist(tag):
                    val = dpg.get_value(tag)
                    key = color_name.lower()
                    self.confParser["Theme"][key] = f"{val[0]}, {val[1]}, {val[2]}, {val[3]}"
            with open(file_data["file_path_name"], "w") as f:
                self.confParser.write(f, True)
        except Exception as e:
            print(f"[EditThemePlugin] Save error: {e}")
