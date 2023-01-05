from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request
import json
import math

# SpaceCowboy models a cowboy in our super amazing system


@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system


@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system


@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location


# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database


@app.route('/entity', methods=['POST'])
def create_entity():
    info = request.get_json()
    entities = info['entities']
    for entity in entities:
        newEntity = SpaceEntity(entity['metadata'], entity['location'])
        space_database.append(newEntity)

    return json.dumps({})
    ...

# lasooable returns all the space animals a space cowboy can lasso given their name


@app.route('/lassoable', methods=['GET'])
def lassoable():
    info = request.args.to_dict()
    cowboyName = info['cowboy_name']
    cowboy = None
    for entity in space_database:
        metadata = entity.metadata
        if 'name' in metadata and metadata['name'] == cowboyName:
            cowboy = entity
            break

    loc_x = cowboy.location['x']
    loc_y = cowboy.location['y']

    entity_list = []

    for entity in space_database:
        ent_x = entity.location['x']
        ent_y = entity.location['y']
        distance = math.sqrt(abs(loc_x - ent_x) * abs(loc_x -
                             ent_x) + abs(loc_y - ent_y) * abs(loc_y - ent_y))
        if distance <= cowboy.metadata['lassoLength'] and 'name' not in entity.metadata:
            entity_list.append(
                {"type": entity.metadata, "location": entity.location})

    return json.dumps({"space_animals": entity_list})
    ...


"""
NOTE: The endpoints here are assuming Design by Contract and therefore aren't error checking
"""

# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)
