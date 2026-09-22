import os
import pytest
from app.core.entropy import calculate_shannon_entropy

def test_entropy_of_zero_file(tmp_path):
    empty_file = tmp_path / "empty.dat"
    empty_file.write_bytes(b"")
    assert calculate_shannon_entropy(str(empty_file)) == 0.0

def test_entropy_high_value(tmp_path):
    random_bytes = os.urandom(2000)
    rand_file = tmp_path / "random.dat"
    rand_file.write_bytes(random_bytes)
    assert calculate_shannon_entropy(str(rand_file)) > 7.0