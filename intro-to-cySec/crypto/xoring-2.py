import sys

def to_bytes(data):
    """Convert input (hex, ascii, or number) into bytes."""
    if isinstance(data, str) and data.lower().startswith("0x"):
        try:
            return bytes.fromhex(data[2:])
        except ValueError:
            print(f"[!] Invalid hex value: {data}")
            return b""

    if isinstance(data, str) and data.isdigit():
        val = int(data)
        return val.to_bytes((val.bit_length() + 7) // 8 or 1, "big")

    return data.encode()

def xor_data(value, key):
    value_bytes = to_bytes(value)
    key_bytes = to_bytes(key)
    return bytes([value_bytes[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(value_bytes))])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <output_type>")
        print("Example: python xor.py hex")
        print("         python xor.py ascii")
        sys.exit(1)

    output_type = sys.argv[1].lower()
    if output_type not in ["hex", "ascii"]:
        print("[!] Output type must be 'hex' or 'ascii'.")
        sys.exit(1)

    print("## Starting XOR Shell (press Ctrl+C to exit)")
    try:
        while True:
            value = input("Value: ").strip()
            key = input("Key: ").strip()

            result = xor_data(value, key)

            if output_type == "hex":
                print("→ Result:", "0x" + result.hex())
            elif output_type == "ascii":
                try:
                    print("→ Result:", result.decode())
                except UnicodeDecodeError:
                    print("→ [!] Result not printable as ASCII — try hex mode.")
            print("-" * 40)
    except KeyboardInterrupt:
        print("\nExiting... Goodbye!")

