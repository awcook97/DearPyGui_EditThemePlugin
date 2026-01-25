"""
Tests for EditThemePlugin and ChooseFontsPlugin

These tests verify that the plugins can be instantiated and their basic
functionality works correctly without requiring a full GUI environment.
"""

import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import Mock, patch, MagicMock
import configparser

# Mock dearpygui before importing plugins
sys.modules['dearpygui'] = MagicMock()
sys.modules['dearpygui.dearpygui'] = MagicMock()


class TestEditThemePlugin(unittest.TestCase):
    """Test cases for EditThemePlugin."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.themes_dir = os.path.join(self.test_dir, 'themes')
        os.makedirs(self.themes_dir, exist_ok=True)
        
        # Change to test directory
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('dearpygui.dearpygui')
    def test_plugin_initialization(self, mock_dpg):
        """Test that EditThemePlugin can be initialized."""
        mock_dpg.add_theme = Mock()
        mock_dpg.add_menu = Mock(return_value=1)
        mock_dpg.add_menu_item = Mock()
        mock_dpg.add_window = Mock()
        mock_dpg.add_button = Mock()
        mock_dpg.add_file_dialog = Mock()
        mock_dpg.add_file_extension = Mock()
        mock_dpg.theme_component = Mock()
        mock_dpg.mvAll = 0
        
        from EditThemePlugin import EditThemePlugin
        
        plugin = EditThemePlugin()
        
        # Verify plugin was created
        self.assertIsNotNone(plugin)
        self.assertIsNotNone(plugin.confParser)
        self.assertIsNotNone(plugin.theColors)
        
        # Verify theme folder was created
        self.assertTrue(os.path.exists('themes'))
        
        # Verify default theme file was created
        self.assertTrue(os.path.exists('themes/default.ini'))

    @patch('dearpygui.dearpygui')
    def test_default_theme_creation(self, mock_dpg):
        """Test that default theme file is properly created."""
        mock_dpg.add_theme = Mock()
        mock_dpg.add_menu = Mock(return_value=1)
        mock_dpg.add_menu_item = Mock()
        mock_dpg.add_window = Mock()
        mock_dpg.add_button = Mock()
        mock_dpg.add_file_dialog = Mock()
        mock_dpg.add_file_extension = Mock()
        mock_dpg.theme_component = Mock()
        mock_dpg.mvAll = 0
        
        from EditThemePlugin import EditThemePlugin
        
        plugin = EditThemePlugin()
        
        # Verify default theme file has content
        self.assertTrue(os.path.exists('themes/default.ini'))
        
        # Parse the default theme file
        config = configparser.ConfigParser()
        config.read('themes/default.ini')
        
        # Verify Theme section exists
        self.assertIn('Theme', config)
        
        # Verify some color entries exist
        self.assertIn('mvthemecol_text', config['Theme'])
        self.assertIn('mvthemecol_button', config['Theme'])

    def test_color_parsing(self):
        """Test getThemeColor method parses colors correctly."""
        from EditThemePlugin import EditThemePlugin
        
        # Create a plugin instance with minimal mocking
        with patch('dearpygui.dearpygui') as mock_dpg:
            mock_dpg.add_theme = Mock()
            mock_dpg.add_menu = Mock(return_value=1)
            mock_dpg.add_menu_item = Mock()
            mock_dpg.add_window = Mock()
            mock_dpg.add_button = Mock()
            mock_dpg.add_file_dialog = Mock()
            mock_dpg.add_file_extension = Mock()
            mock_dpg.theme_component = Mock()
            mock_dpg.mvAll = 0
            
            plugin = EditThemePlugin()
            
            # Test color parsing
            plugin.confParser['Theme']['test_color'] = "255.0, 128.0, 64.0, 255.0"
            result = plugin.getThemeColor('test_color')
            
            self.assertEqual(result, (255, 128, 64, 255))

    def test_color_parsing_error_handling(self):
        """Test getThemeColor handles errors gracefully."""
        from EditThemePlugin import EditThemePlugin
        
        with patch('dearpygui.dearpygui') as mock_dpg:
            mock_dpg.add_theme = Mock()
            mock_dpg.add_menu = Mock(return_value=1)
            mock_dpg.add_menu_item = Mock()
            mock_dpg.add_window = Mock()
            mock_dpg.add_button = Mock()
            mock_dpg.add_file_dialog = Mock()
            mock_dpg.add_file_extension = Mock()
            mock_dpg.theme_component = Mock()
            mock_dpg.mvAll = 0
            
            plugin = EditThemePlugin()
            
            # Test with invalid color
            plugin.confParser['Theme']['invalid_color'] = "not a color"
            result = plugin.getThemeColor('invalid_color')
            
            # Should return default white
            self.assertEqual(result, (255, 255, 255, 255))


class TestChooseFontsPlugin(unittest.TestCase):
    """Test cases for ChooseFontsPlugin."""

    def setUp(self):
        """Set up test environment."""
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.fonts_dir = os.path.join(self.test_dir, 'Fonts')
        os.makedirs(self.fonts_dir, exist_ok=True)
        
        # Change to test directory
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create test font files
        with open(os.path.join(self.fonts_dir, 'test.ttf'), 'w') as f:
            f.write('fake font data')
        with open(os.path.join(self.fonts_dir, 'TEST.TTF'), 'w') as f:
            f.write('fake font data uppercase')
        with open(os.path.join(self.fonts_dir, 'test.otf'), 'w') as f:
            f.write('fake otf font')
        with open(os.path.join(self.fonts_dir, 'test.OTF'), 'w') as f:
            f.write('fake OTF font uppercase')

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('dearpygui.dearpygui')
    def test_plugin_initialization(self, mock_dpg):
        """Test that ChooseFontsPlugin can be initialized."""
        mock_dpg.add_font_registry = Mock(return_value=1)
        mock_dpg.add_menu = Mock(return_value=1)
        mock_dpg.add_menu_item = Mock()
        mock_dpg.add_window = Mock()
        mock_dpg.window = MagicMock()
        mock_dpg.child_window = MagicMock()
        mock_dpg.group = MagicMock()
        mock_dpg.add_text = Mock()
        mock_dpg.add_combo = Mock()
        mock_dpg.add_input_int = Mock()
        mock_dpg.add_slider_float = Mock()
        mock_dpg.add_checkbox = Mock()
        mock_dpg.add_button = Mock()
        mock_dpg.get_viewport_width = Mock(return_value=1200)
        mock_dpg.get_viewport_height = Mock(return_value=800)
        
        from ChooseFontsPlugin import ChooseFontsPlugin
        
        plugin = ChooseFontsPlugin()
        
        # Verify plugin was created
        self.assertIsNotNone(plugin)
        self.assertIsNotNone(plugin.fontDict)
        
        # Verify Fonts folder was created
        self.assertTrue(os.path.exists('Fonts'))

    @patch('dearpygui.dearpygui')
    def test_font_file_discovery_case_insensitive(self, mock_dpg):
        """Test that font files are discovered case-insensitively."""
        mock_dpg.add_font_registry = Mock(return_value=1)
        mock_dpg.add_menu = Mock(return_value=1)
        mock_dpg.add_menu_item = Mock()
        mock_dpg.add_window = Mock()
        mock_dpg.window = MagicMock()
        mock_dpg.child_window = MagicMock()
        mock_dpg.group = MagicMock()
        mock_dpg.add_text = Mock()
        mock_dpg.add_combo = Mock()
        mock_dpg.add_input_int = Mock()
        mock_dpg.add_slider_float = Mock()
        mock_dpg.add_checkbox = Mock()
        mock_dpg.add_button = Mock()
        mock_dpg.get_viewport_width = Mock(return_value=1200)
        mock_dpg.get_viewport_height = Mock(return_value=800)
        mock_dpg.font = MagicMock()
        mock_dpg.add_font_range_hint = Mock()
        mock_dpg.add_font_range = Mock()
        mock_dpg.mvFontRangeHint_Default = 0
        mock_dpg.mvFontRangeHint_Cyrillic = 1
        
        from ChooseFontsPlugin import ChooseFontsPlugin
        
        plugin = ChooseFontsPlugin()
        
        # Check that font files were discovered (case-insensitive)
        font_files = [k for k in plugin.fontDict.keys() if k.lower().endswith(('.ttf', '.otf'))]
        
        # Should find all 4 test font files
        self.assertEqual(len(font_files), 4)
        self.assertIn('test.ttf', font_files)
        self.assertIn('TEST.TTF', font_files)
        self.assertIn('test.otf', font_files)
        self.assertIn('test.OTF', font_files)

    @patch('dearpygui.dearpygui')
    def test_user_preferences_files_created(self, mock_dpg):
        """Test that user preference files are created."""
        mock_dpg.add_font_registry = Mock(return_value=1)
        mock_dpg.add_menu = Mock(return_value=1)
        mock_dpg.add_menu_item = Mock()
        mock_dpg.add_window = Mock()
        mock_dpg.window = MagicMock()
        mock_dpg.child_window = MagicMock()
        mock_dpg.group = MagicMock()
        mock_dpg.add_text = Mock()
        mock_dpg.add_combo = Mock()
        mock_dpg.add_input_int = Mock()
        mock_dpg.add_slider_float = Mock()
        mock_dpg.add_checkbox = Mock()
        mock_dpg.add_button = Mock()
        mock_dpg.get_viewport_width = Mock(return_value=1200)
        mock_dpg.get_viewport_height = Mock(return_value=800)
        
        from ChooseFontsPlugin import ChooseFontsPlugin
        
        plugin = ChooseFontsPlugin()
        
        # Verify preference files were created
        self.assertTrue(os.path.exists('Fonts/USERFONT'))
        self.assertTrue(os.path.exists('Fonts/USERSIZE'))
        self.assertTrue(os.path.exists('Fonts/USERSCALE'))


class TestIntegration(unittest.TestCase):
    """Integration tests for both plugins."""

    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        os.chdir(self.original_dir)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    @patch('dearpygui.dearpygui')
    def test_both_plugins_can_coexist(self, mock_dpg):
        """Test that both plugins can be instantiated together."""
        # Mock all DearPyGui functions
        mock_dpg.add_theme = Mock()
        mock_dpg.add_menu = Mock(return_value=1)
        mock_dpg.add_menu_item = Mock()
        mock_dpg.add_window = Mock()
        mock_dpg.add_button = Mock()
        mock_dpg.add_file_dialog = Mock()
        mock_dpg.add_file_extension = Mock()
        mock_dpg.theme_component = MagicMock()
        mock_dpg.mvAll = 0
        mock_dpg.add_font_registry = Mock(return_value=1)
        mock_dpg.window = MagicMock()
        mock_dpg.child_window = MagicMock()
        mock_dpg.group = MagicMock()
        mock_dpg.add_text = Mock()
        mock_dpg.add_combo = Mock()
        mock_dpg.add_input_int = Mock()
        mock_dpg.add_slider_float = Mock()
        mock_dpg.add_checkbox = Mock()
        mock_dpg.get_viewport_width = Mock(return_value=1200)
        mock_dpg.get_viewport_height = Mock(return_value=800)
        
        from EditThemePlugin import EditThemePlugin
        from ChooseFontsPlugin import ChooseFontsPlugin
        
        # Create both plugins
        theme_plugin = EditThemePlugin()
        font_plugin = ChooseFontsPlugin()
        
        # Verify both were created
        self.assertIsNotNone(theme_plugin)
        self.assertIsNotNone(font_plugin)
        
        # Verify separate directories exist
        self.assertTrue(os.path.exists('themes'))
        self.assertTrue(os.path.exists('Fonts'))


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
