from flask import Flask, send_from_directory, redirect

app = Flask(__name__, static_folder='static')

@app.route("/")
def index():
    return send_from_directory('static', 'index.html')

@app.route("/app")
def app_redirect():
    return redirect("http://localhost:8501", code=302)  # Assumes Streamlit is running on this port


if __name__ == "__main__":
    app.run(port=5000, debug=True)
