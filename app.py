from flask import Flask, render_template, redirect, url_for, request
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)

sql_pwd = os.getenv('SERVER_PWD')


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/players', methods=['POST', 'GET'])
def display_players():

    query = 'SELECT players.player_name AS name, special_abilities.ability_name AS ability, ' \
            'pets.pet_name AS pet, i.item_name AS weapon, i2.item_name AS armor, guilds.guild_name AS guild ' \
            'FROM players ' \
            'INNER JOIN special_abilities ON players.player_abilityID = special_abilities.abilityID ' \
            'INNER JOIN pets ON players.petID = pets.petID ' \
            'INNER JOIN items AS i ON players.weaponID = i.itemID ' \
            'INNER JOIN items AS i2 ON players.armorID = i2.itemID ' \
            'INNER JOIN guilds ON players.guildID = guilds.guildID '

    headers = ['Name', 'Ability', 'Pet', 'Weapon', 'Armor', 'Guild']  # the headers for display in the table

    con = db_connection()
    if con.is_connected():
        print("Connected to MySQL instance!")
    else:
        print("Error connecting to SQL instance, route: players")
        return redirect(url_for('index'))
    cur = con.cursor()

    cur.execute(query)

    players = cur.fetchall()

    con.close()

    return render_template('players.html', entity=players, headers=headers)


@app.route('/pets', methods=['POST', 'GET'])
def display_pets():

    con = db_connection()
    if con.is_connected():
        print("Connected to MySQL instance!")
    else:
        print("Error connecting to SQL instance, route: pets")
        return redirect(url_for('index'))

    cur = con.cursor()
    cur.execute('SELECT pets.pet_name AS name, '
                'special_abilities.ability_name AS ability, '
                'pets.pet_type AS type, pets.pet_attack AS attack, '
                'pets.pet_defense AS defense '
                'FROM pets INNER JOIN special_abilities '
                'ON pets.pet_abilityID = special_abilities.abilityID')

    headers = ['Name', 'Ability', 'Type', 'Attack', 'Defense']  # the headers for display in the table

    pets = cur.fetchall()  # query all the attributes for every row

    con.close()

    return render_template('pets.html', entity=pets, headers=headers)


@app.route('/abilities', methods=['POST', 'GET'])
def display_abilities():

    con = db_connection()
    if con.is_connected():
        print("Connected to MySQL instance!")
    else:
        print("Error connecting to SQL instance, route: abilities")
        return redirect(url_for('index'))

    cur = con.cursor()
    cur.execute('SELECT special_abilities.ability_name AS name, '
                'special_abilities.ability_attack AS attack, '
                'special_abilities.ability_cost AS cost '
                'FROM special_abilities')

    headers = ['Name', 'Attack', 'Cost']  # the headers for display in the table

    abilities = cur.fetchall()  # query all the attributes for every row

    con.close()

    return render_template('abilities.html', entity=abilities, headers=headers)


@app.route('/items', methods=['POST', 'GET'])
def display_items():

    con = db_connection()
    if con.is_connected():
        print("Connected to MySQL instance!")
    else:
        print("Error connecting to SQL instance, route: items")
        return redirect(url_for('index'))

    cur = con.cursor()
    cur.execute('SELECT items.item_name AS name, '
                'items.item_type AS type, '
                'items.item_defense AS defense,'
                'items.item_attack AS attack,'
                'items.item_rarity AS rarity '
                'FROM items')

    headers = ['Name', 'Type', 'Defense', 'Attack', 'Rarity']  # the headers for display in the table

    items = cur.fetchall()  # query all the attributes for every row

    con.close()

    return render_template('items.html', entity=items, headers=headers)


@app.route('/guilds', methods=['POST', 'GET'])
def display_guilds():

    con = db_connection()
    if con.is_connected():
        print("Connected to MySQL instance!")
    else:
        print("Error connecting to SQL instance, route: guilds")
        return redirect(url_for('index'))

    cur = con.cursor()
    cur.execute('SELECT guilds.guild_name AS name, '
                'guilds.guild_color AS color '
                'FROM guilds')

    headers = ['Name', 'Color']  # the headers for display in the table

    guilds = cur.fetchall()  # query all the attributes for every row

    con.close()

    # convert color int to hex and replace value, change from tuple since immutable
    guilds_list = []
    for el in guilds:
        hex_color = hex(el[1])
        guilds_list.append([el[0], hex_color])

    return render_template('guilds.html', entity=guilds_list, headers=headers)


