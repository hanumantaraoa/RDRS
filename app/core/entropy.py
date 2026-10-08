import math
from pathlib import Path

def calculate_shannon_entropy(filepath: str) -> float:
    path = Path(filepath)
    if not path.exists() or path.is_dir():
        return 0.0
    
    total_bytes = path.stat().st_size
    if total_bytes == 0:
        return 0.0

    counts = [0] * 256
    try:
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                for byte in chunk:
                    counts[byte] += 1
    except IOError:
        return 0.0

    entropy = 0.0
    for count in counts:
        if count == 0:
            continue
        p = count / total_bytes
        entropy -= p * math.log2(p)
    return round(entropy, 4)