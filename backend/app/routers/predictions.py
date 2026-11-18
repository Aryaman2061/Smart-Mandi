
from fastapi import APIRouter, HTTPException

from app.schemas import PricePredictionRequest
from app.services.prediction_service import predict_market_price


router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)


@router.post("/predict")
def predict_price(request: PricePredictionRequest):

    try:
        input_data = request.model_dump()

        predicted_price = predict_market_price(input_data)

        return {
            "success": True,
            "message": "Price predicted successfully",
            "data": {
                "predicted_modal_price": predicted_price,
                "unit": "Rs/quintal"
            }
        }

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
