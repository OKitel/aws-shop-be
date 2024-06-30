#!/bin/bash

# Populate products

aws dynamodb put-item --table-name Products --item '{"id": {"S":  "01904089-3efe-748f-8c38-18b1346c7f7f"},    "title": {"S": "Terraforming Mars"},  "description": {"S":  "In Terraforming Mars, players take the role of corporations working together to terraform the planet Mars by raising the temperature, adding oxygen to the atmosphere, covering the planets surface with water and creating plant and animal life."},  "price":{"N":  "35"},    "img": {"S": "terraforming-mars.jpg"}}'

aws dynamodb put-item --table-name Products --item '{"id": {"S":  "01904089-8cba-7037-bce4-c69262b9e750"},    "title": {"S": "Wingspan"},  "description": {"S":  "Wingspan is a competitive, medium-weight, card-driven, engine-building board game from Stonemaier Games. The winner is the player with the most points accumulated from birds, bonus cards, end-of-round goals, eggs, cached food, and tucked birds."},  "price":{"N":  "40"},    "img": {"S": "wingspan.jpg"}}'

aws dynamodb put-item --table-name Products --item '{"id": {"S":  "01904089-8cba-735b-8e54-05bb1d18ae4f"},    "title": {"S": "Everdell"},  "description": {"S":  "Everdell is a worker placement game for 2-4 players, set in a lush, woodland valley. Elements of hand- and resource-management play their part, too. Over the course of four seasons, you will compete to create a tableau of gorgeous cards. Which Constructions will you place in your greenwood city?"},  "price":{"N":  "45"},    "img": {"S": "everdell.jpg"}}'

aws dynamodb put-item --table-name Products --item '{"id": {"S":  "01904089-8cba-7ff7-937d-578e7c759808"},    "title": {"S": "Ticket to Ride"},  "descy train adventure in which players collect and plaription": {"S":  "Ticket to Ride is a cross-country matching train cards to claim railway routes connecting cities throughout North America."},  "price":{"N":  "47"},    "img": {"S": "ticket-to-ride.jpg"}}'

aws dynamodb put-item --table-name Products --item '{"id": {"S":  "01904089-8cba-7984-b426-077bede0a152"},    "title": {"S": "Carcassonne"},  "description": {"S":  "Carcassonne is a tile-laying game wd the medieval French city of Carcassonne while cohere players collectively construct the area arounmpeting to place followers on various features and score the most points."},  "price":{"N":  "25"},    "img": {"S": "carcassonne.jpg"}}'

aws dynamodb put-item --table-name Products --item '{"id": {"S":  "01904089-8cba-7c7d-9475-9824ae906c94"},    "title": {"S": "7 Wonders Duel"},  "description": {"S":  "In 7 Wonders Duel, each player is leading a civilization and will, over the course of 3 ages, construct Buildings and Wonders. Each card represents a Building which helps the player to strengthen their army, make scientific discoveries or develop their city."},  "price":{"N":  "20"},    "img": {"S": "7-wonders-duel.jpg"}}'

aws dynamodb put-item --table-name Products --item '{"id": {"S":  "01904089-8cba-7d26-bd02-d440553782af"},    "title": {"S": "Dune: Imperium"},  "description": {"S":  "Dune: Imperium is a 2020 board game designed by Paul Dennen and published by Dire Wolf Digital. In the board game, which is set in Frank Herbert''s Dune universe, players use deck-building and worker placement to gain alliances with factions and combat to earn victory points."},  "price":{"N":  "40"},    "img": {"S": "dune-imperium.jpg"}}'

# Populate stocks

aws dynamodb put-item --table-name Stocks --item '{"product_id": {"S":  "01904089-3efe-748f-8c38-18b1346c7f7f"},  "count":{"N":  "15"}}'

aws dynamodb put-item --table-name Stocks --item '{"product_id": {"S":  "01904089-8cba-7037-bce4-c69262b9e750"},  "count":{"N":  "10"}}'

aws dynamodb put-item --table-name Stocks --item '{"product_id": {"S":  "01904089-8cba-735b-8e54-05bb1d18ae4f"},  "count":{"N":  "10"}}'

aws dynamodb put-item --table-name Stocks --item '{"product_id": {"S":  "01904089-8cba-7ff7-937d-578e7c759808"},  "count":{"N":  "15"}}'

aws dynamodb put-item --table-name Stocks --item '{"product_id": {"S":  "01904089-8cba-7984-b426-077bede0a152"},  "count":{"N":  "20"}}'

aws dynamodb put-item --table-name Stocks --item '{"product_id": {"S":  "01904089-8cba-7c7d-9475-9824ae906c94"},  "count":{"N":  "10"}}'

aws dynamodb put-item --table-name Stocks --item '{"product_id": {"S":  "01904089-8cba-7d26-bd02-d440553782af"},  "count":{"N":  "5"}}'