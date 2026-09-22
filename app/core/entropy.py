import math
import os

def calculate_shannon_entropy(file_path: str) -> float:
    """FR-3: Computes Shannon Entropy (0.0 to 8.0) reflecting data randomness/encryption."""
    if not os.path.exists(file_path) or os.path.isdir(file_path):
        return 0.0
    
    try:
        size = os.path.getsize(file_path)
        if size == 0:
            return 0.0
        
        counts = [0] * 256
        # Stream read to remain safe with large file payloads
        with open(file_path, "rb") as f:
            while chunk := f.read(65536):
                for byte in chunk:
                    counts[byte] += 1
        
        entropy = 0.0
        for count in counts:
            if count == 0:
                continue
            p = count / size
            entropy -= p * math.log2(p)
        return round(entropy, 4)
    except Exception:
        return 0.0
