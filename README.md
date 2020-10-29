# TCI Simple Picture Viewer

With this program it is possible to quickly and easily search a folder for good images and copy the images. 

The program is written in Python and pysimplegui. 

The program is my first attempt to create a simple interface for python. 

## Prerequisites

* Python 3.x
* PySimpleGUI (https://pypi.org/project/PySimpleGUI/)
  * pip install pysimplegui
* pillow (https://pillow.readthedocs.io/en/stable/installation.html)
  * pip install --upgrade pip
  * pip install --upgrade Pillow
  
 ## Compailing windows exe (https://www.pyinstaller.org/)
 I used pyinstaller to build the windows program.
 
 Command for compiling: pyinstaller -wF tci-simple-image-viewer.py
 
 ## Download Windows EXE-File
 https://github.com/tcicit/TCI-simple-picture-viewer/releases


## Configure Folders

![grafik](![grafik](https://user-images.githubusercontent.com/12540138/97572911-4758ac00-19e9-11eb-8e3b-a9921e4da023.png))

f no Output and Move Path is specified, the folders in the working directory are created automatically.

## View, Copy or Move Images

![grafik](https://user-images.githubusercontent.com/12540138/93336313-e48bc680-f827-11ea-9b45-7c09a55a9f81.png)

The keyboard can be used for scrolling, copying, moving and rotating.
* Next - Right arrow key
* Prev - Left arrow key
* Copy - c key
* Rotate - r key
* Move -  m key

The Delet button deletes the file irreversibly. 
