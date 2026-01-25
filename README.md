# DearPyGui Edit Theme Plugin

A powerful theme editor and font selector plugin for [DearPyGui](https://github.com/hoffstadt/DearPyGui) that allows users to customize their application's appearance in real-time.

## Features

- **EditThemePlugin**: Create, edit, save, and load custom themes for your DearPyGui applications
- **ChooseFontsPlugin**: Choose from system fonts and custom fonts with size and scale adjustments
- Save themes to `.ini` files for easy sharing and reuse
- Live preview of theme changes
- Integrates seamlessly with DearPyGui's viewport menu bar

## Requirements

- Python 3.8+ (Python 3.14 supported)
- DearPyGui 2.1.1 or higher

## Installation

1. Clone this repository or download the plugin files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### EditThemePlugin

Add the theme editor to your DearPyGui application:

```python
import dearpygui.dearpygui as dpg
from EditThemePlugin import EditThemePlugin

dpg.create_context()
dpg.create_viewport(title="My App", width=1000, height=1000)

with dpg.viewport_menu_bar():
    with dpg.menu(label="Tools"):
        dpg.add_menu_item(label="Show Metrics", callback=lambda: dpg.show_tool(dpg.mvTool_Metrics))
    EditThemePlugin()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
```

Theme files are stored locally in a folder called `themes/`. The default theme is `themes/default.ini`, which is automatically created on first run.

### ChooseFontsPlugin

Add the font selector to your DearPyGui application:

```python
import dearpygui.dearpygui as dpg
from ChooseFontsPlugin import ChooseFontsPlugin
from EditThemePlugin import EditThemePlugin

dpg.create_context()
dpg.create_viewport(title="My App", width=1000, height=1000)

with dpg.viewport_menu_bar():
    myFonts = ChooseFontsPlugin()
    myTheme = EditThemePlugin()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
```

The ChooseFontsPlugin integrates perfectly with EditThemePlugin. Place your custom fonts (`.ttf` or `.otf` files) in the `Fonts/` folder, and they will appear in the font selector.

### Screenshots

#### Theme Editor

![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/8b0adc9f-7b59-4bec-bc95-5a9150afb4ef)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/aaf1287e-d092-48d3-94e0-3f9251e8da84)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/a8cb2c2c-9c78-46ab-89a9-36aa3f62cc3c)

#### Font Selector

![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/6b18d676-5ae2-4db9-9610-1e78793a4f93)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/61cff4d4-8ec4-4795-a418-565aaf6989dc)

![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/c6110e5c-3312-4747-9fa8-1d96fcdb55cd)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/aba14839-7ecf-4047-843e-f07af0557e9f)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/69068f50-3987-41c0-9996-d93aab159bf4)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/125441f1-f591-40ad-9880-8a7ae7e29acb)

## Tips

- You can assign the plugins to variables for debugging purposes:
  ```python
  with dpg.viewport_menu_bar():
      myFonts = ChooseFontsPlugin()
      myTheme = EditThemePlugin()
  ```
  If something goes wrong, you can pause the script and inspect these variables.

- Themes and fonts are saved locally, so your customizations persist across sessions.

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
