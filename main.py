from flask import Flask,request,jsonify
from flask_restful import Resource,Api
from Raj_sqlite import *
import pandas as pd

app = Flask(__name__)
api = Api(app)

def get_db_data():
    conn_db   = sqlite3.connect('Fr_details.db',detect_types=sqlite3.PARSE_DECLTYPES)
    conn      = conn_db.cursor()
    res = get_data(conn,'Demographic_details')   
    df = pd.DataFrame(data = res,columns=['ID','Name','DOB','City','State','Pincode','Embeddings'])
    df.drop(['Embeddings'],inplace=True,axis=1)
    dic = df.T.to_dict('list')
    return dic

def db_search(id_,name_,tabel_name):
    conn_db   = sqlite3.connect('Fr_details.db',detect_types=sqlite3.PARSE_DECLTYPES)
    conn      = conn_db.cursor()
    q = f"""SELECT * FROM {tabel_name} WHERE ID == {id_} AND Name == '{name_}';"""
    conn.execute(q)
    match_details = conn.fetchall()
    if match_details != []:
        for details in match_details:
            return {'Id':details[0],'Name':details[1],'Match':'Yes'}
    else:
        return {'Match':'No'}
    
class Match(Resource):
    def get(self):
        dic = get_db_data()
        return jsonify(dic)
          
    def post(self):
        data = request.get_json()
        return db_search(data['Id'],data['Name'],'Demographic_details')

        
    
api.add_resource(Match,'/')
app.run(debug=True)


