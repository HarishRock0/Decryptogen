# Decryptogen

A machine learning project for personality prediction (Introvert vs Extrovert), including:
- model training and evaluation in `model.ipynb`
- a FastAPI inference service in `app.py`
- a Streamlit frontend in `streamlit_app.py`
- a request-based API test script in `test.py`

## Project Structure

- `app.py`: FastAPI app for serving predictions
- `streamlit_app.py`: Streamlit UI that calls the FastAPI backend
- `model.ipynb`: training and evaluation notebook
- `personality_dataset.csv`: dataset used for training
- `test.py`: simple API request tests
- `best_model.pkl`: trained model artifact used by API
- `scaler.pkl`: scaler artifact from training
- `Dockerfile`: container entrypoint for Hugging Face Spaces
- `start.sh`: starts the FastAPI backend and Streamlit UI

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the API Locally

```bash
uvicorn app:app --reload
```

API will start at:
- http://127.0.0.1:8000
- Docs: http://127.0.0.1:8000/docs

## Run the Streamlit UI Locally

Start the FastAPI backend in one terminal:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Start the Streamlit frontend in another terminal:

```bash
streamlit run streamlit_app.py
```

The UI will talk to `http://127.0.0.1:8000/predict` by default.

## Hugging Face Deployment

This project is set up to deploy to Hugging Face Spaces using Docker.

Docker runtime behavior:

```bash
/app/start.sh
```

Deployment checklist:

1. Create a new Hugging Face Space.
2. Choose a Docker Space.
3. Push this repository with `Dockerfile`, `start.sh`, `streamlit_app.py`, `app.py`, `requirements.txt`, `best_model.pkl`, and `scaler.pkl`.
4. Make sure the Space exposes port `7860`.
5. The Streamlit UI will call the FastAPI backend on `http://127.0.0.1:8000/predict` inside the container.
6. After deployment, update `test.py` to point to your Space URL if you still want to use it for external API checks.

## Example Prediction Request

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"Time_spent_Alone\":9,\"Stage_fear\":\"Yes\",\"Social_event_attendance\":1,\"Going_outside\":2,\"Drained_after_socializing\":\"Yes\",\"Friends_circle_size\":3,\"Post_frequency\":2}"
```

## Run the Test Script

`test.py` currently points to the deployed API URL. To test locally, change the URL to `http://127.0.0.1:8000/predict` and run:

```bash
python test.py
```

## Notes

- Ensure `best_model.pkl` exists in the project root before running `app.py`.
- The API expects `Stage_fear` and `Drained_after_socializing` as `"Yes"` or `"No"`.
- In Docker/Hugging Face Spaces, Streamlit is exposed on port `7860` and FastAPI stays internal on port `8000`.
