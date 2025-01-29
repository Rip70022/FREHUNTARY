## FREHUNTARY - WiFi Nuclear Disruptor V0.1

**AUTHOR:**
Rip70022/craxterpy

**Description:**

`FREHUNTARY` is a `Python` script that acts as a "`WiFi network disruptor`" or "`WiFi jammer`". Its primary function is to send `deauthentication packets` to a target `Access Point` (AP), which can cause `devices` connected to the `network` to `disconnect`.

**Features:**

* Selects a target `Access Point` (AP) or all `APs` in range
* Supports `channel hopping` and `monitor mode`
* Sends `deauthentication` packets to the target `AP's` `MAC` address
* Can be `configured` to `attack` a specific `channel`
* Uses the `Scapy` library for `packet manipulation`

**Usage:**

1. Clone the `repository` and run the script as `root`.
```
git clone https://github.com/Rip70022/FREHUNTARY
```
```
cd FREHUNTARY
```
```
sudo python3 FREHUNTARY.py
```
3. Select the target `Access Points` (AP) or all `APs` in range.
4. The script will begin sending `deauthentication packets` to the `target AP`.

**Requirements:**

* `Python 3.x`
* `Sapy library`
* `Wireless network` interface (default: `wlan0`)
* `Monitor mode` enabled on the `network interface`
