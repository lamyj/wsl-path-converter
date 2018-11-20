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

class TestMounts(unittest.TestCase):
    def test_skip_non_drvfs(self):
        globals()["mounts"] = (
            b"/dev/sda1 / ext2 defaults 0 0\n"
            b"C: /mnt/c drvfs rw,relatime 0 0"
            b"nfs.example.com /srv nfs defaults 0 0"
        )
        mounts = wsl_path_converter.parse_mounts()
        self.assertEqual(mounts, ({u"C:": u"/mnt/c"}, {u"/mnt/c": u"C:"}))
    
    def test_source_escape(self):
        globals()["mounts"] = (
            b"\\134\\134samba.example.com\\134my\\040share /mnt/share drvfs rw,relatime 0 0")
        mounts = wsl_path_converter.parse_mounts()
        self.assertEqual(
            mounts, 
            (
                {u"\\\\samba.example.com\\my share": u"/mnt/share"}, 
                {u"/mnt/share": u"\\\\samba.example.com\\my share"}))
    
    def test_target_escape(self):
        globals()["mounts"] = br"C: /mnt/c\040drive drvfs rw,relatime 0 0"
        mounts = wsl_path_converter.parse_mounts()
        self.assertEqual(
            mounts, ({u"C:": u"/mnt/c drive"}, {u"/mnt/c drive": u"C:"}))

if __name__ == "__main__":
    unittest.main()
