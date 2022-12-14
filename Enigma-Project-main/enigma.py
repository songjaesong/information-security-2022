# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order

    if reverse: 
        # reflector??? ?????? reverse
        pass_third = chr(SETTINGS["WHEELS"][2]["wire"].index(input) + ord('A'))
        pass_second = chr(SETTINGS["WHEELS"][1]["wire"].index(pass_third) + ord('A'))
        pass_first = chr(SETTINGS["WHEELS"][0]["wire"].index(pass_second) + ord('A'))

        '''
        print("REVERSE!")
        print("pass_third: " + str(pass_third) + " pass_second: " + str(pass_second) + " pass_first: " +str(pass_first))
        '''

        return pass_first
    else :
        # plugboard??? ?????? ?????? ??????
        pass_first = SETTINGS["WHEELS"][0]["wire"][ord(input) - ord('A')]
        pass_second = SETTINGS["WHEELS"][1]["wire"][ord(pass_first) - ord('A')]
        pass_third = SETTINGS["WHEELS"][2]["wire"][ord(pass_second) - ord('A')]
        
        ...
        print("ENCONDING!")
        print("pass_first: " + str(pass_first) + " pass_second: " + str(pass_second) + " pass_third: " +str(pass_third))
        ...

        return pass_third

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# rotate_wheel_pos & rotate_wheel_alpha
# ???????????? - (pos+1)%26, ????????? ??????
def rotate_wheel_pos(input):
    SETTINGS["WHEEL_POS"][input] += 1
    SETTINGS["WHEEL_POS"][input] %= 26
    SETTINGS["WHEELS"][input]["wire"] = SETTINGS["WHEELS"][input]["wire"][-1:] + SETTINGS["WHEELS"][input]["wire"][:-1]

# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics

    if SETTINGS["WHEEL_POS"][0] == SETTINGS["WHEELS"][0]["turn"] :
        if SETTINGS["WHEEL_POS"][1] == SETTINGS["WHEELS"][1]["turn"] :
            # 1????????? ????????? ???????????? 2????????? ????????? ????????? 3????????? ???????????? -> ?????? ?????????
            rotate_wheel_pos(0)
            rotate_wheel_pos(1)
            rotate_wheel_pos(2)
        else :
            # 1????????? ????????? ???????????? 2????????? ????????? ????????? ?????? ?????? -> 1,2 ?????????
            rotate_wheel_pos(0)
            rotate_wheel_pos(1)
    else :
        # 1????????? ???????????? -> 1 ?????????
        rotate_wheel_pos(0)
    pass

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")

# ukw_select : reflector A,B,C?????? B
# wheel_select : wheel ?????? ?????? I III II
# wheel_pos_select : wheel ?????? ?????? A B C
# plugboard_setup : AB, CZ, EF ...

ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)

result = ''
for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    print(encoded_ch, end='')
    result += encoded_ch
print()
print("RESULT: " + str(result))