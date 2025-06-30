from random import randint

def HandleErrors():
    phrase_list = ["Big boner down the lane!", "Los Bepis!", "I'M THE ERROR WIZARD! BEHOLD!", "I was advised to not put other error messages here..."]
    return phrase_list[randint(0, len(phrase_list)-1)]