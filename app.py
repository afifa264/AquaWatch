from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import init_db, get_db
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'aquawatch-local-demo-change-before-deployment')

init_db()

def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please sign in to submit or manage a report.', 'info')
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped

@app.context_processor
def inject_year():
    return {'current_year': datetime.now().year}

@app.route('/')
def home():
    db = get_db()
    stats = {
        'total': db.execute('SELECT COUNT(*) FROM reports').fetchone()[0],
        'resolved': db.execute("SELECT COUNT(*) FROM reports WHERE status='Resolved'").fetchone()[0],
        'progress': db.execute("SELECT COUNT(*) FROM reports WHERE status='In progress'").fetchone()[0],
        'critical': db.execute("SELECT COUNT(*) FROM reports WHERE priority='Critical' AND status!='Resolved'").fetchone()[0],
    }
    reports = db.execute('SELECT * FROM reports ORDER BY created_at DESC LIMIT 3').fetchall()
    return render_template('index.html', stats=stats, reports=reports)

@app.route('/reports')
def reports():
    db = get_db()
    q = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    status = request.args.get('status', '').strip()
    sql = 'SELECT * FROM reports WHERE 1=1'
    args = []
    if q:
        sql += ' AND (title LIKE ? OR location LIKE ? OR description LIKE ?)'
        args += [f'%{q}%'] * 3
    if category in ('Leakage', 'Water quality', 'Low pressure', 'Water logging'):
        sql += ' AND category=?'; args.append(category)
    if status in ('Open', 'In progress', 'Resolved'):
        sql += ' AND status=?'; args.append(status)
    sql += " ORDER BY CASE priority WHEN 'Critical' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END, created_at DESC"
    rows = db.execute(sql, args).fetchall()
    return render_template('reports.html', reports=rows, q=q, category=category, status=status)

@app.route('/report/new', methods=['GET', 'POST'])
@login_required
def new_report():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'Medium')
        if not all([title, category, location, description]):
            flash('Please complete all required fields.', 'error')
            return render_template('new_report.html')
        if category not in ('Leakage', 'Water quality', 'Low pressure', 'Water logging') or priority not in ('Low', 'Medium', 'High', 'Critical'):
            flash('Please choose a valid category and priority.', 'error')
            return render_template('new_report.html')
        db = get_db()
        db.execute('INSERT INTO reports (title, category, location, description, priority, status, user_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                   (title, category, location, description, priority, 'Open', session['user_id'], datetime.now().strftime('%Y-%m-%d %H:%M')))
        db.commit()
        flash('Your report has been submitted to the community board.', 'success')
        return redirect(url_for('reports'))
    return render_template('new_report.html')

@app.route('/reports/<int:report_id>')
def report_detail(report_id):
    report = get_db().execute('SELECT reports.*, users.username FROM reports LEFT JOIN users ON reports.user_id=users.id WHERE reports.id=?', (report_id,)).fetchone()
    if not report:
        flash('Report not found.', 'error'); return redirect(url_for('reports'))
    return render_template('report_detail.html', report=report)

@app.route('/reports/<int:report_id>/resolve', methods=['POST'])
@login_required
def resolve_report(report_id):
    db = get_db()
    report = db.execute('SELECT * FROM reports WHERE id=?', (report_id,)).fetchone()
    if not report:
        flash('Report not found.', 'error')
    elif report['user_id'] != session['user_id']:
        flash('You can only update your own reports in this demo.', 'error')
    else:
        db.execute("UPDATE reports SET status='Resolved' WHERE id=?", (report_id,)); db.commit()
        flash('Report marked as resolved.', 'success')
    return redirect(url_for('report_detail', report_id=report_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not username or not email or len(password) < 6:
            flash('Enter all details. Password must be at least 6 characters.', 'error')
            return render_template('register.html')
        db = get_db()
        try:
            cur = db.execute('INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)', (username, email, generate_password_hash(password)))
            db.commit(); session['user_id'] = cur.lastrowid; session['username'] = username
            flash('Welcome to AquaWatch!', 'success'); return redirect(url_for('home'))
        except Exception:
            flash('That email may already be registered. Try signing in.', 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = get_db().execute('SELECT * FROM users WHERE email=?', (email,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']; session['username'] = user['username']
            flash('You are signed in.', 'success'); return redirect(url_for('home'))
        flash('Email or password is incorrect.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear(); flash('You have signed out.', 'info'); return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
