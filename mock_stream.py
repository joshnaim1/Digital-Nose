
import time, json, sys, random
import numpy as np

FAMILIES = ["citrus", "floral", "woody", "aquatic"]

# Family profiles roughly matching the synthetic generator
PROFILES = {
    "citrus":  {"raw_voc": (2.2, 0.25), "gas_res": (1800, 120), "humidity": (40, 3), "temperature": (24, 0.7)},
    "floral":  {"raw_voc": (2.0, 0.22), "gas_res": (2000, 140), "humidity": (45, 3), "temperature": (23, 0.7)},
    "woody":   {"raw_voc": (1.3, 0.18), "gas_res": (2500, 150), "humidity": (42, 3), "temperature": (22.5, 0.7)},
    "aquatic": {"raw_voc": (0.9, 0.20), "gas_res": (2900, 160), "humidity": (55, 3), "temperature": (23.5, 0.7)}
}

def derive_features(raw_voc, gas_res, humidity, temperature):
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

def sample_profile(family):
    p = PROFILES[family]
    raw_voc = random.gauss(*p["raw_voc"])
    gas_res = max(100.0, random.gauss(*p["gas_res"]))
    humidity = max(5.0, random.gauss(*p["humidity"]))
    temperature = random.gauss(*p["temperature"])
    return derive_features(raw_voc, gas_res, humidity, temperature)

def main():
    family = sys.argv[1] if len(sys.argv) > 1 else random.choice(FAMILIES)
    print(json.dumps({"mode": "family", "family": family}))
    for _ in range(60):
        frame = sample_profile(family)
        print(json.dumps(frame), flush=True)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
