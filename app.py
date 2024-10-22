from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)


@app.route("/scrape", methods=["GET"])
def scrape():
    url = request.args.get("url")  # Get the URL from query parameters
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract script tags with data-content-len attribute
        script_data = []
        for script in soup.find_all("script"):
            if "data-content-len" in script.attrs:
                data_len = int(script["data-content-len"])  # Convert to integer
                # Extract script content (if necessary)
                script_content = script.string.strip() if script.string else ""
                script_data.append((data_len, script_content))

        # Find the script with the highest data-content-len
        highest_script = max(script_data, key=lambda x: x[0], default=None)
        (length, data) = highest_script

        return (
            jsonify(
                {
                    "data": data,
                    # "edges": edges,
                    # "highest_data_content_len": highest_script,
                    "message": "HTML content saved to scraped_content.html",
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "Hello from Flask on Vercel!"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
