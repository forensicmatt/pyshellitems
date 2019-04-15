A Python library for parsing Shell Items/Extension Blocks/Property Stores.

# Handled Shell Items
|Name|Class Type|Signature|Handled|Notes|
| --- | --- | --- | --- | --- |
|File entry shell item|0x30 after applying a bitmask of 0x70| |Partly|Not handled for pre Windows XP|
|Application shell item|NA|0x53505041 ('APPS')|Yes| |
|Control panel category shell item|0x01|0x39de2184|Yes| |
|URI shell item|0x61| |Partly|Not handled for data size > 0|
|Users property view shell item| |0x23febbee,0x10141981,0x3b93afbb,0xbeebee00|Partly|More work needs to be done| 
|Users property view delegate item|0x1F|0x23a3dfd5|Yes| |
|URI shell item|0x61| |Partly| Needs verification with FTP data |

# Handled Extension Blocks
|Signature|Handled|Notes|
| --- | --- | --- |
| BEEF0004 | Yes | |
| BEEF0013 | Yes | Mainly unknown |
| BEEF0019 | Yes | |
| BEEF0025 | Yes | |
| BEEF0026 | Yes | |

# ShellItem Corpus
The corpus folder contains a lot of shell items files that were collected via the `extract_shellbags.py` 
and `extract_shellitems_from_lnk.py` scripts from public images in an effort to inventory the different shell items and
keep tabs on what this library can currently parse. I would like to work to make this more of a unique structure list.

### scripts/parse_shellitems.py
```
Parse a raw file containing a shell item or a folder of shell items. This script looks for 
*.shellitem or *BagMRU.* file names.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        The source folder or file.
```

#### Example output
```
pyshellitems\scripts>python parse_shellitems.py -s ..\corpus\defctf18-01-administrator-BagMRU.1.0.2.1.0.1
Source: ..\corpus\defctf18-01-administrator-BagMRU.1.0.2.1.0.1
Parsing: ..\corpus\defctf18-01-administrator-BagMRU.1.0.2.1.0.1
{"type": "0x31", "sub_flag": "0x01", "file_size": 0, "modified": 2383432939, "file_attributes": 16, "name": "original", "extension_block": {"signature": "BEEF0004", "version": 9, "created": 2382908651, "accessed": 2383432939, "identifier": 46, "mft_reference": 2533274790508926, "long_name": "original", "localized_name": null, "version_offset": 24}}
```

```
pyshellitems\scripts>python parse_shellitems.py -s ..\corpus\0x00.011caadadcea41258b29ff1b268f17a8.1.shellitem
Source: ..\corpus\0x00.011caadadcea41258b29ff1b268f17a8.1.shellitem
Parsing: ..\corpus\0x00.011caadadcea41258b29ff1b268f17a8.1.shellitem
{"type": "0x00", "unknown1": 0, "size2": 284, "signature": "APPS", "property_store_size": 266, "property_store": [{"version": "1SPS", "guid": "b725f130-47ef-101a-a5f1-02608c9eebac", "values": [{"identifier": "001F [VT_LPWSTR]", "value": ""}]}, {"version": "1SPS", "guid": "9f4c2855-9f79-4b39-a8d0-e1d42de1d5f3", "values": [{"identifier": "001F [VT_LPWSTR]", "value": "windows.immersivecontrolpanel_cw5n1h2txyewy!microsoft.windows.immersivecontrolpanel"}]}]}
```

### scripts/extract_shellbags.py
This tool uses the yarp library to extract out shellbags into files. This tool can be used
to create a shellitem corpus for research and testing purposes.
```
usage: extract_shellbags.py [-h] -s SOURCE [-p PREFIX] -o OUTPUT

Extract shellbags from usrclass hive for research purposes.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        The source USRCLASS.DAT file.
  -p PREFIX, --prefix PREFIX
                        Prefix to append to file names.
  -o OUTPUT, --output OUTPUT
                        The output folder.
```

### scripts/extract_shellitems_from_lnk.py
This tool uses pylnk to recurse a link file's target data to extract out shell items. This tool 
can be used to create a shellitem corpus for research and testing purposes.
```
usage: extract_shellitems_from_lnk.py [-h] -s SOURCE -o OUTPUT

Extract shell items from link files for research purposes.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        The source folder or link file.
  -o OUTPUT, --output OUTPUT
                        The output folder.
```
