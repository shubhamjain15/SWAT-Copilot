from pydantic import BaseModel
class SUBRecord(BaseModel):
   sub: int
   area_km2: float
