import os
import fitz  
import pyaudio
import textwrap
import soundfile
import tkinter as tk
from fpdf import FPDF
from gtts import gTTS
from pathlib import Path
from tkinter import filedialog
import speech_recognition as sr


def convert_pdf_to_audio(pdf_path, language='en', output_file='output.mp3'):
    try:
        text = ""
        with fitz.open(pdf_path) as pdf:
            for page in pdf:
                text += page.get_text()

        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_file)
        print(f"Audio file saved as: {output_file}")

    except FileNotFoundError:
        print(f"Error: File not found at path {pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def convert_mp3_to_pdf(mp3_file_path):
    wav_file_path = "Output.wav"

    # Convert MP3 to WAV
    convert_mp3_to_wav(mp3_file_path, wav_file_path)

    # Convert WAV to PDF
    convert_wav_to_pdf(wav_file_path)

    print("PDF file saved as: Output.pdf")

    # Delete the WAV file
    os.remove(wav_file_path)

def convert_mp3_to_wav(mp3_file, wav_file):
    

    # Open the MP3 file
    with soundfile.SoundFile(mp3_file, 'rb') as mp3:
        # Read the MP3 file
        mp3_data = mp3.read(dtype='int16')
        
        # Save the data as WAV file
        soundfile.write(wav_file, mp3_data, samplerate=mp3.samplerate)

def convert_wav_to_pdf(wav_file):
    recognizer = sr.Recognizer()

    # Open the WAV file
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        text = recognizer.recognize_google(audio_data)
    
    # Create PDF
    a4_width_mm = 210
    pt_to_mm = 0.5
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 5 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.set_margins(left=10, top=10, right=10)
    pdf.add_page()
    pdf.set_font(family='Arial', size=14)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1, align='L')

    pdf.output("Output.pdf", 'F')

def browse_pdf():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        convert_pdf_to_audio(pdf_path)

def browse_audio():
    audio_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
    if audio_path:
        convert_mp3_to_pdf(audio_path)

# Create the main window
window = tk.Tk()
window.title("PDF to Audio and Audio to PDF converter")
window.geometry('800x600')
window.config(bg='black')

# Create a frame to hold the buttons and center it
frame = tk.Frame(window, bg='black')
frame.place(relx=0.5, rely=0.5, anchor='center')

# Create buttons
pdf_button = tk.Button(frame, text="Convert PDF to Audio", command=browse_pdf, height=5, width=30)
pdf_button.pack(pady=10)

audio_button = tk.Button(frame, text="Convert Audio to pdf", command=browse_audio, height=5, width=30)
audio_button.pack(pady=10)

# Run the Tkinter event loop
window.mainloop()
