from firmware_server import app

app.run(debug=True, host="0.0.0.0", port=80, threaded=True)
