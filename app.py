from flask import Flask,request,jsonify
from flask_restful import Resource,Api
import pandas as pd
import sqlite3

app = Flask(__name__)
api = Api(app)



@app.route('/', methods=['POST'])
def db_search():
    data = request.get_json()
    conn_db   = sqlite3.connect('Fr_details.db',detect_types=sqlite3.PARSE_DECLTYPES)
    conn      = conn_db.cursor()
    q = f"""SELECT * FROM Demographic_details WHERE ID == {data['Id']} AND Name == '{data['Name']}';"""
    conn.execute(q)
    match_details = conn.fetchall()
    if match_details != []:
        for details in match_details:
            return {'Id':details[0],'Name':details[1],'Match':'Yes'}
    else:
        return {'Match':'No'}
    
class Match(Resource):
    def get(self):
        return "Hello"
          
    def post(self):
        return db_search()
    
api.add_resource(Match,'/')

if __name__ == '__main__':
    app.run(debug=True)


