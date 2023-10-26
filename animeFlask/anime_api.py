from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

#Database configuration (change password)

config = {
    'user': 'root',
    'password': 'password',
    'host': 'localhost',
    'database': 'animeDB',
    'raise_on_warnings': True
}

#Get all Anime
@app.route('/anime', methods=['GET'])
def get_all_amime():
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Anime")
        anime = cursor.fetchall()
    except Error as e:
        return jsonify({"error":str(e)}), 500
    finally:
        cursor.close()
        connection.close()
    return jsonify(anime)

#Get recommendations based on Genre and Size of anime
@app.route('/recommendation', methods=['GET'])
def get_recommendations():
    genre = request.args.get('genre')
    size = request.args.get('size')

    if not genre or not size:
        return jsonify({"error":"Please provide both genre and size"}), 400
    
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Anime WHERE genre LIKE %s AND size=%s LIMIT 10"
        cursor.execute(query, ('%' + genre +'%', size))
        recommendations = cursor.fetchall()
    except Error as e:
        return jsonify({"error":str(e)}), 500
    finally:
        cursor.close()
        connection.close()
    return jsonify(recommendations)

#Get anime ID
@app.route('/anime/<int:anime_id>', methods=['GET'])
def get_anime_by_id(anime_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Anime WHERE id=%s", (anime_id,))
        anime = cursor.fetchone()
        if not anime:
            return jsonify({"error": "Anime not found"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
    return jsonify(anime)

#Search enginer trial
@app.route('/anime/search', methods=['GET'])
def search_anime():
    name = request.args.get('name')
    genre = request.args.get('genre')

    query = "SELECT * FROM Anime WHERE 1=1"
    params = []

    if name:
        query += " AND name LIKE %s"
        params.append('%' + name + '%')
    if genre:
        query += " AND genre LIKE %s"
        params.append('%' + genre + '%')

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()
        
    return jsonify(results)

#Enter via anime id
@app.route('/anime/<int:anime_id>', methods=['PUT'])
def update_anime(anime_id):
    data = request.get_json()
    set_values = []
    params = []

    for key, value in data.items():
        set_values.append(f"{key}=%s")
        params.append(value)

    query = f"UPDATE Anime SET {', '.join(set_values)} WHERE id=%s"
    params.append(anime_id)

    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "No record updated, check the id"}), 400
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "Anime updated successfully"})

#Delete entry
@app.route('/anime/<int:anime_id>', methods=['DELETE'])
def delete_anime(anime_id):
    try:
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("DELETE FROM Anime WHERE id=%s", (anime_id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"message": "No record deleted, check the id"}), 400
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({"message": "Anime deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)