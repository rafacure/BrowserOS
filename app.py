from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/set_volume')
def set_volume():
    level = request.args.get('level', default=50, type=int)
    subprocess.run(['amixer', 'sset', 'Master', f'{level}%'])
    return jsonify(success=True)

@app.route('/network_info')
def network_info():
    local_ip = subprocess.run(['hostname', '-I'], capture_output=True, text=True).stdout.strip()
    public_ip = subprocess.run(['curl', 'ifconfig.me'], capture_output=True, text=True).stdout.strip()
    dns_servers = subprocess.run(['nmcli', 'dev', 'show'], capture_output=True, text=True).stdout.splitlines()
    gateway = subprocess.run(['ip', 'route'], capture_output=True, text=True).stdout.splitlines()[0].split()[2]

    dns_list = [line.split()[1] for line in dns_servers if 'IP4.DNS' in line]
    
    return jsonify({
        'localIP': local_ip,
        'publicIP': public_ip,
        'dnsServers': dns_list,
        'gateway': gateway
    })

@app.route('/get_packages')
def get_packages():
    cmd = 'rpm -qa | sort'
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    packages = result.stdout.splitlines()
    return jsonify({'packages': packages})

@app.route('/keyboard_layouts')
def keyboard_layouts():
    result = subprocess.run(['localectl', 'list-keymaps'], capture_output=True, text=True)
    layouts = result.stdout.splitlines()
    return jsonify({'layouts': layouts})

@app.route('/set_keyboard_layout')
def set_keyboard_layout():
    layout = request.args.get('layout')
    cmd = f'localectl set-keymap {layout}'
    subprocess.run(cmd, shell=True)
    return jsonify(success=True)

@app.route('/current_keyboard_layout')
def current_keyboard_layout():
    result = subprocess.run(['localectl', 'status'], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if 'VC Keymap' in line:
            current_layout = line.split(':')[1].strip()
            return jsonify({'layout': current_layout})
    return jsonify({'layout': 'unknown'})

if __name__ == '__main__':
    app.run(debug=True)

