import boto3
import json
from dinosaur import Dinosaur

dynamodb = boto3.resource('dynamodb')
dinosaurs_table = dynamodb.Table('dinosaurs')


def handler(event, context):
    """
    The function to create a new dinosaur and store it into DynamoDB
    """
    dinosaur_dict = event.get('dinosaur', None)
    if not dinosaur_dict:
        print('No dinosaur provided.')
        return
    if not all(keys in dinosaur_dict for keys in ['name', 'diet', 'period', 'weight', 'armor', 'hybrid']):
        print('Missing dinosaur values.')
        return

    # Get dinosaur information from event 
    dino_name = dinosaur_dict.get('name')
    dino_diet = dinosaur_dict.get('diet')
    dino_period = dinosaur_dict.get('period')
    dino_weight = dinosaur_dict.get('weight')
    dino_armor = dinosaur_dict.get('armor')
    dino_hybrid = dinosaur_dict.get('hybrid')

    # Create new dinosaur object
    new_dinosaur = Dinosaur(
        name=dino_name,
        diet=dino_diet,
        period=dino_period,
        weight=dino_weight,
        armor=dino_armor,
        hybrid=dino_hybrid
    )

    # Store new dinosaur object in DynamoDB
    print(new_dinosaur.__dict__)
    response = dinosaurs_table.put_item(
    Item={
            'name': new_dinosaur.name,
            'diet': new_dinosaur.diet,
            'period': new_dinosaur.period,
            'attack': new_dinosaur.attack,
            'defense': new_dinosaur.defense,
            'life': new_dinosaur.life,
            'info': {
                'weight': new_dinosaur.weight,
                'armor': new_dinosaur.armor,
                'nature': new_dinosaur.nature,
                'hybrid': new_dinosaur.hybrid
            }
        }
    )

    print('PutItem succeeded:')
    print(json.dumps(response, indent=2))