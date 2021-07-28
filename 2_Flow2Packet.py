import dpkt
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import argparse

def parser():
    parser = argparse.ArgumentParser(description="Selecting Parameter of Packets and Bytes.")
    parser.add_argument("--packet", type=int, required=True, help="number of required packets")
    parser.add_argument("--byte", type=int, required=True, help="number of trimmed byte")
    return parser.parse_args()


def get_packets(pcap, packetnum, target_length):
    
    r_num = 0
    packetlist = []

    # For each packet in the pcap process the contents
    for ts, buf in pcap:

        r_num += 1

        byte_buf = bytes(buf)
        trimmed_buf = trimming(byte_buf, target_length=target_length)

        packetlist.append(trimmed_buf)

        if(r_num == packetnum):
            break

    # If number of packets is lesser than our requirements, pad a whole packet of zeros
    if(r_num < packetnum):
        for _ in range(packetnum - r_num):
            paddings = bytes(target_length)
            packetlist.append(paddings)

    return packetlist


def trimming(byte, target_length):

    # Appending zeros in a packet if byte length < target length
    if(len(byte) < target_length):
        needed_length = target_length - len(byte)
        zeros = bytearray(needed_length)
        return (byte+zeros)

    # Trim byte in a packet if byte length > target length
    elif(len(byte) > target_length):
        return (byte[:target_length])
    
    # Else byte length = target length. Do nothing.
    else:
        return byte

def packet_from_file(file, packetnum, target_length):
    with open(file, 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        packets = get_packets(pcap, packetnum=packetnum, target_length=target_length)
        #print(np.shape(packets))
        return packets

def main():
    args = parser()

    directory = os.path.join('2_Flow', 'AllLayers')

    folder_df = pd.DataFrame(columns = ['Path','Bytes'])
    
    for folder in os.listdir(directory):

        if(os.path.isdir(os.path.join(directory,folder))):
            
            print("Now Processing Folder: ", folder)
            
            for f in tqdm(os.listdir(os.path.join(directory,folder))):
                if f.endswith(".pcap"): 
                    #print(os.path.join(directory, folder, f))
                    path_to_file = os.path.join(directory, folder, f)
                    packets = packet_from_file(path_to_file, packetnum=args.packet, target_length=args.byte)
                    folder_df = folder_df.append({'Path' : path_to_file, 'Bytes' : packets}, ignore_index = True)
                    continue
                else:
                    continue

            print(folder, "Entries:", folder_df.shape[0])
        
            save_path = os.path.join('3_Packet' , os.path.basename(os.path.join(directory,folder)))+".pkl"
            
            folder_df.to_pickle(save_path)
            print("Saved to file: ", save_path)
        
            continue
        else:
            continue

if __name__ == '__main__':
    main()