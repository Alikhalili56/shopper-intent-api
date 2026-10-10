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