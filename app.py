import tempfile
from flask import Flask, request
import docker

app = Flask(__name__)
client = docker.from_env()

@app.route('/run', methods=['POST'])
def run_function():
    code = request.data.decode()
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".py") as f:
        f.write(code)
        temp_file_path = f.name
    try:
        result = client.containers.run('python:3.7', f'python {temp_file_path}', remove=True, 
                               volumes={'/path/to/your/app': {'bind': '/app', 'mode': 'rw'}})
        return result
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run(port=5000)
