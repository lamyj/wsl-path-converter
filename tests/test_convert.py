import builtins
import io
import unittest

import wsl_path_converter

mounts = b""

original_open = builtins.open
def mocked_open(path, *args, **kwargs):
    if path == "/proc/mounts":
        return io.BytesIO(mounts)
    else:
        return original_open(path, *args, **kwargs)
builtins.open = mocked_open

class TestConvert(unittest.TestCase):
    def setUp(self):
        
    def test_w_local(self):
        globals()["mounts"] = b"C: /mnt/c drvfs rw,relatime 0 0"
        path = wsl_path_converter.convert_w(
            "/mnt/c/Users/myself/Pictures/Camera Roll")
        self.assertEqual(path, u"C:\\Users\\myself\\Pictures\\Camera Roll")
    
    def test_w_remote(self):
        globals()["mounts"] = (
            b"\\134\\134samba.example.com\\134my\\040share /samba " 
            b"drvfs rw,relatime 0 0")
        path = wsl_path_converter.convert_w("/samba/Foo")
        self.assertEqual(path, u"\\\\samba.example.com\\my share\\Foo")
    
    def test_u_local(self):
        globals()["mounts"] = b"C: /mnt/c drvfs rw,relatime 0 0"
        path = wsl_path_converter.convert_u(
            u"C:\\Users\\myself\\Pictures\\Camera Roll")
        self.assertEqual(path, u"/mnt/c/Users/myself/Pictures/Camera Roll")
    
    def test_u_remote(self):
        globals()["mounts"] = (
            b"\\134\\134samba.example.com\\134my\\040share /samba " 
            b"drvfs rw,relatime 0 0")
        path = wsl_path_converter.convert_u(
            u"\\\\samba.example.com\\my share\\Foo")
        self.assertEqual(path, u"/samba/Foo")
    
    def test_guess_drive_letter(self):
        self.assertEqual(
            wsl_path_converter.guess_converter("C:\\autoexec.bat"),
            wsl_path_converter.convert_u)
    
    def test_guess_unc(self):
        self.assertEqual(
            wsl_path_converter.guess_converter(
                "\\\\samba.example.com\\my share\\Foo"),
            wsl_path_converter.convert_u)
    
    def test_guess_unix(self):
        self.assertEqual(
            wsl_path_converter.guess_converter("/etc/passwd"),
            wsl_path_converter.convert_w)

if __name__ == "__main__":
    unittest.main()
