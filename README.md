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
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/8b0adc9f-7b59-4bec-bc95-5a9150afb4ef)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/aaf1287e-d092-48d3-94e0-3f9251e8da84)
![image](https://github.com/awcook97/DearPyGui_EditThemePlugin/assets/8891546/a8cb2c2c-9c78-46ab-89a9-36aa3f62cc3c)
