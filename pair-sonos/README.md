# pair-sonos
A simple python script that stereo pairs Sonos speakers. Nothing more, nothing less.

The script uses [SoCo](https://github.com/SoCo/SoCo) to discover and find UID:s of Sonos devices.

Tested on Python 3.9

To build a single binary executable file:
```bash
pip3 install pyinstaller

pyinstaller pair.py --name sonos-pair --onefile

OR (faster binary version)

pip3 install cx_Freeze

python3 setup.py build --build-base=sonos-pair

cp -r sonos-pair ~/bin/

Add build/exe... to PATH
```

## Prerequisites

Pip3 install:

```bash
pip3 install -r requirements.txt
```

## Usage

List devices:
```bash
python pair.py list
```

If that doesn't work, the problem might be that SoCo needs to know the IP of your network interface. Try:
```bash
python pair.py list my_ip_goes_here
```

Pair speakers:
```bash
python pair.py pair master_ip slave_ip
```

The **master** will act as the **left** speaker.

Unpair speakers:
```bash
python pair.py unpair ip_of_master
```

Depending on your Python installation, you might have to change `python` to `python3`.
