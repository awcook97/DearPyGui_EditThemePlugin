"""
ChooseFontsPlugin — DearPyGui 2.x compatible font chooser.
Adapted from https://github.com/awcook97/DearPyGui_EditThemePlugin
Supports both Linux and Windows font directories.
"""
import dearpygui.dearpygui as dpg
import os
import platform
import pathlib


# Default font directories per platform
def _get_system_font_dirs() -> list[str]:
    dirs = []
    system = platform.system()
    if system == "Windows":
        windir = os.environ.get("WINDIR", r"C:\Windows")
        dirs.append(os.path.join(windir, "Fonts"))
    elif system == "Linux":
        # Standard Linux font directories
        for d in [
            "/usr/share/fonts",
            "/usr/local/share/fonts",
            os.path.expanduser("~/.local/share/fonts"),
            os.path.expanduser("~/.fonts"),
        ]:
            if os.path.isdir(d):
                dirs.append(d)
    elif system == "Darwin":
        dirs.extend(["/Library/Fonts", os.path.expanduser("~/Library/Fonts")])
    return dirs


def _walk_fonts(directory: str) -> dict[str, str]:
    """Recursively find .ttf/.otf files, return {display_name: full_path}."""
    found: dict[str, str] = {}
    try:
        for root, _dirs, files in os.walk(directory):
            for f in sorted(files):
                if f.lower().endswith((".ttf", ".otf")):
                    found[f] = os.path.join(root, f)
    except OSError:
        pass
    return found


class ChooseFontsPlugin:
    def __init__(self, menu_parent=None):
        self.ignore = "NO CUSTOM FONT, IGNORE"
        self.font_registry = dpg.add_font_registry()
        self.fontDict: dict[str, str | None] = {}
        self.userFont = self.ignore
        self.userSize = 20
        self.userScale = 1.0

        self._config_dir = pathlib.Path(__file__).parent.parent / "Fonts"
        self._create_folders()
        self._create_font_library()
        self._create_font_window()
        if menu_parent is not None:
            self._create_font_menu(menu_parent)

    # ----- config persistence -----

    def _create_folders(self):
        self._config_dir.mkdir(parents=True, exist_ok=True)
        uf = self._config_dir / "USERFONT"
        if not uf.exists():
            uf.write_text(self.ignore, encoding="utf-8")
        us = self._config_dir / "USERSIZE"
        if not us.exists():
            us.write_text("20", encoding="utf-8")
        usc = self._config_dir / "USERSCALE"
        if not usc.exists():
            usc.write_text("1", encoding="utf-8")

    def _create_font_library(self):
        try:
            self.userFont = (self._config_dir / "USERFONT").read_text("utf-8").strip() or self.ignore
        except Exception:
            self.userFont = self.ignore
        try:
            self.userSize = int((self._config_dir / "USERSIZE").read_text("utf-8").strip())
        except Exception:
            self.userSize = 20
        try:
            self.userScale = float((self._config_dir / "USERSCALE").read_text("utf-8").strip())
        except Exception:
            self.userScale = 1.0

        # Local fonts
        self.fontDict["── YOUR FONTS ──"] = None
        local_dir = str(self._config_dir)
        for fname in sorted(os.listdir(local_dir)):
            if fname.lower().endswith((".ttf", ".otf")):
                full = os.path.join(local_dir, fname)
                self.fontDict[fname] = full

        # System fonts
        for sys_dir in _get_system_font_dirs():
            label = f"── {os.path.basename(sys_dir).upper()} ──"
            if label not in self.fontDict:
                self.fontDict[label] = None
            sys_fonts = _walk_fonts(sys_dir)
            self.fontDict.update(sys_fonts)

        # Apply saved font if available
        if self.userFont in self.fontDict and self.fontDict[self.userFont]:
            try:
                fnt = dpg.add_font(
                    file=str(self.fontDict[self.userFont]),
                    size=self.userSize,
                    parent=self.font_registry,
                    tag="fntCFPNewFont",
                )
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent="fntCFPNewFont")
                dpg.bind_font(fnt)
                dpg.set_global_font_scale(self.userScale)
            except Exception as e:
                print(f"[ChooseFontsPlugin] Error loading saved font: {e}")

    # ----- GUI -----

    def _create_font_window(self):
        with dpg.window(
            label="Font Settings",
            width=500,
            height=400,
            show=False,
            tag="winCFPFontWindow",
        ):
            with dpg.child_window(autosize_x=True, height=-120):
                dpg.add_text(
                    "Choose a font from your local Fonts/ folder or system fonts.",
                    wrap=0,
                )
                dpg.add_text(
                    "Click 'Change Font' to apply. Click 'Save' to persist across sessions.",
                    wrap=0,
                    color=(160, 160, 160),
                )
                dpg.add_separator()
                dpg.add_combo(
                    list(self.fontDict.keys()),
                    label="Font",
                    callback=lambda: self.build_fonts(),
                    tag="cmbCFPFontType",
                    width=-1,
                )
                dpg.add_input_int(
                    label="Size",
                    default_value=self.userSize,
                    tag="intCFPSize",
                    width=150,
                )
                dpg.add_slider_float(
                    default_value=self.userScale,
                    label="Scale",
                    tag="slideCFPFontScale",
                    min_value=0.5,
                    max_value=3.0,
                    clamped=True,
                    width=200,
                )
                with dpg.group(horizontal=True):
                    dpg.add_checkbox(label="Auto-preview?", tag="chkbxCFPAutosize", default_value=True)
                    dpg.add_button(label="Change Font", callback=lambda: self.btnBuild())

            with dpg.child_window(autosize_x=True, height=80):
                dpg.add_text("the quick brown fox jumped over the lazy dog", wrap=0)
                dpg.add_text("THE QUICK BROWN FOX JUMPED OVER THE LAZY DOG", wrap=0)
                dpg.add_text("0123456789  +0x00B4  /*0xDEAD*/", wrap=0)

            with dpg.group(horizontal=True):
                dpg.add_button(
                    label="Close",
                    callback=lambda: dpg.configure_item("winCFPFontWindow", show=False),
                )
                dpg.add_button(label="Save", callback=lambda: self.save_fonts())
                dpg.add_button(
                    label="Reset to Default",
                    callback=lambda: (dpg.bind_font(""), dpg.set_global_font_scale(1.0)),
                )

    def _create_font_menu(self, parent):
        dpg.add_menu_item(
            label="Font Settings...",
            callback=lambda: dpg.configure_item("winCFPFontWindow", show=True),
            parent=parent,
        )

    # ----- font building -----

    def btnBuild(self):
        dpg.set_value("chkbxCFPAutosize", True)
        self.build_fonts()
        dpg.set_value("chkbxCFPAutosize", False)

    def build_fonts(self):
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
            fnt = dpg.add_font(
                file=str(self.fontDict[self.userFont]),
                size=self.userSize,
                parent=self.font_registry,
                tag="fntCFPNewFont",
            )
            dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent="fntCFPNewFont")
            dpg.bind_font(fnt)
            self.userScale = float(dpg.get_value("slideCFPFontScale"))
            dpg.set_global_font_scale(self.userScale)
        except Exception as e:
            print(f"[ChooseFontsPlugin] Error: {e}")

    def save_fonts(self):
        (self._config_dir / "USERFONT").write_text(str(self.userFont), encoding="utf-8")
        (self._config_dir / "USERSIZE").write_text(str(self.userSize), encoding="utf-8")
        (self._config_dir / "USERSCALE").write_text(str(self.userScale), encoding="utf-8")
        dpg.configure_item("winCFPFontWindow", show=False)
