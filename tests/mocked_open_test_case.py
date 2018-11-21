import sys
if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins

import io
import unittest

import wsl_path_converter

class MockedOpenTestCase(unittest.TestCase):
    
    original_open = builtins.open
    
    def mocked_open(self, path, *args, **kwargs):
        if path == "/proc/mounts":
            return io.BytesIO(self.mounts)
        else:
            return MockedOpenTestCase.original_open(path, *args, **kwargs)
    
    def setUp(self):
        self.mounts = b""
        builtins.open = self.mocked_open
    
    def tearDown(self):
        builtins.open = MockedOpenTestCase.original_open
