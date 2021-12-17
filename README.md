# yaml-to-fstab-generator
The tool or script to convert yaml file containing fstab entry to fstab format.

Structure:

```bash
./
├── LICENSE
├── README.md
├── __pycache__
│   ├── genfstab.cpython-39.pyc
│   └── test.cpython-39.pyc
├── example_yamls
│   ├── fstab.v1.yaml
│   ├── fstab.yaml
│   └── fstab_invalid.yaml
├── genfstab.py
├── requirements.txt
└── test.py

2 directories, 10 files
```

## Requirement
To run the script, one must fulfill some requirements.
- Script is ran in: Python 3.9.9 but should work above **Python 3.5+**
- Pip(use pip3 if needed according to your system) should be installed and necessarily for python3.

## Prepare environment

### Install required libraries to work with this tool.

```bash
$ pip install -r requirements.txt
```
## How to

```bash
$ python3 genfstab.py <yaml_file_with_location_if_needed>
```

i.e. `python3 genfstab.py /Users/fahad/tmp/fstab.yaml`

I did not write functions or codes to generate the file through this script. But I let this to the standard output option of bash or other similar shell by using ">" or ">>". I believe it has flexibility to do that.
i.e. `python3 genfstab.py /Users/fahad/tmp/fstab.yaml >> /etc/fstab`

Though, we might want to depend on some sanity check on rewriting the fstab.

## Example
There are some example yaml files in this repository, inside the directory **example_yamls**.

### Example 1

Yaml file: **fstab.yaml**

```yaml
fstab:
  /dev/sda1:
    mount: /boot
    type: xfs
  /dev/sda2:
    mount: /
    type: ext4
  /dev/sdb1:
    mount: /var/lib/postgresql
    type: ext4
    root-reserve: 10%
  192.168.4.5:
    mount: /home
    export: /var/nfs/home
    type: nfs
    options:
      - noexec
      - nosuid
  /dev/sdc1:
    mount: /boot
    type: ext4
```

```bash
$ python3 genfstab.py example_yamls/fstab.yaml
```

Output:

```bash
# Generating fstab entry from YAML file: example_yamls/fstab.yaml at 2021-12-17 21:08:47.349057
# fstab structure: <file system>   <dir/mount-dir>   <type>  <options>       <dump>  <pass>
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
/dev/sda1	/boot	xfs	defaults	0	0
/dev/sda2	/	ext4	defaults	0	1
# We need to use `sudo tune2fs -m 10% /dev/sdb1`.
/dev/sdb1	/var/lib/postgresql	ext4	defaults,resgid=0,resuid=0	0	0
192.168.4.5:/var/nfs/home	/home	nfs	noexec,nosuid	0	0
/dev/sdc1	/boot	ext4	defaults	0	0
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

### Example 2

Yaml file: **fstab.v1.yaml**

```yaml
fstab:
  /dev/sda1:
    mount: /boot
    type: xfs
  /dev/sda2:
    mount: /
    type: xfs
  /dev/sda3:
    mount: swap
    type: swap
  UUID=30fcb748-ad1e-4228-af2f-951e8e7b56df:
    mount: /playground
    type: btrfs
    root-reserve: 5%
  192.168.31.101:
    mount: /fun
    export: /var/nfs/fun
    type: nfs
    options:
      - noexec
      - nosuid
```

```bash
$ python3 genfstab.py example_yamls/fstab.v1.yaml
```

Output:

```bash
# Generating fstab entry from YAML file: example_yamls/fstab.v1.yaml at 2021-12-17 21:11:22.244075
# fstab structure: <file system>   <dir/mount-dir>   <type>  <options>       <dump>  <pass>
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
/dev/sda1	/boot	xfs	defaults	0	0
/dev/sda2	/	xfs	defaults	0	1
/dev/sda3	swap	swap	defaults	0	0
UUID=30fcb748-ad1e-4228-af2f-951e8e7b56df	/playground	btrfs	defaults,resgid=0,resuid=0	0
192.168.31.101:/var/nfs/fun	/fun	nfs	noexec,nosuid	0	0
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```

### Example 3

Yaml file: **fstab_invalid.yaml**

```yaml
      fstab:
  /dev/sda1:
    mount: /boot
    type: xfs
  /dev/sda2:
    mount: /
    type: ext4
  /dev/sdb1:
    mount: /var/lib/postgresql
    type: ext4
    root-reserve: 10%
  192.168.4.5:
    mount: /home
    export: /var/nfs/home
    type: nfs
    options:
      - noexec
      - nosuid
  /dev/sdc1:
    mount: /boot
    type: ext4
```

This file has started with several spaces before "fstab:". Thus it is an invalid yaml file.

```bash
$ python3 genfstab.py example_yamls/fstab_invalid_.yaml
```

Output:

```bash
# Generating fstab entry from YAML file: example_yamls/fstab_invalid.yaml at 2021-12-17 21:13:42.842345
expected '<document start>', but found '<block mapping start>'
  in "example_yamls/fstab_invalid.yaml", line 2, column 3
Error: Invalid YAML file
```

As expected, it should through error.

### Example 4

Yaml file: **_fstab.yaml**

This file doesn't exists. So, the script should give error too.

```bash
$ python3 genfstab.py example_yamls/_fstab.yaml
```

Output:

```bash
# Generating fstab entry from YAML file: example_yamls/_fstab.yaml at 2021-12-17 21:15:52.679266
[Errno 2] No such file or directory: 'example_yamls/_fstab.yaml'
Error: Invalid YAML file
```

## Tests

There is a small effort with unitest on reading yaml file. Unittest file is **test.py**

```bash
$ python3 -m unittest test
```

Output:

```bash
expected '<document start>', but found '<block mapping start>'
  in "example_yamls/fstab_invalid.yaml", line 2, column 3
.[Errno 2] No such file or directory: 'example_yamls/_fstab_.yaml'
..
----------------------------------------------------------------------
Ran 3 tests in 0.002s

OK
```

## Conclusion
This script is an attempt to generate fstab from yaml file. It can be used much more efficiently with implementing enough libraries to -

- handle errors efficiently
- efficient loop handling
- make a CLI application by using arparse or similar to through good responses and handle situations and better clarity on inputs.
etc.

I have just tried to implement a working solutions. When working with this script with an example from the *fstab.yaml*, I stumble upon a problem with this: *root-reserve: 10%*. As we can not define reserve space size via mounting options but in creating or tuning.