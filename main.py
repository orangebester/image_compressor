import os
import sys

from os import listdir
from os.path import isfile, join
from PIL import Image
from settings import src_dir_path, dst_dir_path, optimal_size, optimal_format


def img_check(src_dir_path):
    names_list = [i for i in listdir(
        src_dir_path) if isfile(join(src_dir_path, i))]
    return names_list


def img_size(src_dir_path):
    img_name = img_check(src_dir_path)
    img_size = [os.path.getsize(src_dir_path + '\\' + image_name)
                for image_name in img_name]
    img_dict = {img_name[i]: img_size[i] for i in range(len(img_name))}
    return img_dict


def compression_check(src_dir_path, dst_dir_path):
    dct_to_compress = {}
    for i, j in img_size(src_dir_path).items():
        file_exist = isfile(dst_dir_path + '\\' + i)

        filename, ext = os.path.splitext(i)
        new_filename = f"{filename}.jpg"

        if j < optimal_size and file_exist == False:
            img = Image.open(src_dir_path + '\\' + i)
            img = img.convert("RGB")
            img.save(dst_dir_path + '\\' + new_filename, format=optimal_format)
        elif j > optimal_size and file_exist == False:
            dct_to_compress[i] = j
        else:
            pass
    return dct_to_compress


def compress_img(src_dir_path, dst_dir_path):
    dct_to_compress = compression_check(src_dir_path, dst_dir_path)

    for i in dct_to_compress.keys():
        compression_quality = 90
        img = Image.open(src_dir_path + '\\' + i)

        while True:
            temp_buffer = dst_dir_path + '\\' + 'temp_' + i
            try:
                img.save(temp_buffer, format=optimal_format,
                         quality=compression_quality)
            except OSError:
                img = img.convert("RGB")
                img.save(temp_buffer, format=optimal_format,
                         quality=compression_quality)
            compressed_size = os.path.getsize(temp_buffer)
            if compressed_size > optimal_size:
                compression_quality -= 10
            else:
                break

        final_path = dst_dir_path + '\\' + i
        img.save(final_path,
                 format=optimal_format, quality=compression_quality)
        os.remove(temp_buffer)


compress_img(src_dir_path, dst_dir_path)
