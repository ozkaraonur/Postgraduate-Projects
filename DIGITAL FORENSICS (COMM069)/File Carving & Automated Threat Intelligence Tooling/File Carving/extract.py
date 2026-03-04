from PIL import Image

def extract():
    # 1. Open the suspicious image
    img = Image.open('stego.png')
    bitmap = img.load()
    w, h = img.size

    data_bits = []
    # 2. Loop through every pixel exactly like the attacker did
    for y in range(h):
        for x in range(w):
            red_channel = bitmap[x, y][0]
            # 3. Pull out the 2nd bit (bit index 1)
            # This reverses: (int(data_bit) << 1)
            bit = (red_channel >> 1) & 1
            data_bits.append(bit)

    # 4. Group the bits into bytes (8 bits = 1 byte)
    recovered_bytes = bytearray()
    for i in range(0, len(data_bits), 8):
        byte = 0
        for bit_offset in range(8):
            if i + bit_offset < len(data_bits):
                # The attacker used bit % 8 for the bit position
                byte |= (data_bits[i + bit_offset] << bit_offset)
        recovered_bytes.append(byte)

    # 5. Write the bytes to a new Excel file
    with open('Budget-Forecast.xls', 'wb') as f:
        f.write(recovered_bytes)
    print("Recovery complete: Budget-Forecast.xls created.")

if __name__ == "__main__":
    extract()
