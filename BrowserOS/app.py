from flask import Flask, render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_packages')
def get_packages():
    try:
        packages_output = subprocess.run(['rpm', '-qa'], capture_output=True, text=True).stdout.strip().split('\n')
        return jsonify({"packages": packages_output})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/get_upgrade_packages')
def get_upgrade_packages():
    result = subprocess.run(['dnf', 'check-upgrade'], stdout=subprocess.PIPE)
    result_lines = result.stdout.decode('utf-8').split('\n')
    return jsonify(results=result_lines)

@app.route('/set_volume')
def set_volume():
    level = request.args.get('level', default=50, type=int)
    subprocess.run(['amixer', 'sset', 'Master', f'{level}%'])
    return jsonify(success=True)

@app.route('/current_volume')
def current_volume():
    try:
        result = subprocess.run(['amixer', 'get', 'Master'], capture_output=True, text=True)
        volume_line = None
        for line in result.stdout.splitlines():
            print("Processing line:", line)  # Adiciona log para debug
            if 'Front Left:' in line:
                volume_line = line
                break

        if volume_line:
            volume = volume_line.split('[')[1].split('%')[0]
            return jsonify({'volume': volume})
        else:
            return jsonify({'volume': 'error', 'error': 'Volume info not found'})
    except Exception as e:
        return jsonify({'volume': 'error', 'error': str(e)})

@app.route('/get_network')
def get_network():
    try:
        device_show_output = subprocess.run(['nmcli', 'device', 'show'], capture_output=True, text=True).stdout.strip().split('\n\n')
        
        network_data = []
        for device in device_show_output:
            iface_data = {}
            lines = device.split('\n')
            for line in lines:
                if 'GENERAL.DEVICE:' in line:
                    iface_data['interface'] = line.split(':')[1].strip()
                elif 'GENERAL.TYPE:' in line:
                    iface_data['type'] = line.split(':')[1].strip()
                elif 'IP4.ADDRESS[1]:' in line:
                    iface_data['ip_lan'] = line.split(':')[1].strip().split('/')[0]
                elif 'IP4.GATEWAY:' in line:
                    iface_data['gateway'] = line.split(':')[1].strip()
                elif 'IP4.DNS[1]:' in line:
                    iface_data['dns1'] = line.split(':')[1].strip()
                elif 'IP4.DNS[2]:' in line:
                    iface_data['dns2'] = line.split(':')[1].strip()
            if iface_data:
                network_data.append(iface_data)

        public_ip = subprocess.run(['curl', 'ifconfig.me'], capture_output=True, text=True).stdout.strip()
        for iface in network_data:
            iface['ip_wan'] = public_ip

        return jsonify(network_data)
    except Exception as e:
        return jsonify({"error": str(e)})

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

