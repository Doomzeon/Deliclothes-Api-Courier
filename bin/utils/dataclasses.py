from marshmallow_dataclass import dataclass

@dataclass
class CourierLogin:
    email:str
    password:str