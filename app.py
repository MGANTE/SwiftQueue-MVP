# from flask import Flask, render_template_string, request, redirect, url_for, flash
# import os

# app = Flask(__name__)
# app.secret_key = "swiftqueue_pro_key"

# # Database ya muda
# appointments = []

# HTML_TEMPLATE = '''
# <!DOCTYPE html>
# <html>
# <head>
#     <title>SwiftQueue | Small Provider MVP</title>
#     <meta name="viewport" content="width=device-width, initial-scale=1">
#     <style>
#         body { font-family: 'Arial', sans-serif; background-color: #f0f2f5; padding: 20px; }
#         .container { max-width: 900px; margin: auto; background: white; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
#         .header { text-align: center; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
#         .stats-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 20px; text-align: center; }
#         .stat-card { padding: 15px; border-radius: 8px; color: white; font-weight: bold; }
#         .bg-blue { background-color: #007bff; } .bg-green { background-color: #28a745; } .bg-red { background-color: #dc3545; }
        
#         form { display: grid; grid-template-columns: 1fr 1fr auto; gap: 10px; margin-bottom: 30px; background: #f9f9f9; padding: 15px; border-radius: 8px; }
#         input, select { padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
#         button.add-btn { background: #2c3e50; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        
#         table { width: 100%; border-collapse: collapse; }
#         th, td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
#         .status-pill { padding: 5px 10px; border-radius: 20px; font-size: 12px; color: white; text-transform: uppercase; }
#         .btn-sm { padding: 5px; font-size: 11px; text-decoration: none; border-radius: 3px; margin-right: 2px; }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>🚀 SwiftQueue MVP</h1>
#             <p>Niche: Small-scale Service Providers</p>
#         </div>

#         <div class="stats-grid">
#             <div class="stat-card bg-blue">Pending: {{ stats.pending }}</div>
#             <div class="stat-card bg-green">Served: {{ stats.served }}</div>
#             <div class="stat-card bg-red">Missed: {{ stats.missed }}</div>
#         </div>

#         <form method="POST" action="/add">
#             <input type="text" name="name" placeholder="Jina la Mteja" required>
#             <input type="time" name="time" required>
#             <button type="submit" class="add-btn">Panga Miadi</button>
#         </form>

#         {% with messages = get_flashed_messages() %}{% if messages %}
#             {% for msg in messages %}<p style="color: red; text-align: center;">{{ msg }}</p>{% endfor %}
#         {% endif %}{% endwith %}

#         <table>
#             <thead>
#                 <tr>
#                     <th>Mteja</th>
#                     <th>Muda</th>
#                     <th>Hali (Status)</th>
#                     <th>Action</th>
#                 </tr>
#             </thead>
#             <tbody>
#                 {% for appt in appointments %}
#                 <tr>
#                     <td>{{ appt.name }}</td>
#                     <td>{{ appt.time }}</td>
#                     <td><span class="status-pill {% if appt.status=='pending' %}bg-blue{% elif appt.status=='served' %}bg-green{% else %}bg-red{% endif %}">{{ appt.status }}</span></td>
#                     <td>
#                         <a href="/update/{{ loop.index0 }}/served" class="btn-sm bg-green" style="color:white">Served</a>
#                         <a href="/update/{{ loop.index0 }}/missed" class="btn-sm bg-red" style="color:white">Missed</a>
#                         <a href="/delete/{{ loop.index0 }}" style="color:grey; font-size:10px">Delete</a>
#                     </td>
#                 </tr>
#                 {% endfor %}
#             </tbody>
#         </table>
#     </div>
# </body>
# </html>
# '''

# @app.route('/')
# def index():
#     stats = {
#         'pending': len([a for a in appointments if a['status'] == 'pending']),
#         'served': len([a for a in appointments if a['status'] == 'served']),
#         'missed': len([a for a in appointments if a['status'] == 'missed'])
#     }
#     return render_template_string(HTML_TEMPLATE, appointments=appointments, stats=stats)

# @app.route('/add', methods=['POST'])
# def add():
#     name, time = request.form.get('name'), request.form.get('time')
#     # Prevent Double Booking (Problem iii)
#     if any(a['time'] == time for a in appointments):
#         flash(f"Error: Muda wa {time} umeshachukuliwa!")
#     else:
#         appointments.append({'name': name, 'time': time, 'status': 'pending'})
#         appointments.sort(key=lambda x: x['time'])
#     return redirect(url_for('index'))

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
#     app.run(host='0.0.0.0', port=port)
from flask import Flask, render_template_string, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "swiftqueue_pro_v2"

