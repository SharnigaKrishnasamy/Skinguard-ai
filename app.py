from model.predict import predict
from rag.rag_pipeline import answer


def pipeline(image, question):
    """Run skin-image prediction, then retrieve relevant educational information."""
    prediction = predict(image)

    response = answer(
        question,
        predicted_label=prediction["label"]
    )

    return {
        "prediction": prediction,
        "response": response,
        "disclaimer": (
            "Educational information only. This is not a medical diagnosis. "
            "Consult a dermatologist for medical advice."
        ),
    }


if __name__ == "__main__":
    print("SkinGuard-AI pipeline imports successfully.")
    print("Use pipeline(image, question) to run the complete flow.")
