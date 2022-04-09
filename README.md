# RFID Scanning of NTNU cards

## Quick test

Clone repository.

```
cd /project-folder
git clone git@github.com:napahlm/rfid-ntnu.git
```

Create virtual environment on Ubuntu:
```
cd /path/to/project-folder/repository
python3 -m venv env
source env/bin/activate
```

Install dependancies:
```
pip3 install -r /path/to/project-folder/requirements.txt
```

Test script:
```
python3 rfid.py
```

Deactivate venv:
```
deactivate
```

## Context and other sources

Code that uses a basic RFID USB readerreads the emitted ID of a NTNU card and returns the EM number on the backside. This work is a combination of similar work I've found[^1] [^2] [^3]. Make NTNU has also made something equivalent for an Arduino board[^4].

## Hardware

SYC ID&IC USB Reader. Serial number: 08FF20140315. These can be bought at [Omega Verksted](https://www.omegav.ntnu.no/) that also use these for their system.

## Interpreting the card data

NB: The card reader is not acknowledged as an USB device but rather an input device like a keyboard which can cause frustration when trying to find the serial port. It reads the card data and then dumps the ID like a really fast keyboard.

Each NTNU card has two chips:

- EM4102 (125 kHz) [EM]
- Mifare Classic 1k (13.56 MHz) [M]

This card reader uses the EM4102 chip which has info about the EM number of an NTNU card. This is the chip that the card readers at the doors on campus use. More info about these chips are found in the references.

### Data format

The card emits 10 bytes of data. The ID we want is 4 bytes.

| Start | Length  | Type    | ID         | Parity | Stop   |
| :---: | :-----: | :-----: | :--------: | :----: | :----: |
|  0x02 |    0x0A |  0x0201 | 0xXXXXXXXX |   0xXX |   0x03 |

### Algorithm to extract EM number

```
1. Transform ID from decimal to zero-padded binary
2. Split the binary into 4 different byte-sized groups
3. Reverse the bits in each respective group
4. Conjoin the reversed byte groups into one
5. Transform from binary to decimal
```


## References

[^1]: https://dvikan.no/hvordan-fungerer-ntnu-adgangskortene
[^2]: https://github.com/hermabe/rfid-card
[^3]: https://github.com/balag3/RFID_reader
[^4]: https://github.com/MAKENTNU/RFID-scanner