appointments = []
# Orodha ya masaa ya kazi (Business Hours)
BUSINESS_HOURS = ["08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00"]

HTML_LAYOUT = '''
<!DOCTYPE html>
<html>
<head>
    <title>SwiftQueue | {{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .nav { margin-bottom: 20px; text-align: center; }
        .nav a { margin: 0 10px; text-decoration: none; color: #3498db; font-weight: bold; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; border-bottom: 1px solid #eee; text-align: left; }
        .status { padding: 4px 8px; border-radius: 4px; color: white; font-size: 12px; }
        .bg-blue { background: #3498db; } .bg-green { background: #2ecc71; } .bg-red { background: #e74c3c; } .bg-gray { background: #95a5a6; }
        .btn { padding: 5px 10px; border-radius: 4px; text-decoration: none; color: white; font-size: 12px; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/">Dashboard (Admin)</a> | <a href="/public">Book Now (Public)</a>
    </div>
    <div class="container">
        {{ content | safe }}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Admin View: Anaona majina yote na anaweza ku-manage
    stats = {
        'pending': len([a for a in appointments if a['status'] == 'pending']),
        'served': len([a for a in appointments if a['status'] == 'served']),
        'missed': len([a for a in appointments if a['status'] == 'missed'])
    }
    
    rows = ""
    for i, appt in enumerate(appointments):
        rows += f'''
        <tr>
            <td>{appt['name']}</td>
            <td>{appt['time']}</td>
            <td><span class="status bg-{'blue' if appt['status']=='pending' else 'green' if appt['status']=='served' else 'red'}">{appt['status']}</span></td>
            <td>
                <a href="/update/{i}/served" class="btn bg-green">Served</a>
                <a href="/update/{i}/missed" class="btn bg-red">Missed</a>
                <a href="/delete/{i}" style="color:red; margin-left:10px; font-size:10px;">Delete</a>
            </td>
        </tr>
        '''
    
    content = f'''
        <h2 style="text-align:center;">👨‍⚕️ Admin Dashboard</h2>
        <div style="display:flex; justify-content: space-around; margin-bottom:20px; text-align:center;">
            <div class="status bg-blue">Pending: {stats['pending']}</div>
            <div class="status bg-green">Served: {stats['served']}</div>
            <div class="status bg-red">Missed: {stats['missed']}</div>
        </div>
        <table>
            <tr><th>Mteja</th><th>Muda</th><th>Hali</th><th>Action</th></tr>
            {rows if rows else '<tr><td colspan="4" style="text-align:center;">Hakuna miadi</td></tr>'}
        </table>
    '''
    return render_template_string(HTML_LAYOUT, title="Admin", content=content)

@app.route('/public', methods=['GET', 'POST'])
def public_view():
    # Public View: Mteja haoni majina, anaona tu kama muda umechukuliwa
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        if any(a['time'] == time for a in appointments):
            flash("Muda huo umeshachukuliwa!")
        else:
            appointments.append({'name': name, 'time': time, 'status': 'pending'})
            appointments.sort(key=lambda x: x['time'])
            return redirect(url_for('public_view'))

    rows = ""
    booked_times = [a['time'] for a in appointments]
    for hour in BUSINESS_HOURS:
        is_booked = hour in booked_times
        status_text = '<span class="status bg-red">IMESHASHIKWA</span>' if is_booked else '<span class="status bg-green">WAZI</span>'
        form = f'''
            <form method="POST" style="display:inline;">
                <input type="hidden" name="time" value="{hour}">
                <input type="text" name="name" placeholder="Jina lako" required style="padding:2px;">
                <button type="submit" class="btn bg-blue">Weka Miadi</button>
            </form>
        ''' if not is_booked else ""
        
        rows += f'<tr><td>{hour}</td><td>{status_text}</td><td>{form}</td></tr>'

    content = f'''
        <h2 style="text-align:center;">📅 Ratiba ya Leo (Mteja)</h2>
        <p style="text-align:center; font-size:12px; color:gray;">Faragha: Huwezi kuona majina ya wagonjwa wengine.</p>
        <table>
            <tr><th>Saa</th><th>Hali</th><th>Weka Miadi</th></tr>
            {rows}
        </table>
    '''
    return render_template_string(HTML_LAYOUT, title="Public Booking", content=content)

@app.route('/update/<int:id>/<status>')
def update(id, status):
    appointments[id]['status'] = status
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    appointments.pop(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)