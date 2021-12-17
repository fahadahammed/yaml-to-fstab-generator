#!/usr/bin/python3
# Created By: Fahad Ahammed
# Created On: 2021-12-17 00:12:10
# Purpose: Generate a fstab file from YAML file
import yaml
import sys
import datetime

def read_fstab_yaml(yaml_file):
    try:
        with open(yaml_file, 'r') as stream:
            try:
                data_loaded = yaml.safe_load(stream)
                return data_loaded.get('fstab')
            except yaml.YAMLError as exc:
                print(exc)
                return None
    except Exception as ex:
        print(ex)
        return None

def generate_fstab(yaml_file):
    try:
        data = read_fstab_yaml(yaml_file=yaml_file)
        if data is None:
            print('Error: Invalid YAML file')
            sys.exit(1)
        else:
            entries = ""
            for k,v in data.items():
                file_system = k
                mount_point = v.get('mount')
                file_system_type = v.get('type')
                options = v.get('options')
                _dump = v.get('dump')
                _pass = v.get('pass')

                if v.get('export') is not None:
                    file_system = file_system + ':' + v.get('export')

                if mount_point is None:
                    print('Error: Invalid mount point')
                    sys.exit(1)
                if file_system_type is None:
                    print('Error: Invalid file system type')
                    sys.exit(1)

                if _dump is None:
                    _dump = 0
                if _pass is None:
                    _pass = 0
                if options is None:
                    options = "defaults"
                else:
                    if type(options) is list:
                        options = ",".join(options)
                    else:
                        options = "defaults"

                root_reserve = v.get('root-reserve')
                if root_reserve:
                    if root_reserve not in ("5%", 5):
                        entries += f"# We need to use `sudo tune2fs -m {root_reserve} {file_system}`.\n"
                    options += ",resgid=0,resuid=0"

                if mount_point == "/":
                    _pass = 1

                entry = f"{file_system}\t{mount_point}\t{file_system_type}\t{options}\t{_dump}\t{_pass}"
                entries += entry + '\n'
                
            return entries
    except Exception as e:
        print(e)
        sys.exit(1)

if __name__ == '__main__':
    the_fstab_yaml_file = sys.argv[1]
    print(f'# Generating fstab entry from YAML file: {the_fstab_yaml_file} at {datetime.datetime.now()}')
    generated_fstab = generate_fstab(yaml_file=the_fstab_yaml_file).strip()
    print('# fstab structure: <file system>   <dir/mount-dir>   <type>  <options>       <dump>  <pass>')
    print("#", "- - "*24)
    print(generated_fstab)
    print("#", "- - "*24)