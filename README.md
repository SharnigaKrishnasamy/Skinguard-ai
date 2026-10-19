# SkinGuard AI

**Skin lesion classification and educational information prototype using deep learning and a knowledge base.**

SkinGuard AI is a research and educational prototype designed to classify dermoscopic skin lesion images into seven categories and provide related educational information through a knowledge-base and retrieval-based question-answering pipeline.

## Supported Classes

| Label | Class |
|---|---|
| `akiec` | Actinic keratoses and intraepithelial carcinoma |
| `bcc` | Basal cell carcinoma |
| `bkl` | Benign keratosis-like lesions |
| `df` | Dermatofibroma |
| `mel` | Melanoma |
| `nv` | Melanocytic nevi |
| `vasc` | Vascular lesions |

## Project Components

- **Image classification:** EfficientNet-B0 model for seven-class prediction.
- **Prediction output:** Predicted label, confidence, top-three predictions, and uncertainty flag.
- **Knowledge base:** Educational documents for the seven lesion categories.
- **RAG prototype:** Retrieves relevant knowledge-base information for user questions.
- **Testing:** Unit tests for knowledge-base and RAG behavior, plus a script for evaluating sample images.

## Model Evaluation

A supplied test pack containing 21 dermoscopic images was used for a preliminary local evaluation.

| Metric | Result |
|---|---:|
| Sample images evaluated | 21 |
| Predictions matching supplied CSV | 21/21 (100%) |
| Predictions matching supplied labels | 16/21 (76.19%) |
| Melanoma samples correctly classified | 1/3 |

**Important interpretation:** The 100% CSV agreement means the local model reproduced the predictions recorded in the supplied CSV. It does not mean 100% model accuracy.

The 76.19% result is based on only 21 samples and is not a reliable estimate of general performance or clinical effectiveness. In this sample, two of the three melanoma images were not classified as melanoma. This is a significant limitation that must be considered in any demonstration.

## Run the Image Evaluation

1. Set up the project's Python environment and install the dependencies listed in `model/requirements.txt`.
2. Ensure the trained model file `model/model.pt` and configuration file `model/config.json` are available locally.
3. Download and extract the authorized test pack into:

   `~/Downloads/skinguard_test_pack/`

4. From the project root, run:

   ```powershell
   .\.venv\Scripts\python.exe .\test_skin_images.py
   ```

The script compares local predictions with the supplied CSV and reports label-based results. The test pack is not included in this repository; obtain it separately and follow its license terms.

## Run the Unit Tests

From the project root, run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s .\kb_and_app\tests -p "test_*.py" -v
```

## Limitations and Medical Safety

- SkinGuard AI is a research prototype, not a medical device or diagnostic tool.
- Predictions may be wrong, including predictions for melanoma and other serious conditions.
- An uncertainty flag does not guarantee that a confident prediction is correct.
- Model performance may differ on images captured with phones or on images from other datasets.
- Do not use this application to diagnose, rule out, or make treatment decisions about skin conditions.
- Anyone concerned about a skin lesion should seek assessment from a qualified dermatologist, regardless of the model's output.

## Dataset and Licensing

The supplied test pack states that its images come from the HAM10000 dermoscopic test split and are licensed under **CC BY-NC-SA 4.0**. Follow the license conditions for attribution, non-commercial use, and sharing under the same license. Verify the license and permissions of any additional model weights, datasets, or assets before redistribution.

## Disclaimer

This project is intended for educational and research purposes only. It does not replace professional medical advice, examination, diagnosis, or treatment.
