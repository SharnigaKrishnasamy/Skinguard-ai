import csv
from pathlib import Path
from PIL import Image
from model.predict import predict

root = Path.home() / "Downloads" / "skinguard_test_pack"
csv_path = root / "expected_predictions.csv"
image_dir = root / "images"

total = 0
matches = 0
correct = 0
mel_total = 0
mel_correct = 0

with csv_path.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    path = image_dir / row["file"]
    with Image.open(path) as image:
        result = predict(image.copy())

    expected_prediction = row["predicted"]
    actual_prediction = result["label"]
    same = actual_prediction == expected_prediction
    total += 1
    matches += int(same)

    true_label = row["true_label"]
    correct += int(actual_prediction == true_label)

    if true_label == "mel":
        mel_total += 1
        mel_correct += int(actual_prediction == "mel")

    print(
        f'{row["file"]}: expected_model={expected_prediction}, '
        f'local={actual_prediction}, confidence={result["confidence"]:.4f}, '
        f'uncertain={result["uncertain"]}, match={same}'
    )

print("\n--- SUMMARY ---")
print(f"CSV prediction matches: {matches}/{total} ({matches / total * 100:.2f}%)")
print(f"Local predictions correct vs labels: {correct}/{total} ({correct / total * 100:.2f}%)")
print(f"Melanoma correctly classified: {mel_correct}/{mel_total}")
