corr = [0.080, 0.015, 0.030, 0.040, 0.130, 0.020, 0.015, 0.060, 0.065, 0.005, 0.005, 0.035, 
0.030, 0.070, 0.080, 0.020, 0.002, 0.065, 0.060, 0.090, 0.030, 0.010,   0.015, 0.005, 0.020, 0.002]

encrypt_texts = ['XTKYBFWJXJHZWNYD', 'KCECMKS']

for cipher_text in encrypt_texts:

    print("\n")
    phi, freq = [0]*26, [0]*26
    cipher_text = cipher_text.lower() #make all letters lowercase

    #find the order and corresponding frequency of all characters in cipher text
    for char in cipher_text:
        char_index = ord(char)-ord('a')
        freq[char_index] = freq[char_index] + 1/len(cipher_text)
    
    #populate phi array as per the formula for multiplying freq array and correlation array
    for i in range(0, 26):
        for char in cipher_text:
            char_index = ord(char)-ord('a')
            phi[i] = phi[i] + freq[char_index]*corr[char_index-i]
    
    #sort the phi array in descending order and print the top 5 possible plain texts
    sorted_phi = sorted([[val, index] for index, val in enumerate(phi)], key=lambda x: x[0], reverse=True)

    for i in range(0, 5):
        shift_idx = sorted_phi[i][1]
        text = ""
        for char in cipher_text:
            new_char = chr((26 + (ord(char)-ord('a'))-shift_idx) % 26 + ord('a'))

            text = text + new_char
        
        print(f"With shift - {shift_idx} Plain Text - {text}")