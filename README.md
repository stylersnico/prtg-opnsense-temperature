# Temperature monitoring for OPNSense and PRTG

Monitor temperatures on OPNSense without any external tools

## Tested on
- OPNsense 26.1.8 / FreeBSD 14.3
- Should work on other BSD os if you have Python3 installed

## Setup 

Create a **HTTP Push Data Advanced** sensor in your PRTG and grab the **Identification Token**.

Download the files and restart configd service:
```bash
mkdir /var/script
curl -O https://raw.githubusercontent.com/stylersnico/prtg-opnsense-temperature/refs/heads/main/prtg_temps_sensor.py > /var/script/prtg_temps_sensor.py
curl -O https://raw.githubusercontent.com/stylersnico/prtg-opnsense-temperature/refs/heads/main/actions_push-prtg-temp.conf > /usr/local/opnsense/service/conf/actions.d/actions_push-prtg-temp.conf
service configd restart
```

Edit it to put your **PRTG IP** and **Identification token** at the beginning of `/var/script/prtg_temps_sensor.py`

Create a scheduled task that send the data every minute from GUI:

<img width="1856" height="778" alt="image" src="https://github.com/user-attachments/assets/92fc5af1-d19e-48a8-97b6-9116790eda42" />


## Screenshots

<img width="1953" height="843" alt="image" src="https://github.com/user-attachments/assets/377a7a5b-80a7-49a3-b42a-a39362fcbd95" />
