import numpy as np
import scipy as sp
import os
import sys

ARGS = sys.argv
STDOUT = False
OUTFILE = 0

print(len(ARGS))

if len(ARGS) == 3:
    INFILE = ARGS[1]
    OUTFILE = ARGS[2]
elif len(ARGS) == 2:
    INFILE = ARGS[1]
    STDOUT = True
else: 
    print("Wrong arguments provided, going into interactive mode...")
    INFILE = input("Name of input file (.wav): ")
    OUTFILE = input("Name of output file: ")

if not os.path.exists(f"./{INFILE}"):
    print(f"{INFILE} does not exist.")
    sys.exit()
if os.path.exists(f"./{OUTFILE}") and not OUTFILE:
    print(f"{OUTFILE} already exists.")
    choice = input("Overwrite? (YES/ NO): ")
    if not choice == "YES":
        print("exiting")
        sys.exit()
    

def maxfreq(x, length):
    try:
    	X = np.fft.fft(x)
    except: 
        #print("wrong data length")
        return 1
    X = np.absolute(X)
    X = X[:len(X)//2]
    freq = np.argmax(X)
    return freq/length

from scipy.io import wavfile
samplerate, data = wavfile.read(INFILE)

def ReadBytes(data):
    DC = np.copy(data)[:-10]
    samples = 50
    time = samples/44100
    dl = len(DC)
    duration = dl/44100
    divs = dl // samples
    bytes = []
    while len(DC) > 2000:
        print(len(DC))
        #print(bytes)
        for i in range(divs):
            d = DC[i * samples : (i + 1) * samples]
            if len(d) < 50 or len(DC) < 2000: 
                return bytearray(np.array(bytes, dtype = "uint8"))
            fsamp = maxfreq(d, time)
            if abs(fsamp - 2400) < 500:
                #print("waiting")
                continue
            elif abs(fsamp - 1200) < 500:
                #print("reading")
                invbyte = int(0)
                for j in range(1,9):
                    d = DC[147 * j + i * samples: 147 * j + i * samples + 50]
                    if len(d) < 50 or len(DC) < 2000: 
                        return bytearray(np.array(bytes, dtype = "uint8"))
                    f = maxfreq(d, time)
                    if abs(f - 2400) < 600:
                        invbyte += 1 * 2 ** (j - 1)
                    elif abs(f - 1200) < 600:
                        invbyte += 0 * 2 ** (j - 1)
                    else:
                        print("Read Error")
                bytes.append(invbyte)
                DC = DC[147 * 9 + i * samples:]
                print(147 * 9 + i * samples)
                break
            else: 
                #print(f"unknown {fsamp}")
                continue
    return bytes

result = ReadBytes(data)
result = bytes(result)
if not STDOUT:
    with open(OUTFILE, "wb") as binary_file:
        binary_file.write(result)
else: 
    for b in result:
        print(chr(b), end = '')
