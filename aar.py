# coding=utf-8

# 提取AAR包中的资源 包括jar和res

import os
import sys
import xml.dom.minidom
import shutil
import zipfile

reload(sys)
sys.setdefaultencoding('utf-8')


def export_aar(aar_dir,export_dir):
    packaged_dependencies = []
    packaged_resources = []
    for aar in os.listdir(aar_dir):
        folder_name, ext = os.path.splitext(aar)
        if ext != '.aar':
            continue
        aar_path = os.path.join(aar_dir, aar)
        zip_file = zipfile.ZipFile(aar_path, 'r')
        lib_names = []
        res_names = []
        for name in zip_file.namelist():
            if name.startswith('libs/'):
                lib_names.append(name)
            if name.startswith('res/'):
                res_names.append(name)
        export_path = os.path.join(export_dir, folder_name)
        zip_file.extractall(export_path, lib_names)
        zip_file.extractall(export_path, res_names)

        data = zip_file.read('AndroidManifest.xml')
        DOMTree = xml.dom.minidom.parseString(data)
        collection = DOMTree.documentElement
        package_name = collection.getAttribute("package")

        jar_dir = os.path.join(export_path,'libs')
        res_dir = os.path.join(export_path,'res')

        for name in os.listdir(jar_dir):
            packaged_dependencies.append(name)
            jar_path = os.path.join(jar_dir,name)
            shutil.move(jar_path,os.path.join(export_dir))
        shutil.rmtree(jar_dir)

        if os.path.exists(res_dir):
            packaged_resources.append({'packageName': package_name, 'folderName': folder_name + "-res"})
            shutil.move(res_dir,os.path.join(export_dir, folder_name + "-res"))

        shutil.rmtree(export_path)

    a1 = ''
    a2 = ''

    for i in packaged_dependencies:
        a1 += '''
        <packagedDependency>{0}</packagedDependency>'''.format(i)
    for i in packaged_resources:
        a2 += '''
        <packagedResource>
            <packageName>{0}</packageName>
            <folderName>{1}</folderName>
        </packagedResource>'''.format(i['packageName'], i['folderName'])

    a3 = '''
<platform xmlns="http://ns.adobe.com/air/extension/32.0">
    <packagedDependencies>{0}
    </packagedDependencies>
    <packagedResources>{1}
    </packagedResources>
</platform>'''.format(a1, a2)

    f = open(os.path.join(export_dir, 'platform.xml'), 'w')
    f.write(a3)
    f.flush()
    f.close()


dir = '/Users/yangjin1/Downloads/360'
export = '/Users/yangjin1/Downloads/export'

export_aar(dir,export)