@app.route('/alliances', methods=['POST', 'GET'])
def display_alliances():

    con = db_connection()
    if con.is_connected():
        print("Connected to MySQL instance!")
    else:
        print("Error connecting to SQL instance, route: alliances")
        return redirect(url_for('index'))

    cur = con.cursor()
    cur.execute('SELECT alliances.alliance_name AS name '
                'FROM alliances')

    headers = ['Name']  # the headers for display in the table

    alliances = cur.fetchall()  # query all the attributes for every row

    con.close()

    return render_template('alliances.html', entity=alliances, headers=headers)


@app.route('/create-entry-form', methods=['POST', 'GET'])
def create_entry_form():

    # get the entry type from the form dropdown
    select = request.form.get('entry-type')

    # get attributes (foreign key fields) for dropdowns for each category by case
    con = db_connection()
    cur = con.cursor()

    # TODO COMMENT THESE QUERIES
    ability_query = 'SELECT special_abilities.ability_name FROM special_abilities'
    pet_query = 'SELECT pets.pet_name FROM pets'
    weapon_query = 'SELECT items.item_name FROM items WHERE items.item_type = "weapon"'
    armor_query = 'SELECT items.item_name FROM items WHERE items.item_type ="armor"'
    guild_query = 'SELECT guilds.guild_name FROM guilds'
    pet_type_query = 'SELECT DISTINCT pets.pet_type FROM pets'

    # create empty queries for cases that the attribute isn't necessary
    fields = []
    abilities = []
    pets = []
    weapons = []
    armors = []
    guilds = []
    pet_types = []

    # these aren't nested, they don't have their own queries because they are static
    item_types = ['sword', 'armor']
    item_rarities = ['common', 'uncommon', 'rare', 'epic', 'legendary']

    match select:
        case "Player":
            fields = ['Name', 'Ability', 'Pet', 'Weapon', 'Armor', 'Guild']
            # get abilities for dropdown
            cur.execute(ability_query)
            abilities = cur.fetchall()

            # get pets for dropdown
            cur.execute(pet_query)
            pets = cur.fetchall()

            # get weapons for dropdown
            cur.execute(weapon_query)
            weapons = cur.fetchall()

            # get armors for dropdown
            cur.execute(armor_query)
            armors = cur.fetchall()

            # get guilds for dropdown
            cur.execute(guild_query)
            guilds = cur.fetchall()

        case "Pet":
            fields = ['Name', 'Ability', 'Pet Type', 'Attack', 'Defense']

            # get abilities for dropdown
            cur.execute(ability_query)
            abilities = cur.fetchall()

            # get abilities for dropdown
            cur.execute(pet_type_query)
            pet_types = cur.fetchall()

        case "Ability":
            fields = ['Name', 'Attack', 'Cost']

        case "Item":
            fields = ['Name', 'Item Type', 'Defense', 'Attack', 'Rarity']

        case "Guild":
            fields = ['Name', 'Color']

        case "Alliance":
            fields = ['Name']

    con.close()

    return render_template('entry_form.html', select_type=select, fields=fields, abilities=abilities, pets=pets,
                           weapons=weapons, armors=armors, item_types=item_types, guilds=guilds,
                           item_rarity=item_rarities, pet_types=pet_types)


