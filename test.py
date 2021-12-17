import unittest

from genfstab import read_fstab_yaml

class Test_genfstab(unittest.TestCase):
    def test_read_fstab_yaml_dict(self):
        self.assertEqual(type(read_fstab_yaml(yaml_file="example_yamls/fstab.yaml")), dict, "Should be dict and valid YAML file")
    
    def test_read_fstab_invalid_yaml(self):
        self.assertEqual(read_fstab_yaml(yaml_file="example_yamls/fstab_invalid.yaml"), None, "Should be None and invalid YAML file")

    def test_read_fstab_nonexist_yaml(self):
        self.assertEqual(read_fstab_yaml(yaml_file="example_yamls/_fstab_.yaml"), None, "Should be None and invalid YAML file")

if __name__ == '__main__':
    unittest.main()