# Author: @vinesmsuic
#
#
import numpy as np
import pandas as pd
import os
import pickle
from PIL import Image
import binascii
from tqdm import tqdm

def to_hex(byte_list):
    bytelist = []
    for b in byte_list:
        bytelist.append(binascii.hexlify(bytes(b)))
    
    return bytelist

def matrix_from_hex(hex_list):
    matrice = []
    for hex_str in hex_list:
        matrix = np.array([int(hex_str[i:i+2],16) for i in range(0, len(hex_str), 2)])
        matrix = np.uint8(matrix)
        matrice.append(matrix)

    matrice = np.stack(matrice, axis=0)
    return matrice 

def get_save_path(one_row_df, save_folder):
    base = os.path.basename(one_row_df['Path'])
    filename = os.path.splitext(base)[0]

    ImagePath = os.path.join(save_folder,filename)
    return ImagePath
    
    
def main():
    searching_folder = "3_Packet"
    saving_folder = "4_Image"
    
    for f in os.listdir(searching_folder):
        if f.endswith(".pkl"):
            
            folder = os.path.join(saving_folder, os.path.splitext(f)[0])
            if not os.path.exists(folder):
                os.makedirs(folder)
            
            print("Saving to: " + str(folder))

            file = open(os.path.join(searching_folder, f), 'rb')
            df = pickle.load(file)
            file.close()

            df['Hex'] = df['Bytes'].apply(to_hex)
            df['Matrice'] = df['Hex'].apply(matrix_from_hex)
            
            for index, row in tqdm(df.iterrows()):
                ImagePath = get_save_path(row, folder)
                im = Image.fromarray(row['Matrice'])
                im.save(str(ImagePath)+".png")



if __name__ == '__main__':
    main()