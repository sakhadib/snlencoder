# SNL Encoder

A compact 16-bit binary encoder for Snake and Ladder game moves with parity check validation.

## Overview

SNL Encoder is designed to efficiently store Snake and Ladder game data where players roll two dice and can strategically pick one die or skip their move. This package provides a space-efficient solution for storing billions of game moves by encoding each move into just 4 hexadecimal characters.

## Problem Statement

In a modified Snake and Ladder game:
- Each player rolls 2 dice per turn
- Players can pick one die result or skip the move based on strategy
- Game data needs to be stored efficiently for billions of games

Traditional storage would require significant space for move sequences. This encoder compresses each move from multiple data points into just 16 bits (4 hex characters).

## Encoding Scheme

Each move is encoded into 16 bits with the following structure:

| Component | Bits | Range | Description |
|-----------|------|-------|-------------|
| r1 | 3 bits | 1-6 | First dice roll |
| r2 | 3 bits | 1-6 | Second dice roll |
| pick | 2 bits | 0-2 | Player's choice (0=skip, 1=r1, 2=r2) |
| to | 7 bits | 0-127 | Destination position |
| parity | 1 bit | 0-1 | Error detection bit |

**Total: 16 bits = 4 hexadecimal characters**

### Space Efficiency
- A 50-move game requires only 200 characters (50 × 4 hex chars)
- Massive space savings compared to traditional CSV storage
- Built-in parity check for data integrity

## Installation

```bash
pip install snlencoder
```

## Usage

```python
from snlencoder import encode_move, decode_move

# Encode a move: dice rolls (3,5), player picks first die, moves to position 42
encoded = encode_move(r1=3, r2=5, pick=3, to=42)
print(encoded)  # Output: 4-character hex string like "6AA1"

# Decode the move back
r1, r2, pick, to = decode_move(encoded)
print(f"Dice: {r1}, {r2} | Pick: {pick} | To: {to}")
# Output: Dice: 3, 5 | Pick: 3 | To: 42
```

### Parameters

#### `encode_move(r1, r2, pick, to)`
- **r1**: First dice roll (1-6)
- **r2**: Second dice roll (1-6)  
- **pick**: Player's choice (0=skip, or the actual dice value chosen)
- **to**: Destination position (0-127)

#### `decode_move(hex_str)`
- **hex_str**: 4-character hexadecimal string
- **Returns**: Tuple of (r1, r2, pick, to)

### Pick Value Logic
- `pick = 0`: Player skips the move
- `pick = r1`: Player chooses the first dice roll
- `pick = r2`: Player chooses the second dice roll

## Error Handling

The encoder includes robust error checking:
- **Input validation**: Ensures all parameters are within valid ranges
- **Parity check**: Detects data corruption during storage/transmission
- **Format validation**: Verifies hex string format during decoding

```python
# These will raise ValueError:
encode_move(7, 3, 1, 50)  # r1 out of range
encode_move(3, 5, 1, 200)  # to position out of range
decode_move("XYZ")        # Invalid hex format
decode_move("FFFF")       # May fail parity check
```

## Example Game Storage

```python
# Store a sequence of moves
moves = [
    encode_move(3, 5, 3, 42),   # Pick first die, move to 42
    encode_move(2, 6, 6, 48),   # Pick second die, move to 48  
    encode_move(1, 4, 0, 48),   # Skip move, stay at 48
]

# Store as compact string
game_sequence = "".join(moves)
print(f"3 moves stored in {len(game_sequence)} characters")

# Later decode the sequence
for i in range(0, len(game_sequence), 4):
    move_hex = game_sequence[i:i+4]
    r1, r2, pick, to = decode_move(move_hex)
    print(f"Move: dice({r1},{r2}) pick={pick} to={to}")
```

## CSV Schema Integration

For game database storage:

```
game_id, player_1, player_2, winner, dice_roll_count, move_sequence
1001, "Alice", "Bob", "Alice", 45, "6AA142B8C3D5..."
```

Where `move_sequence` contains all encoded moves concatenated together.

## Technical Details

- **Language**: Python 3.6+
- **Dependencies**: None (pure Python)
- **Encoding**: 16-bit binary with hex representation
- **Error Detection**: Single-bit parity check
- **Performance**: Optimized for high-volume game data storage

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

Sakhawat Adib ([@sakhadib](https://github.com/sakhadib))

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues on GitHub.