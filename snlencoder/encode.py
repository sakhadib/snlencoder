def encode_move(r1, r2, pick, to):
    if not (1 <= r1 <= 6) or not (1 <= r2 <= 6):
        raise ValueError("Dice rolls must be between 1 and 6")
    if not (0 <= pick <= 6):
        raise ValueError("Pick must be between 0 and 6")
    if not (0 <= to <= 127):
        raise ValueError("Destination block must be between 0 and 127")

    if(pick == 0): pick = 0
    elif(pick == r1): pick = 1
    elif(pick == r2): pick = 2
    
    r1_bin = r1 & 0b111
    r2_bin = r2 & 0b111
    pick_bin = pick & 0b11
    to_bin = to & 0b1111111

    data = (r1_bin << 13) | (r2_bin << 10) | (pick_bin << 8) | (to_bin << 1)
    parity = bin(data).count("1") % 2 == 1
    data |= int(parity)

    return f"{data:04X}"


def decode_move(hex_str):
    if len(hex_str) != 4:
        raise ValueError("Hex move must be 4 characters")

    data = int(hex_str, 16)

    parity = data & 1
    bits15 = data >> 1

    if bin(bits15).count("1") % 2 != parity:
        raise ValueError("Parity check failed")

    r1 = (bits15 >> 12) & 0b111
    r2 = (bits15 >> 9) & 0b111
    pick_encoded = (bits15 >> 7) & 0b11
    to = bits15 & 0b1111111

    # Decode the pick value back to original dice value
    if pick_encoded == 0:
        pick = 0
    elif pick_encoded == 1:
        pick = r1
    elif pick_encoded == 2:
        pick = r2
    else:
        pick = pick_encoded  # fallback for any other value

    return r1, r2, pick, to
