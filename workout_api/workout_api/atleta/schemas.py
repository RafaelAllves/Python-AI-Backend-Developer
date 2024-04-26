from typing import Annotated
from pydantic import Field, PositiveFloat, PositiveInt
from workout_api.contrib.schemas import BaseSchema, OutMixin
from workout_api.workout_api.categorias.schemas import CategoriaIn
from workout_api.workout_api.centro_treinamento.schemas import CentroTreinamentoAtleta


class Atleta(BaseSchema):
    nome: Annotated[str, Field(description='Nome do atleta', example='Fulano', max_length=50)]
    cpf: Annotated[str, Field(description='CPF do atleta', example='12345678900', max_length=11)]
    idade: Annotated[PositiveInt, Field(description='Idade do atleta', example=25)]
    peso: Annotated[PositiveFloat, Field(description='Peso do atleta', example=75.5)]
    altura: Annotated[PositiveFloat, Field(description='Altura do atleta', example=1.70)]
    sexo: Annotated[str, Field(description='Sexo do atleta', example='M', max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]

class AtletaIn(Atleta):
    pass

class AtletaOut(Atleta, OutMixin):
    pass
