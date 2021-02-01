Introduction
------------

This module aim to assist with an Android app buildup.

To use, create an XML file with your app properties and run.

## Installation
Install via pip:

    pip install os-android-app-automation

## Usage:

Create an XML file with your app properties:

- [xml example 1](/examples/example_1.xml):
```xml
<android_mapper>

    <!-- will hold all of the project settings -->
    <settings>
        <!-- toggle this to true if you want to create a copy of your project and let the automation run on it, instead of the original project -->
        <work_on_project_alias>false</work_on_project_alias>
    </settings>

    <!-- will hold all of the project properties -->
    <project_properties>
        
        <project_path>/path/to/Android/studio/project</project_path>

        <!-- you can also set placeholders here, for any of the below properties, and define them during runtime like so -->
        <!--<project_path>$android_project_path</project_path>-->
        

        <!-- if you have admob in your app, set here the admob id -->
        <app_ad_id>ca-app-pub-32050407656945904~1094096384</app_ad_id>
        <google_services_path>/path/to/google-services.json</google_services_path>
        <package_name>com.company_name.product_name</package_name>
        <app_name>App Name</app_name>
        <version_code>1</version_code>
        <version_name>1.0</version_name>

        <!-- set the launchers you want to copy to your project.
         The path should be look like so:
         main::
            ic_launcher-playstore.png
            res:
                mipmap-anydpi-v26:
                    ic_launcher_round.xml
                    ic_launcher.xml
                mipmap-hdpi:
                    ic_launcher_round.xml
                    ic_launcher.xml
                ... all the rest of the mipmaps ....
                values:
                    ic_launcher_background.xml
         -->
        <launchers_path>/path/to/app/launcher/files/main</launchers_path>

        <!-- if you want to copy some assets to your project, set it here -->
        <assets_path>/path/to/assets</assets_path>
    </project_properties>


    <!-- set here all of the modules you want to add to the project -->
    <added_modules>
        <module>module_1</module>
        <module>module_2</module>
        <module>module_3</module>
    </added_modules>


    <!-- set any gradle dependencies here -->
    <gradle_dependencies>
        implementation 'org.jetbrains.kotlin:kotlin-stdlib:$kotlin_version'
        implementation 'androidx.core:core-ktx:1.3.2'
        implementation 'androidx.appcompat:appcompat:1.2.0'
        implementation 'com.google.android.material:material:1.2.1'

        // gson
        implementation 'com.google.code.gson:gson:2.8.6'

        // glide
        implementation 'com.github.bumptech.glide:glide:4.11.0'
        kapt 'com.github.bumptech.glide:compiler:4.11.0'

        // all of the other dependencies...
    </gradle_dependencies>
</android_mapper>
```
After your created the XML file, call it from code:

    from os_android_app_automation import app_automation 

    app_automation.set_android_project_by_xml(xml_path='path/to/xml/file.xml',
                                  place_holder_map={'$project_path': 'path/to/android/project'}, # optional define in runtime
                                  on_backup=on_backup,                  // optional call back here
                                  on_pre_build=on_pre_build             // optional callback here
    )

    # optional callbacks:

    # this callback will be fired before the process begins. You can clear files, remove directories and etc...
    # notice that the package name here is the old package name of the project (the automation didn't changed anything yet)
    def on_backup(project_path, old_package_name):
        pass

    # this callback will be fired right before the build will commence. i.e. after package name change, assets copy and essentially, before apk/bundle creation 
    def on_pre_build(project_path, package_name):
        pass


# Advanced Usage:

You can also extend an XML file to another one.

Inheritance in this sense can help you if you're interested in sharing a behaviour between a bunch of XML files.

- [child xml](/examples/child_xml_example.xml):
```xml
<!-- Notice the extension at the top. Here we will define the path to the parent mapper xml -->
<android_mapper extension_mapper_path="$android_shared_mapper">
    <project_properties>
        <app_ad_id>ca-app-pub-12345678798~546</app_ad_id>
        <package_name>com.osfunapps.my_package_name</package_name>
        <app_name>MyAppName</app_name>
        <version_code>12</version_code>
        <version_name>1.2</version_name>
    </project_properties>

    <!-- will add more modules, they will be merged with the parent modules -->
    <added_modules>
        <module>another_module</module>
    </added_modules>

    <!-- will add more dependencies, they will be merged with the parent modules -->
    <gradle_dependencies>
        implementation 'com.squareup.okhttp3:okhttp:4.9.0'
    </gradle_dependencies>
</android_mapper>
```

- [parent xml](/examples/parent_xml_example.xml):
```xml
<android_mapper>

    <settings>
        <work_on_project_alias>false</work_on_project_alias>
    </settings>

    <project_properties>
        <project_path>/path/to/project</project_path>
        <google_services_path>/path/to/google/services.json</google_services_path>
        <launchers_path>/path/to/launcher/directories</launchers_path>
        <assets_path>/path/to/assets</assets_path>
    </project_properties>

    <added_modules>
        <module>module_1</module>
        <module>module_2</module>
        <module>module_3</module>
        <!-- the rest of the modules will come from the child -->
    </added_modules>

    <gradle_dependencies>
        implementation "org.jetbrains.kotlin:kotlin-stdlib:$kotlin_version"
        implementation 'androidx.core:core-ktx:1.3.2'
        implementation 'androidx.appcompat:appcompat:1.2.0'

        // the rest of the modules dependencies will come from the child

    </gradle_dependencies>
</android_mapper>
```

That's it. Now you can just call the xml of the child (if you set placeholders in the xml, don't forget to set them when you call the function).


And more...


## Links
[GitHub - osapps](https://github.com/osfunapps)

## Licence
ISC