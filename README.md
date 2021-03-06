# Pcap-To-Img
A Modified version of USTC-TK2016 Tools
* For Windows only

# Before Preprocessing

## Convert PcapNG Files to Pcap Files
If you are using PcapNG (`.pcapng`) Files 
> Sometimes pcapng will also shown as `.pcap` file.

* `editcap` program is available from [Wireshark](https://www.wireshark.org/).
* [Usage of editcap](https://www.wireshark.org/docs/man-pages/editcap.html)

```powershell
editcap -F libpcap dump.pcapng dump.pcap
```

* Please see [How To handle PcapNG files](https://www.netresec.com/?page=Blog&month=2012-12&post=HowTo-handle-PcapNG-files) for more detail.


## Usage of Tools

* `SplitCap` : [https://www.netresec.com/?page=SplitCap](https://www.netresec.com/?page=SplitCap)
* `finddupe` : [https://www.sentex.ca/~mwandel/finddupe/](https://www.sentex.ca/~mwandel/finddupe/)


## Run Powershell as Administrator

```Powershell
set-ExecutionPolicy RemoteSigned
```

# Preprocessing

Split Pcap files into Flows
```Powershell
.\1_Pcap2Flow.ps1
```

```Powershell
python .\2_Flow2Packet.py
```

```
usage: 2_Flow2Packet.py [-h] --packet PACKET --byte BYTE [--limit LIMIT]

Selecting Parameter of Packets and Bytes.

optional arguments:
  -h, --help       show this help message and exit
  --packet PACKET  number of required packets
  --byte BYTE      number of trimmed byte
  --limit LIMIT    only extract packets from the largest N flows
```

```Powershell
python .\3_Packet2Image.py
```