from flask import Blueprint, render_template, request, redirect, url_for, send_file, jsonify, render_template_string
from models import Note
from helpers import create_pdf_report
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import io
from io import BytesIO
import base64
from xml_parser import parse_xml_file
import os
import jinja2
from scipy.signal import find_peaks, butter, filtfilt
import json
import numpy as np 
bp = Blueprint('main', __name__)


@bp.route('/')
def hello():
    all_notes = Note.get_all_notes()
    notes = all_notes[:5]
    return render_template('firstpage.html', notes=notes, all_notes=all_notes)


@bp.route('/dashboard/all_json')
def dashboard_all_json():
    try:
        all_notes = Note.query.all()
        notes_list = [note.to_dict() for note in all_notes]
        return jsonify(notes_list)
    except Exception as e:
        app.logger.error(f"Error in /dashboard/all_json: {notes_list}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/dashboard/first_five_json')
def dashboard_first_five_json():
    try:
        first_five_notes = Note.query.limit(5).all()
        notes_list = [note.to_dict() for note in first_five_notes]
        return jsonify(notes_list)
    except Exception as e:
        app.logger.error(f"Error in /dashboard/first_five_json: {e}")
        return jsonify({"error": "Internal server error"}), 500

@bp.route('/search_notes', methods=['POST'])
def search_notes():
    data = request.json
    print(data) 
    last_name = data.get('lastName')
    first_name = data.get('firstName')
    birth_date = data.get('birthDate')
    upload_date = data.get('uploadDate')
    query = Note.query
    if last_name:
        query = query.filter(Note.last_name.contains(last_name))
    if first_name:
        query = query.filter(Note.first_name.contains(first_name))
    if birth_date:
        query = query.filter(Note.date_of_birth == datetime.strptime(birth_date, '%Y-%m-%d').date())
    if upload_date:
        query = query.filter(Note.date_of_upload == datetime.strptime(upload_date, '%Y-%m-%d').date())
    results = query.all()
    notes = [note.to_dict() for note in results]
    return jsonify(notes)

@bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "failure", "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "failure", "message": "No selected file"}), 400
    if file and file.filename.endswith('.xml'):
        file.save(os.path.join("./", file.filename))
        data = parse_xml_file("./"+file.filename)
        return jsonify({"status": "success", "message": "File received", "filename": file.filename}), 200
    else:
        return jsonify({"status": "failure", "message": "Invalid file type"}), 400


@bp.route('/detail/<int:note_id>')
def detail_view(note_id):
    note = Note.get_note_by_id(note_id)
    graph_data = note.data
    graph_urls = []
    for title, data_str in graph_data.items():
        fig, ax = plt.subplots()
        fig.set_size_inches(20, 5)
        data = [float(val) for val in data_str.split(',') if val.strip()]
        ax.plot(data, label=title)
        ax.legend()
        img = BytesIO()
        plt.savefig(img, format='png',bbox_inches='tight')
        img.seek(0)
        plt.close()
        graph_url = base64.b64encode(img.getvalue()).decode()
        graph_urls.append(graph_url)
    if note:
        return render_template('detail.html', note=note, graph_urls=graph_urls)
    else:
        return "Запись не найдена", 404

def bandpass_filter(data, lowcut, highcut, fs, order=1):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

@bp.route('/analyze_plot', methods=['POST'])
def plot():

    fs = 500
    note_id = request.json.get('note_id')
    note = Note.get_note_by_id(note_id)
    
    data = [float(val) for val in note.data.get('II').split(',') if val.strip()]
    np_data = np.array(data)
    
    ecg_lead = (np_data - np.min(np_data)) / (np.max(np_data) - np.min(np_data))
    
    filtered_ecg = bandpass_filter(ecg_lead, 0.5, 45, fs, order=1)
    
    peaks, _ = find_peaks(filtered_ecg, distance=fs/2.5, height=np.mean(filtered_ecg) + 0.5 * np.std(filtered_ecg))
    
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(filtered_ecg, label='ECG')
    ax.plot(peaks, filtered_ecg[peaks], 'ro', label='R-peaks')
    ax.legend()
    
    canvas = FigureCanvas(fig)
    buf = io.BytesIO()
    canvas.print_png(buf)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    r_peak_intervals = np.diff(peaks) / fs
    heart_rate = 60 / np.mean(r_peak_intervals)
    
    return jsonify({'heart_rate': round(heart_rate),'plot_url': plot_url})

@bp.route('/download_report/<int:note_id>')
def download_report(note_id):
    note = Note.get_note_by_id(note_id)
    if not note:
        return "Запись не найдена", 404
    buffer = create_pdf_report(note)
    return send_file(buffer, as_attachment=True, download_name='report.pdf', mimetype='application/pdf')


