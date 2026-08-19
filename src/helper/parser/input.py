from pydantic import BaseModel, Field


class Input(BaseModel):

    nbDrones: int = Field(alias="nb_drones", default=0)
    startHub: str = Field(alias="start_hub", default="")
    endHub: str = Field(alias="end_hub", default="")
    hubs: list[str] = Field(alias="hub", default=[])
    connections: list[str] = Field(alias="connection", default=[])
