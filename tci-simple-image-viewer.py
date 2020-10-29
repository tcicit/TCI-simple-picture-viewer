#!/usr/bin/env python

"""
Simple Image Browser based on PySimpleGUI and pillow
----------------------------------------------------

Autor: Thomas Cigolla
Web: cigolla.ch
Version: 0.6
Date: 21.10.2020

Limitation:
------------

PIL.Image.DecompressionBombError: Image size (220473013 pixels) exceeds limit of 178956970 pixels,
could be decompression bomb DOS attack.

"""
import os
import io
import PySimpleGUI as sg
import shutil
from sys import exit
from PIL import Image, ImageTk

# Programm Setings
sg.theme('dark grey 9')

# global Variables
input_folder = os.getcwd()
inc_sub_folder = False
output_folder = os.getcwd() + "/good_files"
move_folder = os.getcwd() + "/moved_files"
num_files = 0
file_names = []
image_elements = {}
filename = ""

# ------------------------------------------------------------------------------
# Get folders 
# ------------------------------------------------------------------------------
def get_folders():
    ''' 
        make input window for file path
    '''

    global input_folder 
    global inc_sub_folder 
    global output_folder 
    global move_folder 

    layout_popup = [[sg.Text('Chose input folder and output folders')],
                    [sg.Text("Input Path:", size=(15, 1)), sg.InputText(default_text=input_folder,size=(80, 1)), sg.FolderBrowse(), sg.Checkbox('Include subfolders', default=inc_sub_folder)],
                    [sg.Text("Output Path:", size=(15, 1)), sg.InputText(default_text=output_folder,size=(80, 1)), sg.FolderBrowse()],
                    [sg.Text("Move Path:", size=(15, 1)), sg.InputText(default_text=move_folder,size=(80, 1)), sg.FolderBrowse()],
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
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# get image files from folder(s)
# -------------------------------------------------------------------------------
def get_files():
    '''
        get all file names and path, filter by extension
    '''
    global file_names
    global num_files

    del file_names[:]
    num_files = 0

    # PIL supported image types
    img_types = (".png", ".jpg", "jpeg", ".tiff", ".bmp")

    if inc_sub_folder == False:
        flist0 = os.listdir(input_folder)
        for file in flist0:
            file.lower()
            fpath = os.path.join(input_folder, file)
            if os.path.isfile(fpath):
                if (file.endswith(img_types)):
                    file_names.append(file)   
    else:
        for path, directories, files in os.walk(input_folder):
            for file in files:
                file.lower()
                if (file.endswith(img_types)):
                        file_names.append(file)


    num_files = len(file_names)                # number of iamges found

    if num_files == 0:
        sg.popup('     No files in input folder       ', icon="tci-simple-image-viewer.ico")
        raise SystemExit()
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# read next file in list
# -------------------------------------------------------------------------------
def next_file(i, num_files, input_folder, file_names):
    """
    Funktion for readin next File
    """
    if i >= num_files:
        i = 0
    file_name = os.path.join(input_folder, file_names[i])
    return file_name, i
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# use PIL to read data of one image
# ------------------------------------------------------------------------------
def get_img_data( maxsize=(800, 600), first=False, rotate=0 ):
    """
        Generate image data using PIL
    """ 
    global filename

    img = Image.open(filename)
         
    if (rotate > 0):
        img = img.rotate(rotate, expand=True)
    
    img.thumbnail(maxsize)   
        
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()  
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# read image arttribute from file
# ------------------------------------------------------------------------------
'''
  get image attribute from file
'''
def get_img_attribute():

    global filename 

    img = Image.open(filename)
    width, height = img.size
    
    return width, height
# -------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
#  read first image from list
# ------------------------------------------------------------------------------
'''
    read first image from list on start 
'''
def get_first_image(image_elements):
    # make these 2 elements outside the layout as we want to "update" them later
    # initialize to the first file in the list
    global filename

    filename = os.path.join(input_folder, file_names[0])  # name of first file in list
    image_elements["image_elem"] = sg.Image(data=get_img_data(first=True))

    image_elements["filename_display_elem"] = sg.Text(filename, size=(80, 1))
    image_elements["file_num_display_elem"] = sg.Text('File 1 of {}'.format(str(num_files)), size=(15, 1))
    image_elements["file_size_byte"] = sg.Text('File Size (Byte): ' + str(os.stat(filename).st_size), size=(25, 1))

    width, height = get_img_attribute()
    image_elements["file_img_width"] = sg.Text('Width: ' + str(width), size=(15, 1))
    image_elements["file_img_height"] = sg.Text('Height: ' + str(height), size=(15, 1))

    return image_elements

# -------------------------------------------------------------------------------
# -------------------------- END Functions --------------------------------------
# -------------------------------------------------------------------------------


get_folders()
get_files()
get_first_image(image_elements)

i = 0
r = 0
rotate_angle = 0

# Main Window
# define layout, show and read the form

image_elem = image_elements["image_elem"] 
filename_display_elem = image_elements["filename_display_elem"]
file_num_display_elem = image_elements["file_num_display_elem"]
file_size_byte = image_elements["file_size_byte"]
file_img_width = image_elements["file_img_width"]
file_img_height = image_elements["file_img_height"]

menu_def = [['&File',[ '&Properties', 'E&xit']],
            ['&Help', ['&Hints', '&About']], ]

colums = [  
            [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],      
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

# loop reading the user input and displaying image, filename, etc.
while True:
    # read the form
    event, values = window.read()
   
    # perform button and keyboard operations
    if event == sg.WIN_CLOSED or event == 'Close' or event == 'Exit':
        break
    elif event in ('Next >>>', 'MouseWheel:Down', 'Down:40', 'Next:34', 'Right:39'):
        i += 1
        filename, i = next_file(i, num_files, input_folder, file_names)
       
    elif event in ('<<< Prev', 'MouseWheel:Up', 'Up:38', 'Prior:33', 'Left:37'):
        i -= 1
        if i < 0:
            i = num_files + i
        filename = os.path.join(input_folder, file_names[i])
        
    elif event in ('copy','c'):
        # adding exception handling
        try:
            shutil.copyfile(os.path.join(input_folder, file_names[i]), os.path.join(output_folder, file_names[i]))
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
 
        i += 1
        filename, i = next_file(i, num_files, input_folder, file_names)
        
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
            shutil.move(os.path.join(input_folder, file_names[i]), os.path.join(move_folder, file_names[i]))
        except IOError as e:
            print("Unable to move file. %s" % e)
            exit(1)
 
        i += 1
        filename, i = next_file(i, num_files, input_folder, file_names)
                
    elif event in ('Delete'):
              
        layout_popup = [[sg.Text('Do you want to delete the file?')],
                        [sg.Submit("OK", size=(15, 2)), sg.Cancel("Cancel", size=(15, 2))]]

        windowOkCancel = sg.Window('OK / Cancel', layout_popup, icon="tci-simple-image-viewer.ico" )

        while True:
            # read the form
            eventOkCancel, valuesOkCancel = windowOkCancel.read()
                
            # perform button and keyboard operations
            if eventOkCancel in ('OK'):
                # remove File
                try:
                    print ("Delete File")
                    #os.remove(os.path.join(input_folder, file_names[i]))
                except IOError as e:
                    print("Unable to copy file. %s" % e)
                    sg.popup("Can't delete File.", icon="tci-simple-image-viewer.ico")
            windowOkCancel.close() 

    elif event in ('Hints'):
        help_txt = '''The program allows you to easily browse a folder with images and copy good images to a new folder.
The program was born out of my need to quickly search and evaluate large amounts of images.
The program can be controlled via the keeboard.

            c = Copy
            m = Move
            r = Rotate'''

        sg.popup('HELP', help_txt )

    elif event in ('About'):

        about_txt = '''Version 0.6 '''

        sg.popup('About', about_txt )

     
    else:
        filename = os.path.join(input_folder, file_names[i])

    if event in ('Properties'):  # renew list after path chnage
        get_folders()
        get_files()
        
        i = 0
        r = 0
 
        filename = os.path.join(input_folder, file_names[0])  # name of first file in list
        image_elem.update(data=get_img_data(first=True, rotate=rotate_angle))
 
    else:
        
        image_elem.update(data=get_img_data(first=False, rotate=rotate_angle))

    filename_display_elem.update(filename)
    file_num_display_elem.update('File {} of {}'.format(i+1, num_files))
    file_size_byte.update('File Size (Byte): ' + str(os.stat(filename).st_size))
    width, height = get_img_attribute()
    file_img_width.update('Width: ' + str(width))
    file_img_height.update('Height: ' + str(height))
    rotate_angle = 0

window.close()
