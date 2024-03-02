from flask import Flask, Response, request
from jsonrpcserver import method, Result, Success, dispatch

app = Flask(__name__)


@method
def ping() -> Result:
    print(Success("pong"))
    return Success()


@app.route("/", methods=["POST"])
def index():
    return Response(
        dispatch(request.get_data().decode()), content_type="application/json"
    )


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 8080)