# proxy_api.py (deploy on Railway)
from flask import Flask, jsonify, request
import pymssql

app = Flask(__name__)

@app.route('/api/query', methods=['POST'])
def query():
    # This runs on Railway (can connect to Azure SQL)
    sql = request.json.get('sql')
    
    conn = pymssql.connect(
        server='fseb.database.windows.net',
        database='fseb',
        user='fseb_admin',
        password='Welcome1'
    )
    
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    
    return jsonify({'results': results})