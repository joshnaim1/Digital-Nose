# Digital Nose - my weird obsession over cologne has led me to this

**Digital Nose** is a prototype that shows a **test automation + ML** pipeline for scent classification.
It uses **synthetic VOC/environment features** (BME688‑style) to train models and includes a **live mock sensor stream** so you can demo real‑time inference.

**NOTE:** This project is still WIP

## Features
-Created a small synthetic dataset to mimic sensor readings (VOC levels, temperature, humidity) for testing ideas before hardware arrived

-Built a simple Python workflow to try out a few classifiers (k-NN, RandomForest, SVM) and check accuracy with cross-validation

-Made a basic demo: a mock stream that outputs “sensor” values and a classifier script that gives live predictions in the terminal

## Quickstart
```bash
pip install -r requirements.txt
# or: pip install scikit-learn pandas numpy matplotlib

# Run a live demo (pick one: citrus | floral | woody | aquatic)
python mock_stream.py floral | python classify_stream.py
```

Example output:
```
[INFO] Mode: family target_family=floral
pred=floral   conf=0.93 counts={'floral': 1}
...
[FINAL] majority_pred=floral counts={'floral': 45, 'citrus': 3, ...}
```

## Repo Structure
```
digital_nose/
├─ synthetic_scent_data.csv       # synthetic VOC/env dataset
├─ scent_model.pkl                # best trained model (SVM by default)
├─ metrics.json                   # CV + test scores + report text
├─ confusion_matrix.png           # test-set confusion matrix
├─ mock_stream.py                 # emits JSON frames like a sensor
├─ classify_stream.py             # reads frames from stdin, prints predictions
├─ Digital_Nose_Demo.ipynb        # executed notebook (training + plots)
├─ DIGITAL_NOSE_REPORT.md         # one-page summary with results
├─ requirements.txt               # python deps
├─ LICENSE                        # MIT
└─ .gitignore
```

## Swap‑In Plan (when hardware arrives)
1. Write `bme688_reader.py` that reads via I²C and **prints JSON frames** with the same keys used in `mock_stream.py`.
2. Then run:
   ```bash
   python bme688_reader.py | python classify_stream.py
   ```
3. Everything else (model, classifier, README) stays the same.

## Notes
- The dataset is synthetic and meant for **methodology validation**.
- The pipeline and streaming demo are designed to be **sensor‑agnostic** with a stable JSON schema.
