# RFID Scanning of NTNU cards

A program continuously running a card reader in the background that returns the EM number of NTNU access cards when triggered.

## Quick test

*Tested last: April 9th 2022*

Clone repository.

```
cd /project-folder
git clone git@github.com:napahlm/rfid-ntnu.git
```

Create virtual environment (Ubuntu):
```
cd /rfid-ntnu
python3 -m venv env
source env/bin/activate
```

Install dependencies:
```
pip3 install -r requirements.txt
```

Test script (Make sure reader is connected):
```
python3 rfid.py
```

Deactivate venv when finished:
```
deactivate
```

## Context and other sources

Code that uses a basic RFID USB reader that reads the emitted ID of an NTNU card and returns the EM number found on the backside. This work is a combination of similar work I've found[^1] [^2] [^3]. [Make NTNU](https://makentnu.no/) has also made something equivalent for an Arduino board[^4].

## Hardware

SYC ID&IC USB Reader.

- Serial number: 08FF20140315.

These can be bought at [Omega Verksted](https://www.omegav.ntnu.no/) that also use these for their payment system.

## Interpreting the card data

***NB**: The card reader is not acknowledged as an USB device but rather an input device like a keyboard which can cause frustration when trying to find the serial port. It reads the card data and then dumps the ID like a really fast keyboard.*

Each NTNU card has two chips:

- EM4102 (125 kHz)
- Mifare Classic 1k (13.56 MHz)

This card reader triggers the EM4102 chip which has info about the EM number of an NTNU card. This is the chip that the card readers giving door access on campus use. More info about these chips are found in the references.

### Data format

The card emits 10 bytes of data. The ID we want is 4 bytes and is the only info read when used normally.

| Start | Length  | Type    | ID         | Parity | Stop   |
| :---: | :-----: | :-----: | :--------: | :----: | :----: |
|  0x02 |    0x0A |  0x0201 | 0xXXXXXXXX |   0xXX |   0x03 |

### Algorithm to extract EM number

```
1. Transform ID from decimal to zero-padded binary
2. Split the binary into 4 different byte-sized groups
3. Reverse the bits in each respective group
4. Conjoin the reversed byte-groups into one
5. Transform from binary to decimal
```


## References

[^1]: https://dvikan.no/hvordan-fungerer-ntnu-adgangskortene
[^2]: https://github.com/hermabe/rfid-card
[^3]: https://github.com/balag3/RFID_reader
[^4]: https://github.com/MAKENTNU/RFID-scanner
