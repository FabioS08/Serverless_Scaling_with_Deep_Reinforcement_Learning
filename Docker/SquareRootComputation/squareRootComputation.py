import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sqrt', methods = ['POST'])
def compute_sqrt():

    try:
    
        data = request.get_json()
        M = np.array(data['matrix'], dtype = float)
        R = np.sqrt(M)
    
        return jsonify({'result': R.tolist()})
    
    except KeyError:
        return jsonify({'error': 'Missing matrix in request'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    
    app.run(host='0.0.0.0', port=5051)
