import unittest

import wsl_path_converter

class TestRoots(unittest.TestCase):
    def test_top_level(self):
        root = wsl_path_converter.find_root(
            {u"/mnt/c": u"C:"}, "/mnt/c", "/")
        self.assertEqual(root, "/mnt/c")
        
    def test_child(self):
        root = wsl_path_converter.find_root(
            {u"/mnt/c": u"C:"}, "/mnt/c/autoexec.bat", "/")
        self.assertEqual(root, "/mnt/c")
    
    def test_same_prefix_short(self):
        root = wsl_path_converter.find_root(
            {u"/mnt/c": u"C:", u"/mnt/c_bis": u"C:"}, 
            "/mnt/c/autoexec.bat", "/")
        self.assertEqual(root, "/mnt/c")
    
    def test_same_prefix_short_long(self):
        root = wsl_path_converter.find_root(
            {u"/mnt/c": u"C:", u"/mnt/c_bis": u"C:"}, 
            "/mnt/c_bis/autoexec.bat", "/")
        self.assertEqual(root, "/mnt/c_bis")
    
    def test_missing_root(self):
        with self.assertRaises(Exception):
            wsl_path_converter.find_root(
                {u"/mnt/c": u"C:"}, 
                "/mnt/nowhere/autoexec.bat", "/")

if __name__ == "__main__":
    unittest.main()
