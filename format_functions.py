import os

from wand.image import Image as W_Image

exception_formats = ['.HEIC','.HEIF']

def open_file(filename):
    with W_Image(filename=filename) as img:
        return img.clone()
    
def convert_to_jpg(formatted_image, output_file_path):
    formatted_image.save(filename=output_file_path+'.jpg')
    output_filename = os.path.split(output_file_path)
    return output_filename[1]

def format_check(ext,image_name, output_file_path):
    if ext in exception_formats:
                formatted_image = open_file(image_name)
                os.remove(image_name)
                image_name = convert_to_jpg(formatted_image, output_file_path)
    else:
        output_filename = os.path.split(output_file_path)
        image_name = output_filename[1]
    return image_name
