# @app.route('/')
# def index():
#     # Admin View: Anaona majina yote na anaweza ku-manage
#     stats = {
#         'pending': len([a for a in appointments if a['status'] == 'pending']),
#         'served': len([a for a in appointments if a['status'] == 'served']),
#         'missed': len([a for a in appointments if a['status'] == 'missed'])
#     }
    
#     rows = ""
#     for i, appt in enumerate(appointments):
#         rows += f'''
#         <tr>
#             <td>{appt['name']}</td>
#             <td>{appt['time']}</td>
#             <td><span class="status bg-{'blue' if appt['status']=='pending' else 'green' if appt['status']=='served' else 'red'}">{appt['status']}</span></td>
#             <td>
#                 <a href="/update/{i}/served" class="btn bg-green">Served</a>
#                 <a href="/update/{i}/missed" class="btn bg-red">Missed</a>
#                 <a href="/delete/{i}" style="color:red; margin-left:10px; font-size:10px;">Delete</a>
#             </td>
#         </tr>
#         '''
    
#     content = f'''
#         <h2 style="text-align:center;">👨‍⚕️ Admin Dashboard</h2>
#         <div style="display:flex; justify-content: space-around; margin-bottom:20px; text-align:center;">
#             <div class="status bg-blue">Pending: {stats['pending']}</div>
#             <div class="status bg-green">Served: {stats['served']}</div>
#             <div class="status bg-red">Missed: {stats['missed']}</div>
#         </div>
#         <table>
#             <tr><th>Mteja</th><th>Muda</th><th>Hali</th><th>Action</th></tr>
#             {rows if rows else '<tr><td colspan="4" style="text-align:center;">Hakuna miadi</td></tr>'}
#         </table>
#     '''
#     return render_template_string(HTML_LAYOUT, title="Admin", content=content)

# @app.route('/public', methods=['GET', 'POST'])
# def public_view():
#     # Public View: Mteja haoni majina, anaona tu kama muda umechukuliwa
#     if request.method == 'POST':
#         name = request.form.get('name')
#         time = request.form.get('time')
#         if any(a['time'] == time for a in appointments):
#             flash("Muda huo umeshachukuliwa!")
#         else:
#             appointments.append({'name': name, 'time': time, 'status': 'pending'})
#             appointments.sort(key=lambda x: x['time'])
#             return redirect(url_for('public_view'))

#     rows = ""
#     booked_times = [a['time'] for a in appointments]
#     for hour in BUSINESS_HOURS:
#         is_booked = hour in booked_times
#         status_text = '<span class="status bg-red">IMESHASHIKWA</span>' if is_booked else '<span class="status bg-green">WAZI</span>'
#         form = f'''
#             <form method="POST" style="display:inline;">
#                 <input type="hidden" name="time" value="{hour}">
#                 <input type="text" name="name" placeholder="Jina lako" required style="padding:2px;">
#                 <button type="submit" class="btn bg-blue">Weka Miadi</button>
#             </form>
#         ''' if not is_booked else ""
        
#         rows += f'<tr><td>{hour}</td><td>{status_text}</td><td>{form}</td></tr>'

#     content = f'''
#         <h2 style="text-align:center;">📅 Ratiba ya Leo (Mteja)</h2>
#         <p style="text-align:center; font-size:12px; color:gray;">Faragha: Huwezi kuona majina ya wagonjwa wengine.</p>
#         <table>
#             <tr><th>Saa</th><th>Hali</th><th>Weka Miadi</th></tr>
#             {rows}
#         </table>
#     '''
#     return render_template_string(HTML_LAYOUT, title="Public Booking", content=content)

# @app.route('/update/<int:id>/<status>')
# def update(id, status):
#     appointments[id]['status'] = status
#     return redirect(url_for('index'))

# @app.route('/delete/<int:id>')
# def delete(id):
#     appointments.pop(id)
#     return redirect(url_for('index'))

# if __name__ == '__main__':
#     port = int(os.environ.get("PORT", 5000))
#     app.run(host='0.0.0.0', port=port)from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import os
import json
from flask import Flask, render_template_string, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = "swiftqueue_pro_secure_v3"

# Sehemu ya Database (JSON)
DB_FILE = 'database.json'

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f)

