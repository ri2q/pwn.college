import sys

def to_bytes(data):
    """Convert input (hex, ascii, or number) into bytes."""
    # Check if input starts with 0x → HEX
    if isinstance(data, str) and data.lower().startswith("0x"):
        try:
            return bytes.fromhex(data[2:])
        except ValueError:
            print(f"[!] Invalid hex value: {data}")
            sys.exit(1)
    
    # Check if input is a number
    if isinstance(data, str) and data.isdigit():
        value = int(data)
        return value.to_bytes((value.bit_length() + 7) // 8 or 1, "big")

    # Otherwise treat as ASCII string
    return data.encode()

def xor_data(value, key, output_type):
    value_bytes = to_bytes(value)
    key_bytes = to_bytes(key)

    result = bytes([value_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(value_bytes))])

    if output_type.lower() == "hex":
        return "0x" + result.hex()
    elif output_type.lower() == "ascii":
        try:
            return result.decode()
        except UnicodeDecodeError:
            return "[!] Cannot decode as ASCII — result not printable"
    else:
        return "[!] Invalid output type. Use 'hex' or 'ascii'."

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(f"Usage: python {sys.argv[0]} <value> <key> <output_type>")
        print("Examples:")
        print(f"  python {sys.argv[0]} 'A' '0x12' hex")
        print(f"  python {sys.argv[0]} '0x41' 'B' ascii")
        print(f"  python {sys.argv[0]} '123' '456' hex")
        sys.exit(1)

    value = sys.argv[1]
    key = sys.argv[2]
    output_type = sys.argv[3]

    result = xor_data(value, key, output_type)
    print(result)

