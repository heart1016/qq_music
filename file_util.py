# -*- coding: utf-8 -*-

from mutagen.mp3 import MP3, HeaderNotFoundError
from mutagen.id3 import ID3, APIC, TPE1, TIT2, TALB, error
from PIL import Image
#from osgeo import gdal
#import numpy as np


def resize_img(file_path, max_size=(800, 800), quality=90):
    try:
        """
        img = gdal.Open(file_path)
        r = img.GetRasterBand(1)
        g = img.GetRasterBand(2)
        b = img.GetRasterBand(3)
        xx = 50
        yy = 50
        data1 = r.ReadAsArray(0, 0,xx, yy)
        data2 = g.ReadAsArray(0, 0,xx, yy)
        data3 = b.ReadAsArray(0, 0,xx, yy)
        data =  np.dstack([data1, data2, data3])
        img = Image.fromarray(data)
        """
        img = Image.open(file_path)
        img = img.convert('RGB')
    except IOError:
        print('Can\'t open image:', file_path)
        return

    if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
        img.thumbnail(max_size, Image.ANTIALIAS)
        img.save(file_path, quality=quality)


def add_metadata_to_song(file_path, cover_path, song):
    # If no ID3 tags in mp3 file
    try:
        audio = MP3(file_path, ID3=ID3)
    except HeaderNotFoundError:
        print('Can\'t sync to MPEG frame, not an validate MP3 file!')
        return

    if audio.tags is None:
        print('No ID3 tag, trying to add one!')
        try:
            audio.add_tags()
            audio.save()
        except error as e:
            print('Error occur when add tags:', str(e))
            return

    # Modify ID3 tags
    id3 = ID3(file_path)
    # Remove old 'APIC' frame
    # Because two 'APIC' may exist together with the different description
    # For more information visit: http://mutagen.readthedocs.io/en/latest/user/id3.html
    if id3.getall('APIC'):
        id3.delall('APIC')
    # add album cover
    id3.add(
        APIC(
            encoding=0,         # 3 is for UTF8, but here we use 0 (LATIN1) for 163, orz~~~
            mime='image/jpeg',  # image/jpeg or image/png
            type=3,             # 3 is for the cover(front) image
            data=open(cover_path, 'rb').read()
        )
    )
    # add artist name
    id3.add(
        TPE1(
            encoding=3,
            text=song['singer'][0]['name']
        )
    )
    # add song name
    id3.add(
        TIT2(
            encoding=3,
            text=song['songname']
        )
    )
    # add album name
    id3.add(
        TALB(
            encoding=3,
            text=song['albumname']
        )
    )
    id3.save(v2_version=3)
