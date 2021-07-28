foreach($f in gci 1_Pcap *.pcap)
{
    echo "Now processing file : $f"
    0_Tool\SplitCap_2-1\SplitCap -p 100000 -b 100000 -r $f.FullName -s flow -o 2_Flow\AllLayers\$($f.BaseName)-ALL
    #0_Tool\SplitCap_2-1\SplitCap -p 100000 -b 100000 -r $f.FullName -s flow -o 2_Flow\L7\$($f.BaseName)-L7 -y L7
    
    echo "Done Spliting! Now Clearing 0KB size files..."
    # Delete pcap files length equal to 0
    gci 2_Flow\AllLayers\$($f.BaseName)-ALL | ?{$_.Length -eq 0} | del
    echo "-------------------------------------------------"
}

echo "Now Eliminating duplicate flows..."
# Eliminate duplicate Flows
0_Tool\finddupe -del 2_Flow\AllLayers
echo "-------------------------------------------------"
echo "Finished"
