from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from werkzeug.exceptions import RequestEntityTooLarge

from encoder import check_bits_usage, encode_png
from decoder import decode_png
from valid_uuid import validate_uuid

import cv2
import os
import magic
import uuid as uuidgen

app = Flask(__name__)

UPLOAD_FOLDER = 'files'
ALLOWED_EXTENSIONS = {'png'}

# 512KiB
MAX_CONTENT_LENGTH = 512 * 1024 

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get-encoded-file/<uuid>/<file_uuid>', methods=['GET'])
def get_encoded_file(uuid, file_uuid):
    if not validate_uuid(uuid) or not validate_uuid(file_uuid):
        return jsonify({'status': 'error', 'message': 'Invalid UUID format'})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid, file_uuid + '.png')

    if os.path.isfile(file_path):
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], uuid), file_uuid + '.png')
    else:
        return jsonify({'status': 'error', 'message': 'File not found'})

@app.route('/get-uploaded-file/<uuid>', methods=['GET'])
def get_uploaded_file(uuid):
    if not validate_uuid(uuid):
        return jsonify({'status': 'error', 'message': 'Invalid UUID format'})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid, 'original.png')

    if os.path.isfile(file_path):
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], uuid), 'original.png')
    else:
        return jsonify({'status': 'error', 'message': 'File not found'})

@app.route('/decode-file/<uuid>', methods=['POST'])
def decode_file(uuid):
    try:
        # Check if UUID exists (check if the directory and origin.png exist)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid)
        if not os.path.exists(folder_path) or not os.path.exists(os.path.join(folder_path, 'original.png')):
            return jsonify({'status': 'UUID_NOT_FOUND', 'message': 'UUID does not exist'})

        data = request.json
        r_bits = data.get('r_bits', [])
        g_bits = data.get('g_bits', [])
        b_bits = data.get('b_bits', [])
        end_key = data.get('end_key', "==END==")

        if not check_bits_usage(r_bits, g_bits, b_bits):
            return jsonify({'status': 'BAD_BITS', 'message': 'Bits selection are bad'})

        if not end_key:
            return jsonify({'status': 'EMPTY_KEY', 'message': 'Ending encode key is empty'})

        file_path = os.path.join(folder_path, 'original.png')
        decode_response = decode_png(file_path, end_key, r_bits, g_bits, b_bits)

        return jsonify({'status': 'SUCCESS', 'key_used': decode_response["found"], 'message': decode_response["decoded"]})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'ERROR', 'message': "Unknown error"})


@app.route('/encode-file/<uuid>', methods=['POST'])
def encode_file(uuid):
    try:
        # Check if UUID exists (check if the directory and origin.png exist)
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid)
        if not os.path.exists(folder_path) or not os.path.exists(os.path.join(folder_path, 'original.png')):
            return jsonify({'status': 'UUID_NOT_FOUND', 'message': 'UUID does not exist'})

        data = request.json
        r_bits = data.get('r_bits', [])
        g_bits = data.get('g_bits', [])
        b_bits = data.get('b_bits', [])
        to_encode = data.get('to_encode', "")
        end_key = data.get('end_key', "==END==")

        if not check_bits_usage(r_bits, g_bits, b_bits):
            return jsonify({'status': 'BAD_BITS', 'message': 'Bits selection are bad'})

        if not to_encode:
            return jsonify({'status': 'EMPTY_MESSAGE', 'message': 'Message to encode is empty'})

        if not end_key:
            return jsonify({'status': 'EMPTY_KEY', 'message': 'Ending encode key is empty'})


        # Generate UUID
        file_uuid = str(uuidgen.uuid4())

        file_path = os.path.join(folder_path, 'original.png')
        image = encode_png(file_path, to_encode, end_key, r_bits, g_bits, b_bits)

        # Save...
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uuid, file_uuid + ".png")
        cv2.imwrite(file_path, image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
        return jsonify({'status': 'SUCCESS', 'message': 'UUID and array of numbers are valid', 'uuid': file_uuid})
    except ValueError:
        return jsonify({'status': 'PAYLOAD_TOO_LARGE', 'message': "Payload is too large for the file, consider lowing the payload size!"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'ERROR', 'message': "Unknown error"})


@app.route('/encode-upload', methods=['POST'])
def upload_file():
    try:
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return jsonify({'status': 'BAD', 'message': 'No file part'})

        file = request.files['file']

        # Simple malware check...
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(file.read(1024))

        if not file_mime_type.startswith('image/png'):
            return jsonify({'status': 'BAD_TYPE', 'message': 'File is not a PNG'})

        # Check if the file is empty
        if file.filename == '':
            return jsonify({'status': 'BAD', 'message': 'No selected file'})

        # Check if file size does not exceed configured size
        if file.content_length is not None and file.content_length > MAX_CONTENT_LENGTH:
            return jsonify({'status': 'SIZE_EXCEED', 'message': 'File size exceeds limit'})

        # Check if the file is allowed
        if not allowed_file(file.filename):
            return jsonify({'status': 'BAD_TYPE', 'message': 'File type not allowed'})

        # Generate UUID
        file_uuid = str(uuidgen.uuid4())

        # Save...
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], file_uuid)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, 'original.png')
        file.seek(0)
        file.save(file_path)

        return jsonify({'status': 'SUCCESS', 'uuid': file_uuid})
    except RequestEntityTooLarge:
        return jsonify({'status': 'SIZE_EXCEED', 'message': 'File size exceeds limit'})
    except Exception:
        import traceback
        traceback.print_exc()
        return jsonify({'status': 'BAD', 'message': 'Server encountered error'})

@app.route('/ping')
def ping():
    return 'pong'

if __name__ == '__main__':
    DEBUG_ENABLED = os.getenv("IS_DEBUG") == "true"
    app.run(debug=DEBUG_ENABLED, port=8080, host='0.0.0.0')