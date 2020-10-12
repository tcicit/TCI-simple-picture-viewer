#!/usr/bin/env python

"""
Simple Image Browser based on PySimpleGUI and pillow
---------------------------------------------------
Autor: Thomas Cigolla
Web: cigolla.ch
Version: 0.5
Date: 13.09.2020

Das Programm ermöglicht es einen Folder mit Bildern einfach zu durchsuchen 
und gute Bilder in einen neuen Folder zu kopieren.
Das Programm ist aus meinem Bedürfnis entstanden grosse Mengen an Bildern 
schnell zu durchsuchen und zu bewerten.
Das Programm kann über das Keeboard gesteuert werden.
c = Copy
m = Move
r = Rotate

Das Programm arbeitet wie es ist. Es wird keine Granite übernommen.

Das Programm basiert auf dem Code von imgae-browser aus dem pySimpleGui Repositorien.

Geplante Erweiterungen
----------------------
* Bildschirm kann vergrössert / verkleinert werden
* Mehr Attribute
* Vorschau mit Tumpnails
* Wechsel des Folders innerhalb des Programms
* Spalsh-Screen
* etc.

Limitation:
------------

PIL.Image.DecompressionBombError: Image size (220473013 pixels) exceeds limit of 178956970 pixels, could be decompression bomb DOS attack.

"""

import os
import io
import PySimpleGUI as sg
import shutil
from sys import exit
from PIL import Image, ImageTk

sg.theme('dark grey 9')
# ------------------------------------------------------------------------------
# Get folders 
# ------------------------------------------------------------------------------
layout_popup = [[sg.Text('Chose input folder and output folders')],
                [sg.Text("Input Path:", size=(15, 1)), sg.InputText(default_text=os.getcwd(),size=(80, 1)), sg.FolderBrowse(), sg.Checkbox('Include subfolders')],
                [sg.Text("Output Path:", size=(15, 1)), sg.InputText(default_text=os.getcwd()+ "/good_files",size=(80, 1)), sg.FolderBrowse()],
                [sg.Text("Move Path:", size=(15, 1)), sg.InputText(default_text=os.getcwd()+ "/moved_files",size=(80, 1)), sg.FolderBrowse()],
                [sg.Submit(size=(15, 2)), sg.Cancel(size=(15, 2))]]

window = sg.Window('Folders', layout_popup, icon="tci-simple-image-viewer.ico" )

event, values_popup = window.read()
window.close()

input_folder = values_popup[0]     # the first input element is values[0]
inc_sub_folder = values_popup[1]
output_folder = values_popup[2]     
move_folder = values_popup[3]


if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(move_folder):
    os.makedirs(move_folder)    

# PIL supported image types
img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

# get list of files in input folder(s)
fnames = []
if inc_sub_folder == False:
    flist0 = os.listdir(input_folder)
    for file in flist0:
        file.lower()
        fpath = os.path.join(input_folder, file)
        if os.path.isfile(fpath):
            if (file.endswith(img_types)):
                fnames.append(os.path.join(fpath))   
else:
    for path, directories, files in os.walk(input_folder):
        for file in files:
            file.lower()
            if (file.endswith(img_types)):
                fnames.append(os.path.join(path, file))


num_files = len(fnames)                # number of iamges found
print (num_files)
print (fnames)
if num_files == 0:
    sg.popup('     No files in input folder       ', icon="tci-simple-image-viewer.ico")
    raise SystemExit()

# ------------------------------------------------------------------------------
def next_file(i, num_files, input_folder, fnames):
    """
    Funktion for readin next File
    """
    if i >= num_files:
        i = 0
    file_name = os.path.join(input_folder, fnames[i])
    return file_name, i
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# use PIL to read data of one image
# ------------------------------------------------------------------------------
def get_img_data(filename, maxsize=(800, 600), first=False, rotate=0 ):
    """Generate image data using PIL
    """ 
    
    img = Image.open(filename)
         
    if (rotate > 0):
        img = img.rotate(rotate, expand=True)
    
    img.thumbnail(maxsize)   
    
    
    # if first:                     # tkinter is inactive the first time
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()
       
    #return ImageTk.PhotoImage(img)
# ------------------------------------------------------------------------------

def get_img_attribute(filename):
    img = Image.open(filename)
    width, height = img.size
    
    return width, height
# -------------------------------------------------------------------------------
    

# make these 2 elements outside the layout as we want to "update" them later
# initialize to the first file in the list
filename = os.path.join(input_folder, fnames[0])  # name of first file in list
image_elem = sg.Image(data=get_img_data(filename, first=True))

