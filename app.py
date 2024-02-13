from flask import Flask, render_template, redirect, url_for
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
        print("Connected to SQL instance!")
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
        print("Connected to SQL instance!")
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
        print("Connected to SQL instance!")
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
        print("Connected to SQL instance!")
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
        print("Connected to SQL instance!")
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
        print("Connected to SQL instance!")
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


@app.route('/create', methods=['POST', 'GET'])
def create_entry():

    return render_template('entry_form.html')


def db_connection():
    con = mysql.connector.connect(host='localhost',
                                  database='fantasy_game',
                                  user='root',
                                  password=sql_pwd)
    return con


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)