BUSINESS_HOURS = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <title>SwiftQueue | {{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; text-align: center; }
        .nav { text-align: center; margin-bottom: 20px; }
        .nav a { margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background-color: #2c3e50; color: white; }
        .status-pill { padding: 5px 10px; border-radius: 20px; font-size: 12px; color: white; text-transform: uppercase; font-weight: bold; }
        .bg-blue { background-color: #3498db; } .bg-green { background-color: #2ecc71; } .bg-red { background-color: #e74c3c; }
        .btn { padding: 6px 12px; border-radius: 5px; text-decoration: none; color: white; font-size: 12px; display: inline-block; border: none; cursor: pointer; }
        input[type="text"], input[type="password"] { padding: 8px; border: 1px solid #ddd; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/public">📅 Weka Miadi</a> | 
        {% if session.get('admin') %}
            <a href="/admin">👨‍⚕️ Dashboard</a> | <a href="/logout">Logout</a>
        {% else %}
            <a href="/login">Admin Login</a>
        {% endif %}
    </div>
    <div class="container">
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            {% for message in messages %}
              <div style="color: red; margin-bottom: 10px; text-align: center;">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {{ content | safe }}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return redirect(url_for('public_view'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('username') == 'admin' and request.form.get('password') == '1234':
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash("Username au Password si sahihi!")
    content = '''
        <h2>Admin Login</h2>
        <form method="POST" style="text-align: center;">
            <input type="text" name="username" placeholder="Username" required><br><br>
            <input type="password" name="password" placeholder="Password" required><br><br>
            <button type="submit" class="btn bg-blue" style="width: 200px;">Ingia</button>
        </form>
    '''
    return render_template_string(HTML_LAYOUT, title="Login", content=content)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('public_view'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    appointments = load_data()
    stats = {
        'pending': len([a for a in appointments if a['status'] == 'pending']),
        'served': len([a for a in appointments if a['status'] == 'served']),
        'missed': len([a for a in appointments if a['status'] == 'missed'])
    }
    
    rows = ""
    for i, appt in enumerate(appointments):
        status_color = 'blue' if appt['status'] == 'pending' else 'green' if appt['status'] == 'served' else 'red'
        rows += f'''
        <tr>
            <td>{appt['name']}</td>
            <td>{appt['time']}</td>
            <td><span class="status-pill bg-{status_color}">{appt['status']}</span></td>
            <td>
                <a href="/update/{i}/served" class="btn bg-green">Served</a>
                <a href="/update/{i}/missed" class="btn bg-red">Missed</a>
                <a href="/delete/{i}" style="color:red; margin-left:10px; font-size:10px;">Delete</a>
            </td>
        </tr>'''
    
    content = f'''
        <h2>👨‍⚕️ Admin Dashboard</h2>
        <div style="display:flex; justify-content: space-around; margin-bottom:20px;">
            <div class="status-pill bg-blue">Pending: {stats['pending']}</div>
            <div class="status-pill bg-green">Served: {stats['served']}</div>
            <div class="status-pill bg-red">Missed: {stats['missed']}</div>
        </div>
        <table>
            <tr><th>Mteja</th><th>Muda</th><th>Hali</th><th>Action</th></tr>
            {rows if rows else '<tr><td colspan="4" style="text-align:center;">Hakuna miadi kwa sasa.</td></tr>'}
        </table>'''
    return render_template_string(HTML_LAYOUT, title="Admin", content=content)

@app.route('/public', methods=['GET', 'POST'])
def public_view():
    appointments = load_data()
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        if any(a['time'] == time for a in appointments):
            flash("Samahani! Muda huu tayari una miadi.")
        else:
            appointments.append({'name': name, 'time': time, 'status': 'pending'})
            appointments.sort(key=lambda x: x['time'])
            save_data(appointments)
            flash(f"Hongera {name}! Miadi yako ya saa {time} imepokelewa.")
            return redirect(url_for('public_view'))

    booked_times = [a['time'] for a in appointments]
    rows = ""
    for hour in BUSINESS_HOURS:
        is_booked = hour in booked_times
        status_text = '<span class="status-pill bg-red">IMESHASHIKWA</span>' if is_booked else '<span class="status-pill bg-green">WAZI</span>'
        form = f'''
            <form method="POST" style="display:inline;">
                <input type="hidden" name="time" value="{hour}">
                <input type="text" name="name" placeholder="Jina lako" required style="width:120px;">
                <button type="submit" class="btn bg-blue">Book</button>
            </form>''' if not is_booked else ""
        rows += f'<tr><td>{hour}</td><td>{status_text}</td><td>{form}</td></tr>'

    content = f'''
        <h2>📅 Ratiba ya Leo</h2>
        <table>
            <tr><th>Saa</th><th>Hali</th><th>Panga Miadi</th></tr>
            {rows}
        </table>'''
    return render_template_string(HTML_LAYOUT, title="Public", content=content)

@app.route('/update/<int:id>/<status>')
def update(id, status):
    if not session.get('admin'): return redirect(url_for('login'))
    appointments = load_data()
    if id < len(appointments):
        appointments[id]['status'] = status
        save_data(appointments)
    return redirect(url_for('admin_dashboard'))

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('admin'): return redirect(url_for('login'))
    appointments = load_data()
    if id < len(appointments):
        appointments.pop(id)
        save_data(appointments)
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)