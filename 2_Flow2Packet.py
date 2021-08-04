# Author: @vinesmsuic
#
#

import dpkt
import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import argparse
import random

def parser():
    parser = argparse.ArgumentParser(description="Selecting Parameter of Packets and Bytes.")
    parser.add_argument("--packet", type=int, required=True, help="number of required packets")
    parser.add_argument("--byte", type=int, required=True, help="number of trimmed byte")
    parser.add_argument("--limit", type=int, required=False, default=-1, help="only extract packets from the largest N flows")
    return parser.parse_args()

# Sanitization
def zero_mask_packet(eth_packet):

    #Mask MAC Address to 00:00:00:00:00:00
    eth_packet.src = b'\x00\x00\x00\x00\x00\x00'
    eth_packet.dst = b'\x00\x00\x00\x00\x00\x00'

    if(eth_packet.data.__class__.__name__ == 'IP6'):
        #Mask IPv6 Address to 0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0
        eth_packet.data.src = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        eth_packet.data.dst = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    else:
        #Mask IPv4 Address to 0.0.0.0
        eth_packet.data.src = b'\x00\x00\x00\x00'
        eth_packet.data.dst = b'\x00\x00\x00\x00'
    
    return eth_packet

# Extract Information
def get_packets(pcap, packetnum, target_length):
    
    r_num = 0
    packetlist = []

    # For each packet in the pcap process the contents
    for ts, buf in pcap:

        r_num += 1

        eth_packet = dpkt.ethernet.Ethernet(buf)
        eth_packet = zero_mask_packet(eth_packet)

        byte_buf = bytes(eth_packet)
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
    
    for folder in os.listdir(directory):

        if(os.path.isdir(os.path.join(directory,folder))):
            
            
            print("Now Processing Folder: ", folder)

            # Create Dataframe Object
            folder_df = pd.DataFrame(columns = ['Path','Bytes'])

            searching_folders = os.listdir(os.path.join(directory,folder))

            #####################################
            # TODO:
            #
            #
            ##if(args.sort == 1):
                #Sort the searching folders by size (largerst to smallest)
                ##searching_folders = sorted(searching_folders, key=lambda f: os.path.getsize(os.path.abspath(os.path.join(directory, folder, f))), reverse=True)  
            ##else:
            random.seed(72)
            random.shuffle(searching_folders)

            ######################################


            if(args.limit!= -1):
                if(len(searching_folders) > args.limit):
                    searching_folders = searching_folders[:args.limit]
                elif(len(searching_folders) < args.limit):
                    print("Folder "+str(folder), "does not have required "+str(args.limit) + "files. Folder only has "+str(len(searching_folders)) + " files.")
            


            for f in tqdm(searching_folders):

                if f.endswith(".pcap"): 
                    #print(os.path.join(directory, folder, f))
                    path_to_file = os.path.join(directory, folder, f)
                    packets = packet_from_file(path_to_file, packetnum=args.packet, target_length=args.byte)
                    # Create Dataframe Object
                    folder_df = folder_df.append({'Path' : path_to_file, 'Bytes' : packets}, ignore_index = True)

                    continue
                else:
                    continue

            print("Row entries of "+str(folder)+": ",folder_df.shape[0])
        
            save_path = os.path.join('3_Packet' , folder)+"-p"+str(args.packet)+"-b"+str(args.byte)+"-l"+str(abs(args.limit))+".pkl"
            
            folder_df.to_pickle(save_path)
            print("Saved to file: ", save_path)
            print("-"*20)
        
            continue
        else:
            continue

if __name__ == '__main__':
    main()