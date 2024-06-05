!Pritesh Gandhi(pgandh05@uoguelph.ca)

import subprocess
import sys
import numpy as np
import struct

def parse_mbr(disk_file): 
	disk_file.seek(0) 
	mbr = disk_file.read(512) 
	if len(mbr) < 512: 
		raise Exception("Failed to read MBR") 
	partitions = [] 
	for i in range(4): 
		entry = mbr[446 + i * 16: 462 + i * 16] 
		status, first_lba, num_sectors = struct.unpack("<BLL", entry[0:9]) 
		if status == 0: 
			continue 
		partitions.append((first_lba, num_sectors)) 
	return partitions

def unpartitioned_space():
	# Open disk image file
	with open("mbr_fat.dd", "rb") as disk_file:
		free_space = check_lba_consistency(disk_file)
		print("Consistency Check (Unpartitioned disk space):")
		for start_lba, size in free_space:
			print(f"Start LBA: {start_lba} Size: {size} sectors")


def check_lba_consistency(disk_file):
	partitions = parse_mbr(disk_file)
	disk_size = disk_file.seek(0, 2) // 512
	partitions.sort()

	free_space = []
	last_end = 0
	for first_lba, num_sectors in partitions:
		if last_end < first_lba:
			free_space.append((last_end, first_lba - last_end))
		last_end = first_lba + num_sectors

	if last_end < disk_size:
		free_space.append((last_end, disk_size - last_end))

	return free_space

def consistency_check(partition):
	partitions=[]
	sector_size = 512
	with open("mbr_fat.dd","rb") as hex_file:
		for dp in range(len(partition)):
			LBA=[value for key, value in partition[dp].items() if key=='Starting-LBA']
			Size=[value for key, value in partition[dp].items() if key=='Size-MB']
			if (LBA[0] + Size[0]) < hex_file.seek(0,2) / sector_size:
				print("Inconsistent")
			else:
				partitions.append((LBA[0],LBA[0]+Size[0]-1))
	return partitions	

def output_func(MBR):
	from tabulate import tabulate
	print(tabulate(MBR, headers="keys"))

def partition_calc(partition):
	MBR=[]
	Output_MBR={}
	keys=["Starting-CHS","Starting-LBA","Size-MB","Type"]
	check = validity_check(partition)
	if check == False:
		print("Invalid disk image!")	
		exit(0)	
	MBR.append(CHS_calc(partition))
	MBR.append(lba(partition))
	MBR.append(size_calc(partition))
	MBR.append(partition_type(partition))
	for dp in range(len(keys)):
		Output_MBR[keys[dp]] = MBR[dp]
	return Output_MBR	
	
def partition_type(partition):
	par_type = {"05":"Extended Partition","07":"NTFS","01":"DOS 12-bit FAT","82":"Linux Swap","83":"Linux Native partition","0b":"32-bit FAT","00":"Invalid File Type"}
	for_type="0x{:02x}".format(partition[4])
	for_type=for_type[2:]
	for key in par_type:	
		if for_type == key:
			return par_type[key]

def lba(partition):
	endian=[]
	LBA=""
	for i in range(8,12):
		endian.append("0x{:02x}".format(partition[i]))
	for dp in endian:	
		LBA=str(dp[2:])+LBA
	value=hextodec(LBA)
	return value

def size_calc(partition):
	blocks=[]
	hexa=''
	for i in range(12,16):
		blocks.append("0x{:02x}".format(partition[i]))
	for dp in blocks:
		hexa="{0:02}".format(dp[2:])+hexa
	hexadecimal=((int(hexa,16)*512)/1024)/1024
	return round(hexadecimal,6) 



def validity_check(partition):
		if (partition[0] == '00' or '80') :
			return True
		else:
			return False

def CHS_calc(partition):	
	C,S,temp=([] for i in range(3))
	bi="{0:08b}".format(int(partition[2]))
	temp=list(str(bi))
	C=temp[:2]
	S=temp[2:]
	for dp in list(str(partition[3])):
		C.append(dp)
	dec_C=bintodec(C)
	dec_S=bintodec(S)
	CHS="C:"+str(dec_C)+" "+"H:"+str(partition[1])+" "+"S:"+str(dec_S)
	return CHS

def bintodec(li):
	res = [eval(i) for i in li]
	num = 0
	for b in res:
		num = 2 * num + b
	return num

def hextodec(li):
	res = [eval(i) for i in li]
	num = 0
	for b in res:
		num = 16 * num + b
	return num

mbr_data=[]
partition=[]
MBR=[]
image = sys.argv
subprocess.Popen("dcfldd if="+str(image[1])+" bs=512 skip=0 count=1 of=mbr_fat.dd", shell=True)
with open("mbr_fat.dd","rb") as hex_file:
	hex_data = hex_file.read()
#print(hex_data)
for h in range(446, 510):
	mbr_data.append(hex_data[h])
partition= np.array_split(mbr_data,4)
#print(partition)
for dp in partition:
	temp_dict=partition_calc(dp)
	res = "Invalid File Type" in temp_dict.values()
	if res==False:
		MBR.append(temp_dict)
part=consistency_check(MBR)
output_func(MBR)
unpartitioned_space()

	
