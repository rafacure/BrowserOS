from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    result = subprocess.run(['rpm', '-qa'], capture_output=True, text=True)
    packages = result.stdout.splitlines()
    return render_template('index.html', packages=packages)

@app.route('/set_volume')
def set_volume():
    level = request.args.get('level')
    subprocess.run(['amixer', 'set', 'Master', f'{level}%'])
    return jsonify({'status': 'success', 'level': level})

if __name__ == '__main__':
    app.run(debug=True)