@app.route('/create-db-entry', methods=['POST'])
def create_db_entry():

    con = db_connection()
    cur = con.cursor()

    query = ''
    values = []

    select_type = request.form.get('select-type')
    match select_type:
        case 'Player':
            fields = ['Name', 'Ability', 'Pet', 'Weapon', 'Armor', 'Guild']
            for i in range(len(fields)):
                values.append(request.form.get(fields[i]))

            query = f"""INSERT INTO players (players.player_name, players.player_abilityID, players.petID, players.weaponID, players.armorID, players.guildID) 
                VALUES ('{values[0]}', (SELECT special_abilities.abilityID FROM special_abilities WHERE special_abilities.ability_name = '{values[1]}'),
                (SELECT pets.petID FROM pets WHERE pets.pet_name = '{values[2]}'),
                (SELECT items.itemID FROM items WHERE items.item_name = '{values[3]}'), 
                (SELECT items.itemID FROM items WHERE items.item_name = '{values[4]}'), 
                (SELECT items.guildID FROM guilds WHERE items.guild_name = '{values[5]}'));"""

        case 'Pet':
            # todo validate the attack and defense to be integers
            fields = ['Name', 'Ability', 'Pet Type', 'Attack', 'Defense']
            for i in range(len(fields)):
                values.append(request.form.get(fields[i]))
            query = f"""INSERT INTO pets (pets.pet_name, pets.pet_abilityID, pets.pet_type, pets.pet_attack, pets.pet_defense) 
                VALUES ('{values[0]}', (SELECT special_abilities.abilityID FROM special_abilities WHERE special_abilities.ability_name = '{values[1]}'), 
                '{values[2]}', {int(values[3])}, {int(values[4])})"""

        case 'Ability':
            # todo validate the attack and cost to be integers
            fields = ['Name', 'Attack', 'Cost']
            for i in range(len(fields)):
                values.append(request.form.get(fields[i]))
            query = f"""INSERT INTO special_abilities (special_abilities.ability_name, special_abilities.ability_attack, 
                special_abilities.ability_cost) VALUES ('{values[0]}', {int(values[1])}, {int(values[2])})"""

        case 'Item':
            # todo validate the defense and attack to be integers
            fields = ['Name', 'Item Type', 'Defense', 'Attack', 'Rarity']
            for i in range(len(fields)):
                values.append(request.form.get(fields[i]))
            query = f"""INSERT INTO items (items.item_name, items.item_type, items.item_defense, items.item_attack, items.item_rarity) 
                VALUES ('{values[0]}', '{values[1]}', {int(values[2])}, {int(values[3])}, '{values[4]}')"""

        case 'Guild':
            # todo validate the color entry to be an integer
            fields = ['Name', 'Color']
            for i in range(len(fields)):
                values.append(request.form.get(fields[i]))
            query = f"""INSERT INTO guilds (guilds.guild_name, guilds.guild_color) 
                VALUES ('{values[0]}', {int(values[1])})"""

        case 'Alliance':
            # only 1 value in the return form here, just put it in the query
            query = f"""INSERT INTO alliances (alliances.alliance_name) 
                VALUES ('{request.form.get('Name')}')"""

    cur.execute(query)
    con.commit()
    con.close()

    message = 'Record Created!'

    return render_template('status_message.html', message=message)


@app.route('/create-update-form', methods=['POST'])
def create_update_form():

    # need to check form hidden attribute which will contain the update type
    select = request.form.get('update-type')

    con = db_connection()
    cur = con.cursor()

    ability_query = 'SELECT special_abilities.ability_name FROM special_abilities'
    pet_query = 'SELECT pets.pet_name FROM pets'
    weapon_query = 'SELECT items.item_name FROM items WHERE items.item_type = "weapon"'
    armor_query = 'SELECT items.item_name FROM items WHERE items.item_type = "armor"'
    guild_query = 'SELECT guilds.guild_name FROM guilds'

    fields = []
    abilities = []
    pets = []
    weapons = []
    armors = []
    guilds = []

    # TODO FINISH CASES
    match select:
        case 'Player':
            fields = ['Name', 'Ability', 'Pet', 'Weapon', 'Armor', 'Guild']

            cur.execute(ability_query)
            abilities = cur.fetchall()

            cur.execute(pet_query)
            pets = cur.fetchall()

            cur.execute(weapon_query)
            weapons = cur.fetchall()

            cur.execute(armor_query)
            armors = cur.fetchall()

            cur.execute(guild_query)
            guilds = cur.fetchall()

        case 'Item':
            fields = ['Name', 'Item Type', 'Defense', 'Attack', 'Rarity']

    return render_template('update_form.html', select_type=select, fields=fields, abilities=abilities, pets=pets,
                           weapons=weapons, armors=armors, guilds=guilds)


@app.route('/update')
def update_db_entry():

    # TODO ADD SQL FOR ENTRIES
    select = request.form.get('select-type')

    match select:
        case 'Player':
            fields = ['Name', 'Ability', 'Pet', 'Weapon', 'Armor', 'Guild']

    print('update successful')

    return redirect(url_for('index'))


@app.route('/delete', methods=['POST'])
def delete_db_entry():

    select = request.form.get('delete-type')

    con = db_connection()
    cur = con.cursor()

    query = ''
    record = request.form.get('record')

    match select:
        case 'Player':
            query = f"""DELETE FROM players WHERE players.player_name = '{record}'"""
        case 'Pet':
            query = f"""DELETE FROM pets WHERE pets.pet_name = '{record}'"""
        case 'Ability':
            query = f"""DELETE FROM special_abilities WHERE special_abilities.ability_name = '{record}'"""
        case 'Item':
            query = f"""DELETE FROM items WHERE items.item_name = '{record}'"""
        case 'Guild':
            query = f"""DELETE FROM guilds WHERE guilds.guild_name = '{record}'"""
        case 'Alliance':
            query = f"""DELETE FROM alliances WHERE alliances.alliance_name = '{record}'"""

    cur.execute(query)
    con.commit()
    con.close()

    message = 'Record Deleted!'

    return render_template('status_message.html', message=message)


def db_connection():
    con = mysql.connector.connect(host='localhost',
                                  database='fantasy_game',
                                  user='root',
                                  password=sql_pwd)
    return con


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)