import os
import json
from flask import Flask, render_template_string, request, redirect, url_for, flash, session

app = Flask(__name__)
app.secret_key = "swiftqueue_pro_secure_v3"

# Sehemu ya Database (JSON)
DB_FILE = 'database.json'
WAITLIST_FILE = 'waitlist.json' # Faili jipya la kukusanya contacts

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
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
        input[type="text"], input[type="password"], input[type="email"] { padding: 8px; border: 1px solid #ddd; border-radius: 5px; margin-bottom: 10px; }
        .benefit-box { background: #e8f4f8; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 5px solid #3498db; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">🏠 Home</a> |
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
              <div style="color: #2ecc71; font-weight:bold; margin-bottom: 10px; text-align: center;">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {{ content | safe }}
    </div>
</body>
</html>
'''

# 1. LANDING PAGE (Hii ndo Route mpya aliyotaka mwalimu)
@app.route('/')
def home():
    content = '''
        <div style="text-align: center;">
            <h1>SwiftQueue </h1>
            <p style="font-size: 1.2em; color: #555;">"Muda wako ni dhahabu. Panga miadi, okoa muda!"</p>
            
            <div style="text-align: left; margin: 30px 0;">
                <h3>Why SwiftQueue? </h3>
                <div class="benefit-box">
                    <strong>✅ Hakuna Kuingiliana:</strong> Mfumo unakataa miadi miwili kwa saa moja.
                </div>
                <div class="benefit-box">
                    <strong>✅ Muda ni Mali:</strong> Wateja wanajua saa yao kamili ya kuhudumiwa.
                </div>
                <div class="benefit-box">
                    <strong>✅ Kidijitali Zaidi:</strong> Sahau madaftari ya kizamani yanayoweza kupotea.
                </div>
            </div>

            <div style="background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-top: 20px;">
                <h3>Jiunge na Waitlist 📝</h3>
                <p>Tuachie mawasiliano yako ili upate taarifa mfumo kamili utakapozinduliwa!</p>
                <form method="POST" action="/collect-info">
                    <input type="text" name="name" placeholder="Jina lako" required style="width: 80%;">
                    <input type="text" name="contact" placeholder="Simu au Email" required style="width: 80%;">
                    <br>
                    <button type="submit" class="btn bg-green" style="font-size: 16px; padding: 10px 20px;">Nijulishe!</button>
                </form>
            </div>

            <div style="text-align: left; margin-top: 30px;">
                <h3>Vitu vitakavyoongezeka (Product Roadmap):</h3>
                <ul>
                    <li>SMS za kukumbusha miadi (Automatic).</li>
                    <li>Malipo ya awali kwa M-Pesa/Tigo Pesa.</li>
                    <li>Ripoti za mapato ya mwezi.</li>
                </ul>
            </div>
            <br>
            <a href="/public" class="btn bg-blue" style="font-size: 1.1em;">Jaribu Sasa (Demo) &rarr;</a>
        </div>
    '''
    return render_template_string(HTML_LAYOUT, title="Karibu", content=content)

# 2. COLLECT INFO ROUTE (Kukusanya data za wateja)
@app.route('/collect-info', methods=['POST'])
def collect_info():
    name = request.form.get('name')
    contact = request.form.get('contact')
    waitlist = load_data(WAITLIST_FILE)
    waitlist.append({'name': name, 'contact': contact})
    save_data(WAITLIST_FILE, waitlist)
    flash(f"Asante {name}! Tumekuweka kwenye orodha yetu.")
    return redirect(url_for('home'))

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
    return redirect(url_for('home'))

@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('login'))
    
    appointments = load_data(DB_FILE)
    waitlist = load_data(WAITLIST_FILE) # Tunapakua na Waitlist hapa
    
    # Sehemu ya Appointments
    rows = ""
    for i, appt in enumerate(appointments):
        status_color = 'blue' if appt['status'] == 'pending' else 'green' if appt['status'] == 'served' else 'red'
        rows += f'<tr><td>{appt["name"]}</td><td>{appt["time"]}</td><td><span class="status-pill bg-{status_color}">{appt["status"]}</span></td><td><a href="/update/{i}/served" class="btn bg-green">Served</a> <a href="/delete/{i}" style="color:red; font-size:10px;">Delete</a></td></tr>'
    
    # Sehemu ya Waitlist (Landing Page Leads)
    wait_rows = ""
    for w in waitlist:
        wait_rows += f'<tr><td>{w["name"]}</td><td>{w["contact"]}</td></tr>'

    content = f'''
        <h2>👨‍⚕️ Admin Dashboard</h2>
        <h3>Miadi ya Leo</h3>
        <table><tr><th>Mteja</th><th>Muda</th><th>Hali</th><th>Action</th></tr>{rows}</table>
        
        <h2 style="margin-top:40px;">📝 Waitlist (Interested People)</h2>
        <table><tr><th>Jina</th><th>Mawasiliano</th></tr>{wait_rows if wait_rows else "<tr><td colspan='2'>Hamna mtu bado</td></tr>"}</table>
    '''
    return render_template_string(HTML_LAYOUT, title="Admin", content=content)

@app.route('/public', methods=['GET', 'POST'])
def public_view():
    appointments = load_data(DB_FILE)
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        if any(a['time'] == time for a in appointments):
            flash("Samahani! Muda huu tayari una miadi.")
        else:
            appointments.append({'name': name, 'time': time, 'status': 'pending'})
            appointments.sort(key=lambda x: x['time'])
            save_data(DB_FILE, appointments)
            flash(f"Hongera {name}! Miadi imepokelewa.")
            return redirect(url_for('public_view'))

    booked_times = [a['time'] for a in appointments]
    rows = ""
    for hour in BUSINESS_HOURS:
        is_booked = hour in booked_times
        status_text = '<span class="status-pill bg-red">IMESHASHIKWA</span>' if is_booked else '<span class="status-pill bg-green">WAZI</span>'
        form = f'''<form method="POST" style="display:inline;"><input type="hidden" name="time" value="{hour}"><input type="text" name="name" placeholder="Jina" required style="width:80px;"><button type="submit" class="btn bg-blue">Book</button></form>''' if not is_booked else ""
        rows += f'<tr><td>{hour}</td><td>{status_text}</td><td>{form}</td></tr>'

    content = f'''<h2>📅 Ratiba ya Leo</h2><table><tr><th>Saa</th><th>Hali</th><th>Booking</th></tr>{rows}</table>'''
    return render_template_string(HTML_LAYOUT, title="Public", content=content)

@app.route('/update/<int:id>/<status>')
def update(id, status):
    if not session.get('admin'): return redirect(url_for('login'))
    appointments = load_data(DB_FILE)
    if id < len(appointments):
        appointments[id]['status'] = status
        save_data(DB_FILE, appointments)
    return redirect(url_for('admin_dashboard'))

@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('admin'): return redirect(url_for('login'))
    appointments = load_data(DB_FILE)
    if id < len(appointments):
        appointments.pop(id)
        save_data(DB_FILE, appointments)
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)