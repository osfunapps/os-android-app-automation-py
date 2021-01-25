import os_xml_handler.xml_handler as xh

from os_android_app_automation.bp import _app_automation as bp


def set_android_project_by_xml(xml_path,
                               place_holder_map=None,
                               on_backup=None,
                               on_pre_build=None):
    """
    Will prepare an Android project for deployment with the properties defined by an xml file.

    param xml_path: the path to your XML file
    place_holder_map: a map holding the place holders that appear in the xml file, with their respective definitions.
    The map could be like {'$dynamic_src': '/Users/home/my_dyn_src',
                       '$dynamic_dst': '/Users/home/my_dyn_dst'}
    """
    if place_holder_map is None:
        place_holder_map = {}
    xml = xh.read_xml_file(xml_path)

    bp.manipulate(xml_path, xml, place_holder_map, on_backup, on_pre_build)