filename_display_elem = sg.Text(filename, size=(80, 1))
file_num_display_elem = sg.Text('File 1 of {}'.format(num_files), size=(15, 1))
file_size_byte = sg.Text('File Size (Byte): ' + str(os.stat(filename).st_size), size=(25, 1))

width, height = get_img_attribute(filename)
file_img_width = sg.Text('Width: ' + str(width), size=(15, 1))
file_img_height = sg.Text('Height: ' + str(height), size=(15, 1))
# define layout, show and read the form


colums = [        
            [
             filename_display_elem
            ],
            [
             file_num_display_elem, file_size_byte, file_img_width, file_img_height
            ],
            [
             sg.Button('<<< Prev', size=(10, 2)), 
             sg.Button('Next >>>', size=(10, 2)), 
             sg.Button('Copy (c)', size=(10, 2), key='copy'), 
             sg.Button('Rotate (r)', size=(10, 2), key='rotate'),
             sg.Button('Move (m)', size=(10, 2), key='move'),
             sg.Button('Delete', size=(10, 2)),
             sg.Button('Close', size=(10, 2))
            ],
            [
             image_elem
            ]
        ]

layout = [[sg.Column(colums)]]

window = sg.Window('Image Browser', 
                    layout, 
                    return_keyboard_events=True,
                    location=(0, 0), 
                    use_default_focus=False,
                    resizable=True,
                    text_justification="center",
                    icon="tci-simple-image-viewer.ico"
                    )

#size=(825,725)


# loop reading the user input and displaying image, filename
i = 0
r = 0
rotate_angle = 0

while True:
    # read the form
    event, values = window.read()
    # print(event, values)
    
    # perform button and keyboard operations
    if event == sg.WIN_CLOSED or event == 'Close':
        break
    elif event in ('Next >>>', 'MouseWheel:Down', 'Down:40', 'Next:34', 'Right:39'):
        i += 1
        filename, i = next_file(i, num_files, input_folder, fnames)
       
    elif event in ('<<< Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33', 'Left:37'):
        i -= 1
        if i < 0:
            i = num_files + i
        filename = os.path.join(input_folder, fnames[i])
        
    elif event in ('copy','c'):
        # adding exception handling
        try:
            shutil.copyfile(os.path.join(input_folder, fnames[i]), os.path.join(output_folder, fnames[i]))
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
 
        # print("\nFile copy done!\n")
        
        i += 1
        filename, i = next_file(i, num_files, input_folder, fnames)
        
    elif event in ('rotate', 'r'):
        if r == 0:
            rotate_angle = 90
            r += 1
        elif r == 1:
           rotate_angle = 180
           r += 1
        elif r == 2:
           rotate_angle = 270
           r += 1
        else:
           rotate_angle = 0
           r = 0
 
    elif event in ('move', 'm'):
        
        try:
            shutil.move(os.path.join(input_folder, fnames[i]), os.path.join(move_folder, fnames[i]))
        except IOError as e:
            print("Unable to move file. %s" % e)
            exit(1)
 
        i += 1
        filename, i = next_file(i, num_files, input_folder, fnames)
                
    elif event in ('Delete'):
              
        layout_popup = [[sg.Text('Do you want to delete the file?')],
                        [sg.Submit("OK", size=(15, 2)), sg.Cancel("Cancel", size=(15, 2))]]

        windowOkCancel = sg.Window('OK / Cancel', layout_popup, icon="tci-simple-image-viewer.ico" )

        while True:
            # read the form
            eventOkCancel, valuesOkCancel = windowOkCancel.read()
            # print(eventOkCancel, valuesOkCancel)
    
            # perform button and keyboard operations
            if eventOkCancel in ('OK'):
                # remove File
                try:
                    print ("Delete File")
                    #os.remove(os.path.join(input_folder, fnames[i]))
                except IOError as e:
                    print("Unable to copy file. %s" % e)
                    sg.popup("Can't delete File.", icon="tci-simple-image-viewer.ico")
            windowOkCancel.close() 
     
    else:
        filename = os.path.join(input_folder, fnames[i])

    # update window with new image
    image_elem.update(data=get_img_data(filename, first=False, rotate=rotate_angle))
    rotate_angle = 0
    # update window with filename
    filename_display_elem.update(filename)
    # update page display
    file_num_display_elem.update('File {} of {}'.format(i+1, num_files))
    # update file information
    file_size_byte.update('File Size (Byte): ' + str(os.stat(filename).st_size))
    width, height = get_img_attribute(filename)
    file_img_width.update('Width: ' + str(width))
    file_img_height.update('Height: ' + str(height))

window.close()
