from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Hii ni list ya kuhifadhi miadi (Temporary Database kwa ajili ya MVP)
appointments = []

@app.route('/')
def index():
    return "<h1>SwiftQueue Dashboard</h1><p>Tumia /add kuongeza mteja.</p>"

@app.route('/add', methods=['GET', 'POST'])
def add_appointment():
    if request.method == 'POST':
        name = request.form.get('name')
        time = request.form.get('time')
        
        # LOGIC: Kuzuia Double Booking
        for appt in appointments:
            if appt['time'] == time:
                return f"<h2>Samahani! Muda wa {time} umeshachukuliwa na mteja mwingine.</h2>"
        
        # Kama muda uko wazi, ongeza mteja
        appointments.append({'name': name, 'time': time, 'status': 'Pending'})
        return f"<h2>Mteja {name} amepangiwa saa {time} vizuri!</h2>"
    
    # Fomu rahisi ya kuingiza data
    return '''
        <form method="POST">
            Jina: <input type="text" name="name"><br>
            Saa (mfano 10:00): <input type="text" name="time"><br>
            <input type="submit" value="Weka Miadi">
        </form>
    '''

import os


if __name__ == '__main__':
    # Hii inachukua Port inayotolewa na Render, la sivyo inatumia 5000
    port = int(os.environ.get("PORT", 5000))
    # Ni lazima host iwe '0.0.0.0' ili ionekane nje ya server
    app.run(host='0.0.0.0', port=port)