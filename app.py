from flask import Flask, render_template_string, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = "swiftqueue_secret_key" # Inahitajika kwa ajili ya flash messages

# Database ya muda (Inafuta data ukizima server, inatosha kwa MVP)
appointments = []

# HTML Template yenye CSS (Inakaa ndani ya app.py kwa urahisi wa ku-push haraka)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>SwiftQueue | Smart Booking</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        h2 { color: #2c3e50; text-align: center; }
        .form-group { margin-bottom: 15px; }
        input[type="text"], input[type="time"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { background-color: #27ae60; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; }
        button:hover { background-color: #219150; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; border-bottom: 1px solid #ddd; text-align: left; }
        th { background-color: #2c3e50; color: white; }
        .alert { padding: 15px; margin-bottom: 20px; border: 1px solid transparent; border-radius: 4px; color: #721c24; background-color: #f8d7da; border-color: #f5c6cb; }
        .success { color: #155724; background-color: #d4edda; border-color: #c3e6cb; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🚀 SwiftQueue Dashboard</h2>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class="alert {{ category }}">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}

        <form method="POST" action="/add">
            <div class="form-group">
                <label>Jina la Mteja:</label>
                <input type="text" name="name" placeholder="Andika jina kamili" required>
            </div>
            <div class="form-group">
                <label>Muda wa Miadi:</label>
                <input type="time" name="time" required>
            </div>
            <button type="submit">Weka Miadi Sasa</button>
        </form>

        <hr>

        <h3>Orodha ya Miadi ya Leo</h3>
        <table>
            <thead>
                <tr>
                    <th>Jina</th>
                    <th>Muda</th>
                    <th>Hali (Status)</th>
                </tr>
            </thead>
            <tbody>
                {% for appt in appointments %}
                <tr>
                    <td>{{ appt.name }}</td>
                    <td>{{ appt.time }}</td>
                    <td><span style="color: orange;">● Pending</span></td>
                </tr>
                {% else %}
                <tr>
                    <td colspan="3" style="text-align:center;">Hakuna miadi iliyopangwa bado.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, appointments=appointments)

@app.route('/add', methods=['POST'])
def add_appointment():
    name = request.form.get('name')
    time = request.form.get('time')
    
    # LOGIC: Kuzuia Double Booking
    for appt in appointments:
        if appt['time'] == time:
            flash(f"Samahani! Muda wa {time} umeshachukuliwa. Chagua muda mwingine.", "alert")
            return redirect(url_for('index'))
    
    # Kama muda uko wazi
    appointments.append({'name': name, 'time': time})
    appointments.sort(key=lambda x: x['time']) # Kupanga miadi kwa mfuatano wa muda
    flash(f"Mteja {name} amepangiwa saa {time} vizuri!", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)