"""Deterministic RGB PNG I/O, retaining 16-bit normal data without extra packages."""
import struct,zlib
from pathlib import Path
import numpy as np


def write_png(path,array,bits=8):
    array=np.clip(array,0,1);h,w,c=array.shape
    data=(array*((1<<bits)-1)+.5).astype('>u2' if bits==16 else np.uint8)
    rows=np.zeros((h,1+w*c*(bits//8)),np.uint8);rows[:,1:]=data.reshape(h,-1).view(np.uint8)
    def chunk(tag,payload):return struct.pack('>I',len(payload))+tag+payload+struct.pack('>I',zlib.crc32(tag+payload)&0xffffffff)
    png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',w,h,bits,{1:0,3:2,4:6}[c],0,0,0))
    png+=chunk(b'IDAT',zlib.compress(rows.tobytes(),6))+chunk(b'IEND',b'')
    Path(path).parent.mkdir(parents=True,exist_ok=True);Path(path).write_bytes(png)


def read_png(path):
    # Embedded GLB PNGs use the same lossless codec as file-backed atlases.
    data=path if isinstance(path,(bytes,bytearray)) else Path(path).read_bytes()
    offset=8;compressed=[]
    while offset<len(data):
        size=struct.unpack_from('>I',data,offset)[0];tag=data[offset+4:offset+8];payload=data[offset+8:offset+8+size];offset+=size+12
        if tag==b'IHDR':w,h,bits,kind,_,_,interlace=struct.unpack('>IIBBBBB',payload)
        if tag==b'IDAT':compressed.append(payload)
    if interlace:raise ValueError('Interlaced PNG is unsupported')
    c={0:1,2:3,6:4}[kind];stride=w*c*(bits//8)
    rows=np.frombuffer(zlib.decompress(b''.join(compressed)),np.uint8).reshape(h,stride+1)
    # Our writer deliberately uses PNG filter 0, preserving numerical precision.
    if np.any(rows[:,0]):raise ValueError('Expected the toolkit unfiltered PNG encoding')
    values=np.ascontiguousarray(rows[:,1:]).view('>u2' if bits==16 else np.uint8).reshape(h,w,c)
    return values.astype(np.float32)/((1<<bits)-1)


def linear_to_srgb(array):return np.where(array<=.0031308,array*12.92,1.055*np.power(np.maximum(array,0),1/2.4)-.055)
def srgb_to_linear(array):return np.where(array<=.04045,array/12.92,np.power((array+.055)/1.055,2.4))
