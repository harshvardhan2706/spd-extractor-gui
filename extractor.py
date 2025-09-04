import os

def extract_spd(file_path, output_dir):
    with open(file_path, "rb") as f:
        data = f.read()

    # search for WAV headers
    i = 0
    count = 0
    while i < len(data):
        if data[i:i+4] == b"RIFF" and data[i+8:i+12] == b"WAVE":
            size = int.from_bytes(data[i+4:i+8], "little")
            wav_data = data[i:i+8+size]
            out_path = os.path.join(output_dir, f"extracted_{count:02d}.wav")
            with open(out_path, "wb") as wf:
                wf.write(wav_data)
            count += 1
            i += 8 + size
        else:
            i += 1
