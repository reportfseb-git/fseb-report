from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/')
def home():
    return '<h1> Live!</h1><p>Test on phone</p>'
@app.route('/api/test')
def test():
    return jsonify({'status': 'ok'})
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
