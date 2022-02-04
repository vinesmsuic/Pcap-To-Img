import os
import shutil
from tqdm import tqdm
import random
import argparse

def parser():
    parser = argparse.ArgumentParser(description="Copying files")
    parser.add_argument("--limit", type=int, required=False, default=-1, help="only copy a number of files each folder")
    return parser.parse_args()

def main():
    args = parser()

    src_dir = os.path.join('2_Flow','AllLayers')
    dst_dir = os.path.join('2_Flow_Processed','AllLayers')

    if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)

    folders = os.listdir(src_dir)
    for folder in folders:
        
        if not os.path.exists(os.path.join(dst_dir,folder)):
            os.makedirs(os.path.join(dst_dir,folder))
        
        if(os.path.isdir(os.path.join(dst_dir,folder))):
            
            print("Now Processing Folder: ", folder)

            copying_folders = os.listdir(os.path.join(src_dir,folder))

            random.seed(72)
            random.shuffle(copying_folders)

            if(args.limit!= -1):
                if(len(copying_folders) > args.limit):
                    copying_folders = copying_folders[:args.limit]
                elif(len(copying_folders) < args.limit):
                    print("Folder "+str(folder), "does not have required "+str(args.limit) + "files. Folder only has "+str(len(copying_folders)) + " files.")



            for f in tqdm(copying_folders):
                full_file_name = os.path.join(src_dir, folder, f)
                if os.path.isfile(full_file_name):
                    shutil.copy(full_file_name, os.path.join(dst_dir, folder))
                

if __name__ == '__main__':
    main()