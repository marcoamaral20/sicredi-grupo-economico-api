from pydantic import BaseModel


class AssociateResponse(BaseModel):
    name: str
    cpf_cnpj: str
