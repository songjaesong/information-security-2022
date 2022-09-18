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

#로터1 로터2 로터3
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
# NEXT : 노치에 도달했을 때 다음 바퀴가 회전했는지 여부
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

# 3. setting값들을 확인하고 SETTINGS에 저장
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
        pass_third = chr(SETTINGS["WHEELS"][2]["wire"].index(input) + ord('A'))
        pass_second = chr(SETTINGS["WHEELS"][1]["wire"].index(pass_third) + ord('A'))
        pass_first = chr(SETTINGS["WHEELS"][0]["wire"].index(pass_second) + ord('A'))

        print("REVERSE!")
        print("pass_third: " + str(pass_third) + " pass_second: " + str(pass_second) + " pass_first: " +str(pass_first))

        return pass_first
    else :
        pass_first = SETTINGS["WHEELS"][0]["wire"][ord(input) - ord('A')]
        pass_second = SETTINGS["WHEELS"][1]["wire"][ord(pass_first) - ord('A')]
        pass_third = SETTINGS["WHEELS"][2]["wire"][ord(pass_second) - ord('A')]
        
        print("ENCONDING!")
        print("pass_first: " + str(pass_first) + " pass_second: " + str(pass_second) + " pass_third: " +str(pass_third))
        
        return pass_third

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# rotate_wheel_pos & rotate_wheel_alpha
def rotate_wheel_pos(input):
    SETTINGS["WHEEL_POS"][input] += 1
    SETTINGS["WHEEL_POS"][input] %= 26
    SETTINGS["WHEELS"][input]["wire"] = SETTINGS["WHEELS"][input]["wire"][-1:] + SETTINGS["WHEELS"][input]["wire"][:-1]


# Wheel Rotation
def rotate_wheels():
    # Implement Wheel Rotation Logics

    if SETTINGS["WHEEL_POS"][0] == SETTINGS["WHEELS"][0]["turn"] :
        if SETTINGS["WHEEL_POS"][1] == SETTINGS["WHEELS"][1]["turn"] :
            # 1바퀴가 노치에 걸려있고 2바퀴도 노치에 걸려서 3바퀴가 돌아갈때 -> 셋다 돌아감
            rotate_wheel_pos(0)
            rotate_wheel_pos(1)
            rotate_wheel_pos(2)
        else :
            # 1바퀴가 노치에 걸려있고 2바퀴는 노치에 걸리지 않은 경우 -> 1,2 돌아감
            rotate_wheel_pos(0)
            rotate_wheel_pos(1)
    else :
        # 1바퀴가 돌아갈때 -> 1 돌아감
        rotate_wheel_pos(0)
    pass

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")

# 2. 각기 setting값들을 받는다.
# ukw_select : reflector A,B,C설정 B
# wheel_select : wheel 순서 설정 I III II
# wheel_pos_select : 
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