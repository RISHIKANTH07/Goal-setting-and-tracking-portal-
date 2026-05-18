from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret"

# Dummy users
users = {
    "emp": "employee",
    "mgr": "manager"
}

goals = []

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            session['user'] = username
            session['role'] = users[username]

            if users[username] == "employee":
                return redirect('/employee')
            else:
                return redirect('/manager')
    return render_template('login.html')


# Employee Dashboard
@app.route('/employee')
def employee():
    return render_template('employee.html', goals=goals)


# Add Goal
@app.route('/add', methods=['GET', 'POST'])
def add_goal():
    if request.method == 'POST':
        title = request.form['title']
        target = request.form['target']
        weight = int(request.form['weight'])

        # RULES
        if len(goals) >= 8:
            return "Max 8 goals allowed"

        if weight < 10:
            return "Min weight is 10%"

        total_weight = sum(g['weight'] for g in goals)

        if total_weight + weight > 100:
            return "Total weight exceeds 100%"

        goals.append({
            "title": title,
            "target": target,
            "weight": weight,
            "status": "Not Started",
            "approved": False
        })

        return redirect('/employee')

    return render_template('add_goal.html')


# Manager Dashboard
@app.route('/manager')
def manager():
    return render_template('manager.html', goals=goals)


# Approve Goal
@app.route('/approve/<int:id>')
def approve(id):
    goals[id]['approved'] = True
    return redirect('/manager')


# Update Status
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    goals[id]['status'] = request.form['status']
    return redirect('/employee')


app.run(debug=True) 