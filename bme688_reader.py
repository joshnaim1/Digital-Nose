# bme688_reader.py — stub to illustrate the JSON schema expected by classify_stream.py
# Replace `read_sensor_frame()` with real I²C reads (e.g., smbus2) and compute the same keys.

import json, random, time

def read_sensor_frame():
    # TODO: Replace with real BME688 measurements
    raw_voc = max(0.05, random.gauss(1.6, 0.4))
    gas_res = max(100.0, random.gauss(2200, 250))
    humidity = max(5.0, random.gauss(45, 5))
    temperature = random.gauss(23.5, 1.0)
    voc_delta = random.gauss(0.0, 0.05)
    voc_slope = random.gauss(0.0, 0.02)
    gas_ratio = raw_voc / (gas_res + 1.0)
    humid_comp_voc = raw_voc * (1.0 - (humidity - 45.0) * 0.002)
    return {
        "raw_voc": raw_voc,
        "gas_res": gas_res,
        "humidity": humidity,
        "temperature": temperature,
        "voc_delta": voc_delta,
        "voc_slope": voc_slope,
        "gas_ratio": gas_ratio,
        "humid_comp_voc": humid_comp_voc
    }

def main():
    print(json.dumps({"mode": "hardware", "sensor": "BME688", "note": "stub"}))
    for _ in range(60):
        print(json.dumps(read_sensor_frame()), flush=True)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
