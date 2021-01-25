import os_xml_handler.xml_handler as xh
from os_xml_automation import shared_res as shared_res
from os_xml_automation import shared_tools as shared_tools
from os_android_app_automation.bp import _res as res
import os_file_handler.file_handler as fh
import os
from os_tools import tools as tools
from os_file_stream_handler import file_stream_handler as fsh
import os_android_package_name_changer.name_changer as nc


# manipulate an xcode project by an xml properties file


def set_app_name(project_path, app_name):
    strings_path = os.path.join(project_path, res.PROJECT_STRINGS_FILE)
    strings_xml = xh.read_xml_file(strings_path)
    name_node = xh.get_root_direct_child_nodes(strings_xml, 'string', 'name', 'app_name')[0]
    xh.set_node_text(name_node, app_name)
    xh.save_xml_file(strings_xml, strings_path)


def set_launcher_icons(project_main, launchers_path):
    launcher_icons = fh.search_file(project_main, prefix='ic_launcher', recursive=True)
    fh.remove_files(launcher_icons)

    fh.copy_dir_content(launchers_path, project_main)


def set_assets(project_assets, assets_path):
    fh.remove_dir(project_assets)
    fh.copy_dir_content(assets_path, project_assets)


# will set the app id in the manifest
def set_ad_id(project_manifest, app_ad_id):
    manifest_xml = xh.read_xml_file(project_manifest, {'android': 'http://schemas.android.com/apk/res/android'})
    application_node = xh.get_root_direct_child_nodes(manifest_xml, 'application')[0]
    ad_node = xh.get_child_nodes(application_node, 'meta-data', 'android:name', 'com.google.android.gms.ads.APPLICATION_ID')
    if ad_node:
        xh.set_node_atts(ad_node[0], {'{http://schemas.android.com/apk/res/android}value': app_ad_id})
    else:
        xh.create_and_add_new_node(application_node,
                                   'meta-data', {'{http://schemas.android.com/apk/res/android}name': 'com.google.android.gms.ads.APPLICATION_ID',
                                                 '{http://schemas.android.com/apk/res/android}value': app_ad_id})

    xh.save_xml_file(manifest_xml, project_manifest, add_utf_8_encoding=True)


def get_old_package_name(project_manifest):
    manifest_xml = xh.read_xml_file(project_manifest)
    root_node = xh.get_root_node(manifest_xml)
    return xh.get_node_att(root_node, 'package')


def manipulate(xml_path, xml, place_holder_map, on_backup, on_pre_build):
    root_node = xh.get_root_node(xml)

    shared_tools.add_extension_nodes(xml_path, place_holder_map, root_node, xml)
    # xh.save_xml_file(xml, '/Users/home/Programming/Python/modules/general/os_file_automation/examples/xcode_mapper2.xml')
    project_properties_node = xh.get_child_nodes(root_node, 'project_properties')[0]

    # fetch the project properties
    project_path = xh.get_text_from_child_node(project_properties_node, 'project_path')
    project_path = shared_tools.fill_place_holders(project_path, place_holder_map)

    launchers_path = xh.get_text_from_child_node(project_properties_node, 'launchers_path')
    launchers_path = shared_tools.fill_place_holders(launchers_path, place_holder_map)

    assets_path = xh.get_text_from_child_node(project_properties_node, 'assets_path')
    assets_path = shared_tools.fill_place_holders(assets_path, place_holder_map)

    google_services_path = xh.get_text_from_child_node(project_properties_node, 'google_services_path')
    if google_services_path:
        google_services_path = shared_tools.fill_place_holders(google_services_path, place_holder_map)

    package_name = xh.get_text_from_child_node(project_properties_node, 'package_name')
    version_name = xh.get_text_from_child_node(project_properties_node, 'version_name')
    version_code = xh.get_text_from_child_node(project_properties_node, 'version_code')
    app_ad_id = xh.get_text_from_child_node(project_properties_node, 'app_ad_id')
    app_name = xh.get_text_from_child_node(project_properties_node, 'app_name')

    # build paths
    project_app = os.path.join(project_path, res.PROJECT_APP)
    project_main = os.path.join(project_path, res.PROJECT_MAIN)
    project_assets = os.path.join(project_path, res.PROJECT_ASSETS_DIR)
    project_build_gradle = os.path.join(project_path, res.PROJECT_BUILD_GRADLE_FILE)
    project_manifest = os.path.join(project_path, res.PROJECT_MANIFEST)
    old_package_name = get_old_package_name(project_manifest)

    # # do backup
    # if on_backup:
    #     on_backup(project_path, old_package_name)

    # # set the general properties in the android project
    # set_app_name(project_path, app_name)
    # set_launcher_icons(project_main, launchers_path)
    # set_assets(project_assets, assets_path)

    # todo: enable!
    # nc.change_package_name(project_path, package_name)

    # todo: check if works!
    # if google_services_path:
    #     fh.copy_file(google_services_path, os.path.join(project_app, fh.get_file_name_from_path(google_services_path)))

    # do pre build callback
    if on_pre_build:
        on_pre_build(project_path)

    # set ad id in manifest
    # if app_ad_id:
    #     set_ad_id(project_manifest, app_ad_id)
    #
    # # add dependencies
    # dependencies_nodes = xh.get_child_nodes(root_node, 'gradle_dependencies')
    # if dependencies_nodes:
    #     set_build_gradle_file(project_build_gradle, dependencies_nodes, version_name, version_code)
    #
    # # # start running on all of the steps
    # # run_next_step_cycle(project, root_node, xml_path, place_holder_map, curr_step=1)
    # #
    # # # run pod install
    # # check_and_run_pod_install(xpm, project, project_properties_node)
    # #
    # # print_line()
    # # print('saving...')
    # # xpm.save_changes(project)


