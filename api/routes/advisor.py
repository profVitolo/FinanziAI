from fastapi import APIRouter
from fastapi.responses import JSONResponse
from advisor_engine.advisor_engine import AdvisorEngine
from advisor_engine.advisor_executor import AdvisorExecutor, AdvisorBusyError
from advisor_engine.advisor_models import AdvisorRequest, InvestorProfile
from api.schemas import AdviseBody

router = APIRouter(prefix="/advisor", tags=["Advisor"])

executor = AdvisorExecutor()    
engine = AdvisorEngine()

@router.get("/investor-profiles")
def get_investor_profiles():
    return [
        {
            "value": profile.value,
            "label": profile.name,
        }
        for profile in InvestorProfile
    ]


@router.post("/advise")
def advise(body: AdviseBody):
    request = AdvisorRequest(prompt=body.prompt, investor_profile=body.investor_profile)
    
    try:
        return executor.execute(engine.advise, request)
    
    except AdvisorBusyError as ex:
        #raise HTTPException(status_code=429, detail=str(ex))
        return JSONResponse(
            status_code=429,
            headers={"Retry-After": "5"},
            content={
                "detail": str(ex)
            },
        )