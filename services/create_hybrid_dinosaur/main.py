import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
import json
import decimal
from dinosaur import Dinosaur

dynamodb = boto3.resource('dynamodb')
dinosaurs_table = dynamodb.Table('dinosaurs')


def handler(event, context):
    """
    The function to create a new hybrid dinosaur by combining 2
    dinosaurs from DynamoDB and storing the new dinosaur in DynamoDB
    """
    
    # Get names of all dinosaurs in DynamoDB table
    dinosaur_list = dinosaurs_table.scan(
        FilterExpression=Attr('info.hybrid').eq(False),
        ProjectionExpression='#name',
        ExpressionAttributeNames={ '#name': 'name' }
    )['Items']

    if len(dinosaur_list) < 2:
        print('Need at least 2 dinosaurs to create hybrid.')
        return
    
    # Select 2 random dinosaurs to create hybrid from
    dinosaur_pair = random.sample(dinosaur_list, k=2)

    #Get dinosaur information for each selected dinosaur
    dino_1 = dinosaurs_table.query(
        KeyConditionExpression=Key('name').eq(dinosaur_pair[0]['name'])
    )['Items'][0]
    dino_2 = dinosaurs_table.query(
        KeyConditionExpression=Key('name').eq(dinosaur_pair[1]['name'])
    )['Items'][0]

    # Generate hybrid dinosaur name
    dino_1_name = dino_1['name'].split(' ')
    dino_2_name = dino_2['name'].split(' ')
    dino_name = (dino_1_name[0][:5] + dino_2_name[0][-6:]).capitalize() + ' ' + dino_2_name[1][:3] + dino_1_name[1][-5:]
    
    # Specify hybrid dinosaur diet
    if dino_1['diet'] == dino_2['diet']:
        dino_diet = dino_1['diet']
    else:
        dino_diet = random.choice(['carnivore', 'herbivore'])

    # Set hybrid dinosaur period (current period)
    dino_period = 'Quaternary'

    # Calculate hybrid dinosaur weight based on random distribution
    dino_weight_dist1 = round(random.random(),2)
    dino_weight_dist2 = 1 - dino_weight_dist1
    dino_weight = (dino_1['info']['weight'] * decimal.Decimal(dino_weight_dist1)) + (dino_2['info']['weight'] * decimal.Decimal(dino_weight_dist2))

    # Specify if hybrid has armor
    if dino_1['info']['armor'] == dino_2['info']['armor']:
        dino_armor = dino_1['info']['armor']
    else:
        dino_armor = random.random() < 0.5

    # Create hybrid dinosaur object
    new_hybrid_dinosaur = Dinosaur(
        name=dino_name,
        diet=dino_diet,
        period=dino_period,
        weight=dino_weight,
        armor=dino_armor,
        hybrid=True
    )

    # Store hybrid dinosaur object in DynamoDB
    response = dinosaurs_table.put_item(
    Item={
            'name': new_hybrid_dinosaur.name,
            'diet': new_hybrid_dinosaur.diet,
            'period': new_hybrid_dinosaur.period,
            'attack': new_hybrid_dinosaur.attack,
            'defense': new_hybrid_dinosaur.defense,
            'life': new_hybrid_dinosaur.life,
            'info': {
                'weight': new_hybrid_dinosaur.weight,
                'armor': new_hybrid_dinosaur.armor,
                'nature': new_hybrid_dinosaur.nature,
                'hybrid': new_hybrid_dinosaur.hybrid
            }
        }
    )

    print('PutItem succeeded:')
    print(json.dumps(response, indent=2))