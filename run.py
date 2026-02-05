import os
from app import create_app
from app.config import Config

config = Config()
app = create_app(config)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=config.DEBUG)  # nosec B104
