
import sys, json, pickle, os, time
import numpy as np

FEATURES = ["raw_voc", "gas_res", "humidity", "temperature", "voc_delta", "voc_slope", "gas_ratio", "humid_comp_voc"]

def load_model(path):
    with open(path, "rb") as f:
        return pickle.load(f)

def smooth(prev, new, alpha=0.2):
    if prev is None:
        return new
    return prev * (1 - alpha) + new * alpha

def main():
    model_path = os.environ.get("SCENT_MODEL", "scent_model.pkl")
    model = load_model(model_path)
    prev = None
    counts = {}
    start = time.time()

    for line in sys.stdin:
        try:
            obj = json.loads(line.strip())
        except Exception:
            continue
        if "mode" in obj:
            print(f"[INFO] Mode: {obj['mode']} target_family={obj.get('family')}")
            continue
        x = np.array([[obj.get(k, 0.0) for k in FEATURES]], dtype=float)
        prob = None
        try:
            if hasattr(model, "predict_proba"):
                prob = model.predict_proba(x)[0]
        except Exception:
            prob = None

        pred = model.predict(x)[0]
        counts[pred] = counts.get(pred, 0) + 1

        if prob is not None:
            # simple confidence as max class prob
            conf = float(np.max(prob))
            prev = smooth(prev, conf)
            conf_out = prev if prev is not None else conf
            print(f"pred={pred:8s} conf={conf_out:.3f} counts={counts}")
        else:
            print(f"pred={pred:8s} counts={counts}")

        if time.time() - start > 12.0:
            # brief demo window
            break

    # Final majority vote
    final_pred = None
    if counts:
        final_pred = max(counts.items(), key=lambda kv: kv[1])[0]
    print(f"[FINAL] majority_pred={final_pred} counts={counts}")

if __name__ == "__main__":
    main()
