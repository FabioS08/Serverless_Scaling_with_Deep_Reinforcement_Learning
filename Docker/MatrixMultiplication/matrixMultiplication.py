import numpy as np
import time
import datetime
import os
import json
import requests
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

lock = threading.Lock()

# Get the pod's name and, in the case in which it is not present, it returns a 
# default value (e.g. when we run the bare docker image out of kubernetes)
podName = os.getenv("pod_name", "[ERROR] Unknown Pod")
 

@app.route('/multiply', methods = ['POST'])
def multiply_matrices():
    
    # As soon as the request arrives, we register the timestamp (we consider the milliseconds as well
    # to avoid that fast responses will overwrite the files)
    timestamp = datetime.datetime.now().strftime("%Y.%m.%d_%H:%M:%S.%f")[:-3]

    # We take the time in which the ingress received the request
    requestTimeValue = request.headers.get('requestTime')
    requestTime = float(requestTimeValue.lstrip('t='))

    # Get JSON data from request
    data = request.get_json()
    
    # Extract matrices from request
    try:

        A = np.array(data['matrix_a'], dtype = float)
        B = np.array(data['matrix_b'], dtype = float)
        sqrtFlag = bool(data.get('sqrt', False))
        
        # Validate matrices can be multiplied
        if A.shape[1] != B.shape[0]:

            return jsonify({'error': f"Matrix dimensions don't match for multiplication. A: {A.shape}, B: {B.shape}"}), 400
        
        # Create results directory if it doesn't exist
        os.makedirs("results", exist_ok = True)
        
        # Ensure exclusive access for consistent timing
        with lock:                          

            start = time.perf_counter()
            C = np.dot(A, B)
            end = time.perf_counter()

        endTime = time.time()
        
        # Compute the response and service time  
        serviceTime = end - start
        responseTime = endTime - requestTime

        # Generate a unique filename based on timestamp
        filename = f"{podName}_{timestamp}.json"
        filepath = os.path.join("results", filename)

        # Prepare data for JSON output
        data = {

            "Service Time": round(serviceTime, 12),
            "Response Time": round(responseTime, 12)
        
        }

        # Write results to JSON file
        with open(filepath, "w") as f:

            json.dump(data, f, indent = 4)
        
        # Return results
        if not sqrtFlag:
            
            return jsonify({
                'message': f"Matrix multiplication completed!",
                'Service Time': serviceTime,
                'Result': C[:5, :5].tolist() if min(C.shape) >= 5 else C.tolist()
            })
        
        sqrtResp = requests.post('http://sqrt-service/sqrt', json = {'matrix': C.tolist()}, timeout = 10)

        if not sqrtResp.ok:

            return jsonify({
            
                'error': 'Square-root Service Error',
                'details': sqrtResp.text
            
            }), 502
        
        sqrtMatrix = sqrtResp.json().get('result')

        return jsonify({

            'message': "Matrix multiplication + Square Root completed!",
            'Original Matrix': C[:5, :5].tolist() if min(C.shape) >= 5 else C.tolist(),
            'Square Rooted Matrix': sqrtMatrix[:5][:5] if hasattr(sqrtMatrix, '__getitem__') else sqrtMatrix
        })

    
    except KeyError:

        return jsonify({'error': 'Missing matrix_a or matrix_b in request'}), 400
    
    except Exception as e:
        
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":

    app.run(host = '0.0.0.0', port = 5050)