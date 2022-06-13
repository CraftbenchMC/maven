#!/usr/bin/env python3

import os
import pathlib
import collections
import zipfile

from pathlib import Path

def createIndex(path: str, relative: str, files: {}):
    breadcrumbs = f'<a href="{relative}" class="breadcrumb">maven</a><p class="divider">/</p>'
    _files = f"""
        <a href="{relative}">
            <li>
                <img src="{relative}icons/back.svg" />
                <p>..</p>
            </li>
        </a>
    """

    parts = path.split("/")
    
    if len(parts) > 0 and path != "":
        for (index, part) in enumerate(parts):
            previous = "/".join(parts[:index])
            breadcrumbs += f'<a href="{relative}{previous}/{part}" class="breadcrumb">{part}</a><p class="divider">/</p>'
    
    for (key, val) in files.items():
        trail = ""

        if val == "folder":
            trail = "/"

        _files += f"""
            <a href="{key}{trail}">
                <li>
                    <img src="{relative}icons/{val}.svg" />
                    <p>{key}{trail}</p>
                </li>
            </a>
        """
    
    title = "/" + path
    if path == "":
        title = "/"
    
    return f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link href="{relative}css/index.css" rel="stylesheet" />
        <title>Index of {title}</title>
    </head>
    <body>
        <main>
            <div class="breadcrumbs">
                {breadcrumbs}
            </div>
            <ul>
                {_files}
            </ul>
        </main>
    </body>
</html>
    """

def findIndexFiles():
    _files = list(pathlib.Path(os.getcwd()).glob("**/index.html"))
    files = []
    for file in _files:
        files.append(file.as_posix())
    return files

def deleteIndexFiles():
    indexFiles = findIndexFiles()
    for file in indexFiles:
        os.remove(file)

def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()

def createIndexFiles(root = os.getcwd()):
    __folders = os.listdir(root)
    _folders = []

    for folder in __folders:
        if not folder.startswith(".") and os.path.isdir(folder):
            _folders.append(root + "/" + folder)

            hasSubDirectory = False

            for file in os.listdir(root + "/" + folder):
                if os.path.isdir(root + "/" + folder + "/" + file):
                    hasSubDirectory = True
            
            if hasSubDirectory:
                for (dirroot, subdirs, files) in os.walk(root + "/" + folder):
                    for subdir in subdirs:
                        _folders.append(dirroot + "/" + subdir)
    
    folders = []
    folderDict = {}
    
    for _folder in _folders:
        folder = _folder.replace(os.getcwd() + "/", "")
        folders.append(folder)
        relative = "../" * len(folder.split("/"))
        
        folderDict[folder] = relative
    
    for (key, val) in folderDict.items():
        files = {}
        
        for file in os.listdir(key):
            if not file.startswith("."):
                if os.path.isdir(key + "/" + file):
                    files[file] = "folder"
                else:
                    files[file] = "file"
                    if "javadoc" in file and file.endswith(".jar"):
                        with zipfile.ZipFile(key + "/" + file, "r") as zipf:
                            if os.path.exists(key + "/" + file + ".d"):
                                rmdir(key + "/" + file + ".d")
                            
                            os.mkdir(key + "/" + file + ".d")
                            zipf.extractall(key + "/" + file + ".d")
        
        index = createIndex(key, val, files)
        
        if not os.path.exists(key + "/index.html"):
            with open(key + "/index.html", "w") as file:
                file.write(index)
                file.close()
    
    files = {}
        
    for file in os.listdir("."):
        if not file.startswith("."):
            if os.path.isdir(file):
                files[file] = "folder"
            else:
                files[file] = "file"
        
    index = createIndex("", "./", files)
        
    with open("index.html", "w") as file:
        file.write(index)
        file.close()

deleteIndexFiles()
createIndexFiles()
