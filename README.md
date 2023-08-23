# DearPyGui_EditThemePlugin
Adds a viewport menu that allows the user to create a theme in dearpygui, save the theme to a .ini file, and load themes from a .ini file.

You can take a look at the code to see how it works. There's a small demo in this that shows a brief demonstration of different objects. 

To use EditThemePlugin, all you have to do is load the class, then call the class in a menu.
```
  import dearpygui.dearpygui as dpg
  from EditThemePlugin import EditThemePlugin
  dpg.create_context()
  dpg.create_viewport(title="some title", width=1000, height=1000)
  with dpg.viewport_menu_bar():
    with dpg.menu():
      dpg.add_menu_item(label="Show Metrics", 		callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
    EditThemePlugin()
  dpg.setup_dearpygui()
  dpg.show_viewport()
  dpg.start_dearpygui()
  dpg.destroy_context()
  exit()
```
Files are storeed locally, in a folder called "themes". Default theme is "themes/default.ini". The program will create the default on start up.
