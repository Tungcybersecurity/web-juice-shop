from flask import Blueprint, request, jsonify
import subprocess
import os

api_bp = Blueprint('api', __name__)

# VULNERABLE: Command injection endpoint
@api_bp.route('/api/execute', methods=['POST'])
def execute_command():
    # Cách 1: Trả về thông báo lỗi
    return jsonify({'error': 'Command execution is disabled for security reasons'}), 403

# VULNERABLE: File read endpoint
@api_bp.route('/api/read-file', methods=['POST'])
def read_file():
    # LỖ HỔNG: Nhận đường dẫn file từ user và đọc trực tiếp
    data = request.get_json()
    filepath = data.get('path')
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# VULNERABLE: File write endpoint
@api_bp.route('/api/write-file', methods=['POST'])
def write_file():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403
# VULNERABLE: SSRF endpoint
@api_bp.route('/api/fetch-url', methods=['POST'])
def fetch_url():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403

# VULNERABLE: NoSQL injection endpoint
@api_bp.route('/api/users/search', methods=['POST'])
def search_users():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403

# VULNERABLE: JWT token endpoint
@api_bp.route('/api/token', methods=['POST'])
def generate_token():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403

# VULNERABLE: JWT verification endpoint
@api_bp.route('/api/verify-token', methods=['POST'])
def verify_token():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403

# VULNERABLE: XML External Entity (XXE) endpoint
@api_bp.route('/api/parse-xml', methods=['POST'])
def parse_xml():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403

# VULNERABLE: Deserialization endpoint
@api_bp.route('/api/deserialize', methods=['POST'])
def deserialize_data():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403

# VULNERABLE: Directory traversal endpoint
@api_bp.route('/api/list-directory', methods=['POST'])
def list_directory():
    # LỖ HỔNG: Nhận đường dẫn thư mục từ user và liệt kê trực tiếp
    data = request.get_json()
    dirpath = data.get('path')
    try:
        files = os.listdir(dirpath)
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# VULNERABLE: Environment variables exposure
@api_bp.route('/api/env')
def get_environment():
    # VULNERABLE: Exposing sensitive environment variables
    return jsonify(dict(os.environ))

# VULNERABLE: Process information exposure
@api_bp.route('/api/processes')
def get_processes():
     return jsonify({'error': 'Command execution is disabled for security reasons'}), 403