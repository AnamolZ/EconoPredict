from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from PulseAI import LoadingModel

class EconPredict:
    def __init__(self):
        self.app = FastAPI()
        self.templates = Jinja2Templates(directory="templates")
        self.configure_middleware()
        self.configure_routes()

    def configure_middleware(self):
        origins = [
            "http://localhost",
            "http://localhost:8000",
            "http://127.0.0.1",
            "http://127.0.0.1:8000",
        ]

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.app.mount("/static", StaticFiles(directory="static"), name="static")

    def configure_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request, "Prediction": "Hi! From Dev"})

        @self.app.get("/favicon.ico")
        async def favicon(request: Request):
            return None

        @self.app.post("/api/predict")
        async def predict_stock(request: Request):
            try:
                data = await request.json()
                stock = data.get("stock")
                model = LoadingModel(stock_symbol=stock, input_data_path="TrainingData.csv", trained_model="LSTMmodel.h5")
                model.predicting_value()
                prediction = model.percentage_change()
                return JSONResponse(content={"prediction": prediction})
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

app = EconPredict().app