# SNL Encoder

A compact 12-bit binary encoder for Snake and Ladder game moves.

## Overview

SNL Encoder is designed to efficiently store Snake and Ladder game data where players make moves with different outcomes (skip, ladder hit, snake hit, or normal progress). This package provides a space-efficient solution for storing billions of game moves by encoding each move into just 3 hexadecimal characters.

## Problem Statement

In a Snake and Ladder game:
- Players make moves with dice picks (0-6)
- Each move has a destination position (0-100)
- Moves have different statuses based on what happens
- Game data needs to be stored efficiently for billions of games

Traditional storage would require significant space for move sequences. This encoder compresses each move from multiple data points into just 12 bits (3 hex characters).

## Encoding Scheme

Each move is encoded into 12 bits with the following structure:

| Component | Bits | Range | Description |
|-----------|------|-------|-------------|
| pick | 3 bits | 0-6 | Dice pick value |
| to | 7 bits | 0-100 | Destination position |
| status | 2 bits | 0-3 | Move outcome status |

**Total: 12 bits = 3 hexadecimal characters**

### Status Values
- **0** (00): Skip / Not moving
- **1** (01): Ladder hit
- **2** (10): Snake hit  
- **3** (11): Normal progress

### Space Efficiency
- A 50-move game requires only 150 characters (50 × 3 hex chars)
- Massive space savings compared to traditional CSV storage
- No parity check needed due to simplified structure

## Installation

### From GitHub
```bash
pip install git+https://github.com/sakhadib/snlencoder
```

### From PyPI (if published)
```bash
pip install snlencoder
```

## Usage

```python
from snlencoder import encode_move, decode_move, batch_decode

# Encode a move: pick=3, destination=42, ladder hit
encoded = encode_move(pick=3, to=42, status=1)
print(encoded)  # Output: 3-character hex string like "6A9"

# Decode the move back
pick, to, status = decode_move(encoded)
print(f"Pick: {pick} | To: {to} | Status: {status}")
# Output: Pick: 3 | To: 42 | Status: 1

# Batch decode multiple moves
game_sequence = "6A9502123"  # 3 moves encoded
moves = batch_decode(game_sequence)
print(moves)
# Output: [(3, 42, 1), (2, 80, 2), (0, 72, 3)]
```

### Parameters

#### `encode_move(pick, to, status)`
- **pick**: Dice pick value (0-6)
- **to**: Destination position (0-100)  
- **status**: Move outcome (0=skip, 1=ladder, 2=snake, 3=normal)

#### `decode_move(hex_str)`
- **hex_str**: 3-character hexadecimal string
- **Returns**: Tuple of (pick, to, status)

#### `batch_decode(hex_string)`
- **hex_string**: Long hex string (length must be divisible by 3)
- **Returns**: List of tuples, each containing (pick, to, status)

## Error Handling

The encoder includes robust error checking:
- **Input validation**: Ensures all parameters are within valid ranges
- **Format validation**: Verifies hex string format and length during decoding
- **Batch validation**: Ensures hex string length is divisible by 3

```python
# These will raise ValueError:
encode_move(7, 50, 1)     # pick out of range
encode_move(3, 150, 1)    # to position out of range
encode_move(3, 50, 5)     # status out of range
decode_move("XYZ")        # Invalid hex format
decode_move("ABCD")       # Wrong length (must be 3 chars)
batch_decode("ABCDE")     # Length not divisible by 3
```

## Example Game Storage

```python
from snlencoder import encode_move, batch_decode

# Store a sequence of moves
moves = [
    encode_move(3, 42, 1),   # Pick 3, move to 42, ladder hit
    encode_move(0, 42, 0),   # Skip move, stay at 42
    encode_move(5, 78, 2),   # Pick 5, move to 78, snake hit  
    encode_move(2, 65, 3),   # Pick 2, move to 65, normal progress
]

# Store as compact string
game_sequence = "".join(moves)
print(f"4 moves stored in {len(game_sequence)} characters")

# Later decode the entire sequence
decoded_moves = batch_decode(game_sequence)
for i, (pick, to, status) in enumerate(decoded_moves, 1):
    status_names = ["skip", "ladder", "snake", "normal"]
    print(f"Move {i}: pick={pick}, to={to}, {status_names[status]}")
```

## CSV Schema Integration

For game database storage:

```
game_id, player_1, player_2, winner, move_count, move_sequence
1001, "Alice", "Bob", "Alice", 45, "6A9502123A4B..."
```

Where `move_sequence` contains all encoded moves concatenated together (each move = 3 hex chars).

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (pure Python)
- **Encoding**: 12-bit binary with hex representation
- **Performance**: Optimized for high-volume game data storage
- **Bit Layout**: `pick(3) | to(7) | status(2)` = 12 bits total

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Sakhawat Adib ([@sakhadib](https://github.com/sakhadib))

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on GitHub.