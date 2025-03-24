import time
from typing import Dict

import requests
import torch  # noqa: F401
from ray import serve
from starlette.requests import Request
from transformers import pipeline


# 1: Wrap the pretrained sentiment analysis model in a Serve deployment.
@serve.deployment
class SentimentAnalysisDeployment:
    def __init__(self):
        self._model = pipeline("sentiment-analysis")

    def __call__(self, request: Request) -> Dict:
        return self._model(request.query_params["text"])[0]


# 2: Deploy the deployment.
serve.run(SentimentAnalysisDeployment.bind(), route_prefix="/")


def main() -> None:
    # 3: Query the deployment and print the result.
    print(
        requests.get(
            "http://localhost:8000/", params={"text": "Ray Serve is great!"}
        ).json()
    )
    # {'label': 'POSITIVE', 'score': 0.9998476505279541}
    time.sleep(100)


if __name__ == "__main__":
    main()
