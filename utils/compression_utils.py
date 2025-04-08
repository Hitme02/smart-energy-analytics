import zlib
import json

def compress_data(data: dict) -> bytes:
    """
    Compress a dictionary to a zlib-compressed byte string.
    """
    json_str = json.dumps(data)
    return zlib.compress(json_str.encode('utf-8'))

def decompress_data(compressed: bytes) -> dict:
    """
    Decompress a zlib-compressed byte string back into a dictionary.
    """
    json_str = zlib.decompress(compressed).decode('utf-8')
    return json.loads(json_str)

# Optional test section
if __name__ == "__main__":
    raw_data = {
        "timestamp": "2025-04-04 10:00:00",
        "usage_kwh": 4.52,
        "device_id": "meter_001"
    }

    compressed = compress_data(raw_data)
    print("🗜️ Compressed Data (bytes):", compressed)

    decompressed = decompress_data(compressed)
    print("🔓 Decompressed Data (dict):", decompressed)
