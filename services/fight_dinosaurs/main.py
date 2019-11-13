import boto3
from boto3.dynamodb.conditions import Key, Attr
import random
import json
from dinosaur import Dinosaur

dynamodb = boto3.resource('dynamodb')
dinosaurs_table = dynamodb.Table('dinosaurs')


def handler(event, context):
    """
    The function to fight two random dinosaurs from DynamoDB
    """
    dinosaur_carnivore_list = dinosaurs_table.scan(
        FilterExpression=Attr('diet').eq('carnivore'),
        ProjectionExpression='#name',
        ExpressionAttributeNames={ '#name': 'name' }
    )['Items']

    dinosaur_herbivore_list = dinosaurs_table.scan(
        FilterExpression=Attr('diet').eq('herbivore'),
        ProjectionExpression='#name',
        ExpressionAttributeNames={ '#name': 'name' }
    )['Items']
    
    carnivore = random.choice(dinosaur_carnivore_list)
    herbivore = random.choice(dinosaur_herbivore_list)

    dino_data_1 = dinosaurs_table.query(
        KeyConditionExpression=Key('name').eq(carnivore['name'])
    )['Items'][0]

    dino_data_2 = dinosaurs_table.query(
        KeyConditionExpression=Key('name').eq(herbivore['name'])
    )['Items'][0]

    dino_1 = Dinosaur(
        name=dino_data_1['name'],
        diet=dino_data_1['diet'],
        period=dino_data_1['period'],
        weight=dino_data_1['info']['weight'],
        armor=dino_data_1['info']['armor'],
        hybrid=dino_data_1['info']['hybrid'],
        nature=dino_data_1['info']['nature'], 
        attack=dino_data_1['attack'],
        defense=dino_data_1['defense'],
        life=dino_data_1['life']
    )

    dino_2 = Dinosaur(
        name=dino_data_2['name'],
        diet=dino_data_2['diet'],
        period=dino_data_2['period'],
        weight=dino_data_2['info']['weight'],
        armor=dino_data_2['info']['armor'],
        hybrid=dino_data_2['info']['hybrid'],
        nature=dino_data_2['info']['nature'], 
        attack=dino_data_2['attack'],
        defense=dino_data_2['defense'],
        life=dino_data_2['life']
    )

    battle_turns = 0
    print(f'A wild {dino_1.name} and {dino_2.name} encounter!')
    print('---------------------------------')
    print('THE HUNT HAS STARTED!')
    while (True):
        print('---------------------------------')
        print(f'Turn {battle_turns} status:')
        print(f'Dino 1: {dino_1.name}')
        print(f'Life  : {dino_1.life}')
        print(f'Dino 2: {dino_2.name}')
        print(f'Life  : {dino_2.life}')
        dino_2.update_life(dino_1.make_attack())
        if(dino_2.is_dead()):
           winner = dino_1
           loser = dino_2
           break
        dino_1.update_life(dino_2.make_attack())
        if(dino_1.is_dead()):
            winner = dino_2
            loser = dino_1
            break
        battle_turns += 1
    
    announce_winner(winner, loser)

def announce_winner(winner, loser):
    print('---------------------------------')
    print(f'THE HUNT IS OVER')
    print('---------------------------------')
    if(winner.diet == 'herbivore'):
        print(f'{winner.name} has fended off {loser.name} with {winner.life} life points to spare...')
    else:
        print(f'{winner.name} has hunted {loser.name} with {winner.life} life points to spare...')