from flask import Flask, render_template, request, redirect
import requests
import cv2
import numpy as np
import base64

app = Flask(__name__)

FASTAPI_URL = "http://inference:8000/predict"  # for fastapi inference container from food101 docker-compose.yml

@app.route('/food101', methods=["GET", "POST"])
def food101():
    if request.method == "POST":
        if "image" not in request.files:
            return redirect(request.url)
        file = request.files["image"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            # Send image to FastAPI inference endpoint
            files = {"file": (file.filename, file.stream, file.mimetype)}
            response = requests.post(FASTAPI_URL, files=files)

            if response.status_code != 200:
                return render_template("food101.html", error="Inference failed. Try again.")

            result = response.json()

            # Optional: If you want to visualize predictions on the original image
            # Reload image to memory
            file.stream.seek(0)
            data = np.frombuffer(file.read(), dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)

            # Annotate with predictions (example: overlay top prediction)
            preds = result.get("predictions", [])
            if not preds:
                return render_template("food101.html", error="No predictions returned.")
            top = preds[0]
            top_text = top.get("class") or str(top.get("id", ""))
            cv2.putText(image, top_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            _, buffer = cv2.imencode('.jpg', image)
            result_base64 = base64.b64encode(buffer).decode('utf-8')
            result_data_url = f"data:image/jpeg;base64,{result_base64}"

            return render_template(
                "food101.html",
                result_image=result_data_url,
                predictions=result["predictions"],
                latency=result["latency_ms"]
            )

    return render_template("food101.html")