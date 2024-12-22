import uvicorn
from dotenv import load_dotenv

from auth_service.main.web_api import create_app

if __name__ == "__main__":
    load_dotenv()

    app = create_app()

    uvicorn.run(app)
