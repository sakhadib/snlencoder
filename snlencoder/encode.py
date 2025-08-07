def encode_move(pick, to, status):
    """
    Status

    00 - 0 = indicates [skip] / [not moving]
    01 - 1 = indicates [ladder hit]
    10 - 2 = indicates [snake hit]
    11 - 3 = indicates [normal progress]

    """
    if not (0 <= pick <= 6):
        raise ValueError("Pick must be between 0 and 6")
    if not (0 <= to <= 100):
        raise ValueError("Destination must be between 0 and 100")
    if not (0 <= status <= 3):
        raise ValueError("Status must be between 0 and 3")
    
    pick_bin = pick & 0b111     # 3 bits for pick (0-6)
    to_bin = to & 0b1111111     # 7 bits for to (0-100)
    status_bin = status & 0b11  # 2 bits for status (0-3)

    # Combine: pick (3 bits) | to (7 bits) | status (2 bits) = 12 bits total
    data = (pick_bin << 9) | (to_bin << 2) | status_bin

    return f"{data:03X}"


def decode_move(hex_str):
    if len(hex_str) != 3:
        raise ValueError("Hex move must be 3 characters")

    data = int(hex_str, 16)

    pick = (data >> 9) & 0b111      # Extract pick (3 bits)
    to = (data >> 2) & 0b1111111    # Extract to (7 bits)
    status = data & 0b11            # Extract status (2 bits)

    return pick, to, status


def batch_decode(hex_string):
    """
    Decode a long string of hex digits by splitting into 3-character chunks.
    
    Args:
        hex_string (str): Long hex string to decode
        
    Returns:
        list: List of tuples, each containing (pick, to, status)
    """
    if len(hex_string) % 3 != 0:
        raise ValueError("Hex string length must be divisible by 3")
    
    moves = []
    for i in range(0, len(hex_string), 3):
        chunk = hex_string[i:i+3]
        pick, to, status = decode_move(chunk)
        moves.append((pick, to, status))
    
    return moves


