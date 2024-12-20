#
# Usage: this script converts all of the images located in _img/<folder>
#        to responsive sizes and places them into assets/img/<folder>. Behavior
#        beyond the default behavior can be referenced by running this script with
#        the --help or -h options.
#
# Requirements: the pillow image manipulation package
#               install by running in the command line:
#               python -m pip install pillow
#

from __future__ import print_function
from __future__ import division
from builtins import input

import sys
import os
import shutil
from glob import glob
import argparse

is_win = 'win' in sys.platform

try:
    from PIL import Image
except:
    print("Cannot import PIL. Try:")
    print("\npython -m pip install Pillow\n")
    if is_win:
        print("If you need permission to install, open cmd as administrator")
    else:
        print("If you need permission, instead run")
        print("\nsudo python -m pip install Pillow\n")
    
    print("If you run python with a command other than 'python', replace 'python' with the command you use above.\n")

    exit(1)

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    if is_win:
        HEADER = ''
        OKBLUE = ''
        OKGREEN = ''
        WARNING = ''
        FAIL = ''
        ENDC = ''
        BOLD = ''
        UNDERLINE = ''

resize_widths = {
    "placehold" : 230,
    "thumb" : 535,
    "thumb@2x" : 535 * 2,
    "xs" : 575,
    "sm" : 767,
    "md" : 991,
    "lg" : 1999,
    "self" : -1
}

def make_dir(save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

def update(msg):
    print(colors.OKBLUE + msg + colors.ENDC)

def warn(msg):
    msg_lines = msg.split("\n")
    print("    " + colors.WARNING + "WARNING: " + msg_lines[0] + colors.ENDC)
    for msg_line in msg_lines[1:]:
        print("    " + colors.WARNING + "         " + msg_line + colors.ENDC)

def error(msg):
    msg_lines = msg.split("\n")
    print('\n' + colors.FAIL + "ERROR: " + msg_lines[0] + colors.ENDC)
    for msg_line in msg_lines[1:]:
        print(colors.FAIL + "       " + msg_line + colors.ENDC)    
    print()

def save(img, fn, format, quality):
    print("    " + colors.OKGREEN + "Saving: " + fn + colors.ENDC)
    img.save(fn, format, optimize=True, quality=quality)

def find_images(folder):
    # Find images in root folder
    images = [i for i in glob(os.path.join(folder, "*.jpg")) + 
        glob(os.path.join(folder, "*.png")) if os.path.isfile(i)]

    # Recursively find images in sub-folders
    folders = [f for f in glob(os.path.join(folder, "*")) if os.path.isdir(f)]
    for folder in folders:
        images = images + find_images(folder)
    
    return images

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--convert", type=str, action='store',
        help="The format to convert all images to. Either JPEG or PNG. Default = None",
        default=None)
    parser.add_argument("--quality", type=int, action='store',
        help="The quality to use with JPEG compression. Valid range is 1 - 100.",
        default=70)
    parser.add_argument("--out-dir", type=str, action='store', dest='out_dir',
        help="The root directory to send resized pictures to.",
        default=os.path.join("assets", "img"))
    parser.add_argument("--in-dir", type=str, action='store', dest='in_dir', 
        help="The root directory to pull pictures from.",
        default="_img")
    parser.add_argument("--clean", action='store_true', default=False,
        help="Include this to clean the output directory (assets/img) by default.")
    parser.add_argument("--deep", action='store_true', default=False,
        help="Include this to overwrite all images.")

    args = parser.parse_args()

    in_dir = args.in_dir
    out_dir = args.out_dir

    convert = args.convert
    quality = args.quality
    clean = args.clean
    deep = args.deep

    if clean:
        if out_dir in ['.', './']:
            warn("You are attempting to remove everything in your current directory!!!!")
        elif out_dir == in_dir:
            warn("You are attempting to remove the input directory!!!")
        else:
            warn("You are attempting to remove the directory {}".format(out_dir))
        
        ans = input("Are you sure you want to do this? [yes / no]: ")
        if ans.lower() in ['yes', 'y']:
            # Delete only folders that exist in in_dir
            in_dir_folder_names = [os.path.basename(f) for f in glob(os.path.join(in_dir, '*')) if os.path.isdir(f)]
            out_dir_folders = [os.path.join(out_dir, f) for f in in_dir_folder_names]
            for f in out_dir_folders:
                warn("Removing folder: {}".format(f))
                shutil.rmtree(f)

    # Check for spelling error
    if convert is None:
        pass
    elif convert.lower() in ['jpg', 'jpeg']:
        convert = 'JPEG'
    elif convert.lower() in ['png']:
        convert = 'PNG'
    elif convert is not None:
        error("Value passed to --convert not valid. Use {} --help for more info.".format(sys.argv[0]))
        exit()

    # Range checking
    if quality > 100 or quality < 1:
        error("Value passed to --quality not valid. Use {} --help for more info.".format(sys.argv[0]))
        exit()
    
    # Find all images in the input directory
    image_names = find_images(in_dir)

    images = [Image.open(i) for i in image_names]

    for name, img in zip(image_names, images):
        folder_name = os.path.dirname(name)
        if folder_name != in_dir:
            folder_name = folder_name.replace(in_dir + '/', '')
        # Check if we are scanning the root directory, in which case we want
        # those files to go to the root of the our directory
        if folder_name == in_dir or folder_name + '/' == in_dir:
            save_dir = out_dir
        else:
            save_dir = os.path.join(out_dir, folder_name)
        make_dir(save_dir)

        update("\nProcessing {}".format(name))
        if img.format not in ['JPEG', 'PNG', 'MPO']:
            warn("Image is required to be either JPEG or PNG format.\nImage is detected to be of format: {}\nSkipping...".format(img.format))
            continue

        width = img.width
        height = img.height

        aspect_ratio = float(width) / float(height)

        # Sort by image size small to large
        key_val_list = [(key, resize_widths[key]) for key in sorted(resize_widths, 
            key=resize_widths.get)]
        
        for width_name, resize_width in key_val_list:
            filename, ext = os.path.splitext(name)

            if convert is None:
                ext = ext[1:]
            elif img.format == 'JPEG' or convert == 'JPEG' or img.format == 'MPO':
                ext = 'jpg'
            elif img.format == 'PNG' or convert == 'PNG':
                ext = 'png'

            if width_name == 'self':
                save_name = "{}.{}".format(os.path.join(save_dir, os.path.basename(filename)), ext)                
            else:
                save_name = "{}_{}.{}".format(os.path.join(save_dir, os.path.basename(filename)), 
                    width_name, ext)

            # If we don't want to overwrite images, skip ones that already exist
            if not deep and os.path.exists(save_name):
                update("Skipping existing file...")
                continue

            # Compute necessary height given aspect ratio
            resize_height = int(resize_width / aspect_ratio)

            # Check if we are upscaling, in which case a new image isn't necessary
            if resize_width >= width:
                warn("Upscaling detected! Format {} requires an image of width at least {}px\nSaving at normal resolution...".format(width_name, resize_width))
                resize_width = width
                resize_height = height

            if width_name == 'self':
                resize_width = width
                resize_height = height

            resized_img = img.resize((resize_width, resize_height))

            # Check if we need to convert the image before saving
            if convert is not None:
                if convert == 'JPEG':
                    resized_img = resized_img.convert('RGB')
                elif convert == 'PNG':
                    resized_img = resized_img.convert('RGBA')

                save(resized_img, save_name, convert, quality)
            else:
                save(resized_img, save_name, img.format, quality)
    
if __name__ == "__main__":
    main()
