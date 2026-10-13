from pydantic import BaseModel, Field
from typing import Literal

# Input schema plan:

# Administrative: int, >= 0
# Administrative_Duration: float, >= 0
# Informational: int, >= 0
# Informational_Duration: float, >= 0
# ProductRelated: int, >= 0
# ProductRelated_Duration: float, >= 0
# BounceRates: float, between 0 and 1
# ExitRates: float, between 0 and 1
# PageValues: float, >= 0 (possible leakage; client must supply it)
# SpecialDay: float, between 0 and 1
# Month: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec (3-letter names)
#   - the API maps "Jun" to "June", the spelling used in training
#   - Jan and Apr were not in the training data; the encoder ignores them,
#     so the model scores without month info
# OperatingSystems: int, >= 1 (unseen codes ignored by the encoder)
# Browser: int, >= 1 (unseen codes ignored by the encoder)
# Region: int, >= 1 (unseen codes ignored by the encoder)
# TrafficType: int, >= 1 (unseen codes ignored by the encoder)
# VisitorType: one of Returning_Visitor, New_Visitor, Other ("Other" is rare)
# Weekend: bool


class SessionInput(BaseModel):
    Administrative : int = Field(ge= 0)
    Administrative_Duration: float = Field(ge= 0)
    Informational: int = Field(ge= 0)
    Informational_Duration: float = Field(ge= 0)
    ProductRelated: int = Field(ge= 0)
    ProductRelated_Duration: float = Field(ge= 0)
    BounceRates: float = Field(ge =0, le=1)
    ExitRates: float = Field(ge = 0, le =1)
    PageValues: float = Field(ge = 0)
    SpecialDay: float =Field(ge = 0, le=1)
    Month : Literal["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    OperatingSystems: int = Field(ge = 1)
    Browser: int = Field(ge = 1)
    Region: int = Field(ge=1)
    TrafficType: int = Field(ge=1)
    VisitorType : Literal["Returning_Visitor", "New_Visitor", "Other"]
    Weekend: bool

    