# will operate the <pods> tag
def set_build_gradle_file(project_build_gradle, dependencies_nodes, version_name, version_code):
    build_gradle_lines = fsh.read_text_file(project_build_gradle)
    import re

    # copy the first part of the build.gradle file
    build_gradle_output = []
    for line in build_gradle_lines:

        # set the right version name or version code, if required
        if 'versionCode' in line:
            line = re.sub('[.0-9+]', '', line)
            line += f' ${version_code}'
        elif 'versionName' in line:
            line = re.sub('[".0-9+]', '', line)
            line += f' "${version_name}"'
        build_gradle_output.append(line)
        if 'dependencies {' in line:
            break

    # add the dependencies
    for dependency_node in dependencies_nodes:
        text = xh.get_text_from_node(dependency_node)
        build_gradle_output.append(text)

    fsh.write_file(project_build_gradle + "2", build_gradle_output)


#
# # operate the next step
# def run_next_step_cycle(project, root_node, xml_path, place_holder_map, curr_step):
#     next_step_node = xh.get_child_nodes(root_node, f'{shared_res.NODE_STEP}_{str(curr_step)}')
#
#     # if the next step exists, start running on all of the direct children
#     if next_step_node:
#         print_line()
#         print(f'Starting step: {str(curr_step)}')
#         next_step_node = next_step_node[0]
#         for curr_step_child_node in xh.get_all_direct_child_nodes(next_step_node):
#             curr_step_tag = curr_step_child_node.tag
#
#             # if link
#             if curr_step_tag == res.NODE_LINK:
#                 do_link_tag(project, xml_path, place_holder_map, curr_step_child_node)
#
#             # if unlink
#             elif curr_step_tag == res.NODE_UNLINK:
#                 do_unlink_tag(project, place_holder_map, curr_step_child_node)
#
#             # if pods
#             elif curr_step_tag == res.NODE_PODS:
#                 do_pods_tag(project, place_holder_map, curr_step_child_node)
#
#             # if frameworks
#             elif curr_step_tag == res.NODE_FRAMEWORKS:
#                 do_frameworks_tag(project, place_holder_map, curr_step_child_node)
#
#             elif curr_step_tag == res.NODE_RUN_TEXT_MAPPER:
#                 do_run_text_mapper_tag(xml_path, place_holder_map, curr_step_child_node)
#
#         print('done!')
#         run_next_step_cycle(project, root_node, xml_path, place_holder_map, curr_step + 1)
#
#
# # will operate the <unlink> tag
# def do_unlink_tag(project, place_holder_map, node):
#     from os_xcode_tools import xcode_project_manipulator as xpm
#     node_path = xh.get_text_from_node(node)
#     node_path = shared_res.fill_place_holders(node_path, place_holder_map)
#     node_type = xh.get_node_att(node, res.NODE_UNLINK_ATT_TYPE)
#     if node_type == res.NODE_UNLINK_ATT_TYPE_VAL_DIR:
#         node_group = xpm.get_or_create_group(project, path_to_group=node_path)
#         xpm.remove_group(project, node_group)
#     elif node_type == res.NODE_UNLINK_ATT_TYPE_VAL_FILE:
#         node_group = xpm.get_or_create_group(project, path_to_group=fh.get_parent_path(node_path))
#         xpm.remove_file_from_group(project, node_group, fh.get_file_name_from_path(node_path))
#
#     if xh.get_node_att(node, res.NODE_UNLINK_ATT_DELETE) == res.XML_TRUE:
#         project_grandpa_path = os.path.join(xpm.get_project_root(project), '..')
#         path_to_delete = os.path.join(project_grandpa_path, node_path)
#         if fh.is_dir_exists(path_to_delete):
#             fh.remove_dir(path_to_delete)
#         elif fh.is_file_exists(path_to_delete):
#             fh.remove_file(path_to_delete)
#
#
# # will operate the <link> tag
# def do_link_tag(project, xml_path, place_holder_map, link_node):
#     # get the src <file_src> or the <dir_src> (from the computer's path)
#     from os_xcode_tools import xcode_project_manipulator as xpm
#     if xh.get_child_nodes(link_node, shared_res.NODE_DIR_SRC):
#
#         # dir copy
#         src_text = shared_res.get_file_node_path(xml_path, place_holder_map, link_node, shared_res.NODE_DIR_SRC, file_search=False)
#         dst_node = xh.get_child_nodes(link_node, shared_res.NODE_DIR_DST)[0]
#         dst_text = xh.get_text_from_child_node(dst_node, 'path')
#         dst_text = shared_res.fill_place_holders(dst_text, place_holder_map)
#         xpm.add_dir(project, src_text, dst_text)
#
#     else:
#
#         # file copy
#         src_text = shared_res.get_file_node_path(xml_path, place_holder_map, link_node, shared_res.NODE_FILE_SRC, file_search=True)
#         dst_node = xh.get_child_nodes(link_node, shared_res.NODE_FILE_DST)[0]
#         dst_text = xh.get_text_from_child_node(dst_node, 'path')
#         dst_text = shared_res.fill_place_holders(dst_text, place_holder_map)
#         file_group = xpm.get_or_create_group(project, fh.get_parent_path(dst_text))
#         xpm.add_file_to_group(project, src_text, file_group)
#
#
# # will operate the <frameworks> tag
# def do_frameworks_tag(project, place_holder_map, frameworks_node):
#     # get all of the frameworks
#     framework_dict_list = []
#     for framework_node in xh.get_all_direct_child_nodes(frameworks_node):
#         framework_path = xh.get_text_from_child_node(framework_node, 'path')
#         framework_path = shared_res.fill_place_holders(framework_path, place_holder_map)
#         framework_type = xh.get_text_from_child_node(framework_node, 'type')
#
#         framework_dict_list.append(
#             {
#                 'type': framework_type,
#                 'path': framework_path,
#             }
#         )
#
#     from os_xcode_tools import xcode_project_manipulator as xpm
#     xpm.set_frameworks(project, framework_dict_list)
#
#
# # will operate the <run_text_mapper> tag
# def do_run_text_mapper_tag(xml_path, place_holder_map, curr_step_child_node):
#     req_place_holder_map = xh.get_child_nodes(curr_step_child_node, res.NODE_PLACE_HOLDER_MAP)
#
#     # if a dictionary exists in the xml, build it in code
#     text_mapper_place_holder_map = None
#     if req_place_holder_map:
#         text_mapper_place_holder_map = {}
#         req_place_holder_map = req_place_holder_map[0]
#         for arg in xh.get_all_direct_child_nodes(req_place_holder_map):
#             key = xh.get_text_from_child_node(arg, res.NODE_KEY)
#             val = xh.get_text_from_child_node(arg, res.NODE_VALUE)
#             val = shared_res.fill_place_holders(val, place_holder_map)
#             text_mapper_place_holder_map[key] = val
#
#     src_path = shared_res.get_file_node_path(xml_path, place_holder_map, curr_step_child_node, shared_res.NODE_FILE_SRC, file_search=True)
#     from os_file_automation.xml_mapper import xml_mapper as xm
#     xm.set_texts_by_xml(src_path, text_mapper_place_holder_map)


def print_line():
    print('-----------------------------------------------------------------------')
