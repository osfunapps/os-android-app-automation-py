Introduction
------------

This module aim to assist with an Android app buildup.

To use, create an XML file with your app properties and run.

## Installation
Install via pip:

    pip install os-android-app-automation

## Usage:

Create an XML file with your app properties:

## todo: add xml here

After your created the XML file, call it from code:
    
## todo: add callbacks here
    import os_file_automation.xml_mapper.xml_mapper as xm
 
    xm.set_xcode_project_by_xml('/path/to/your/xcode_mapper.xml',
                                place_holder_map = {'$app_path': '/path/to/a/dynamic/directory'})

        
           

And more...


## Links
[GitHub - osapps](https://github.com/osfunapps)

## Licence
ISC