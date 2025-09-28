# Digital Nose — Hardware‑Free AI Scent Classifier Prototype

**Digital Nose** is a prototype that shows a **test automation + ML** pipeline for scent classification.
It uses **synthetic VOC/environment features** (BME688‑style) to train models and includes a **live mock sensor stream** so you can demo real‑time inference today.
When the sensor arrives, swap in a real I²C reader and keep the rest unchanged.

## Features
- **Synthetic dataset** (2,400 rows, 8 features) for reproducible experimentation
- **Reproducible ML pipeline** (SVM, RandomForest, k‑NN with k‑fold CV + test split)
- **Saved model** (`scent_model.pkl`) + **confusion matrix** image
- **Live mock stream** (`mock_stream.py`) → **classifier** (`classify_stream.py`) for real‑time predictions
- **Notebook** (`Digital_Nose_Demo.ipynb`) with clear outputs
- **One‑page report** (`DIGITAL_NOSE_REPORT.md`) for quick review

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
