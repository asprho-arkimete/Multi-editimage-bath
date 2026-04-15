import os
import tkinter as tk
from tkinter import ttk
from turtle import width
from PIL import Image, ImageTk
from sympy.series import order

os.makedirs("Lora", exist_ok=True)
os.makedirs("output_image", exist_ok=True)
os.makedirs("image_referenze", exist_ok=True)

window = tk.Tk()
window.title("Select Action")
window.geometry("1280x1028")
window.resizable(False, False)
window.config(bg='gray')

# Canvas a sinistra
frame1 = tk.Frame(window, bg='gray')
frame1.grid(row=0, column=0)
frame = tk.Canvas(frame1, width=512, height=512, bg='red')
frame.grid(row=0, column=0)

# Listbox a destra
frame2 = tk.Frame(window, bg='gray')
frame2.grid(row=0, column=1, sticky="ns")
lista_azioni = tk.Listbox(frame2, width=50, height=35, exportselection=False)
lista_azioni.grid(row=0, column=0, pady=10, padx=5)

frame_button= tk.Frame(window,bg='Gray')
frame_button.grid(row=0,column=2)

def f_su():
    global elementi_selezionati
    selezione = lista_azioni.curselection()
    if not selezione:
        return
    idx = selezione[0]
    if idx == 0:
        return  # già in cima
    # scambia con l'elemento precedente
    elementi_selezionati[idx], elementi_selezionati[idx - 1] = elementi_selezionati[idx - 1], elementi_selezionati[idx]
    aggiorna_listbox()
    # mantieni la selezione sull'elemento spostato
    lista_azioni.selection_set(idx - 1)
    lista_azioni.activate(idx - 1)

def f_giu():
    global elementi_selezionati
    selezione = lista_azioni.curselection()
    if not selezione:
        return
    idx = selezione[0]
    if idx == len(elementi_selezionati) - 1:
        return  # già in fondo
    # scambia con l'elemento successivo
    elementi_selezionati[idx], elementi_selezionati[idx + 1] = elementi_selezionati[idx + 1], elementi_selezionati[idx]
    aggiorna_listbox()
    # mantieni la selezione sull'elemento spostato
    lista_azioni.selection_set(idx + 1)
    lista_azioni.activate(idx + 1)

def f_elimina():
    global elementi_selezionati
    selezione = lista_azioni.curselection()
    if not selezione:
        return
    idx = selezione[0]
    azione = elementi_selezionati[idx]['azione']
    if messagebox.askyesno("Elimina", f"Eliminare '{azione}' dalla lista?"):
        elementi_selezionati.pop(idx)
        aggiorna_listbox()

su = tk.Button(frame_button, text='⬆', command=f_su)
su.grid(row=0, column=0, pady=5, padx=2)
elimina_elemento = tk.Button(frame_button, text="🗑", command=f_elimina)
elimina_elemento.grid(row=1, column=0, pady=2, padx=2)
giu = tk.Button(frame_button, text="⬇", command=f_giu)
giu.grid(row=2, column=0, pady=2, padx=2)

import time
import shutil
from datetime import datetime, timedelta

frame_video = tk.Frame(window, bg='gray')
frame_video.grid(row=0, column=3)

lista_video = tk.Listbox(frame_video, width=30, height=25)
lista_video.grid(row=0, column=0)

import re
# ✅ Funzione per l'ordinamento naturale (v1, v2, ... v10, v11)
def natural_sort_key(s):
    # Trova tutti i numeri nella stringa e li converte in interi per il confronto
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

def carica_video():
    path_video = "./videos"
    if os.path.exists(path_video):
        # 1. Recuperiamo la lista dei file
        files = [v for v in os.listdir(path_video) if v.endswith('.mp4')]
        
        # 2. Ordiniamo la lista con la nostra chiave speciale
        files.sort(key=natural_sort_key)
        
        # 3. Inseriamo i file ordinati nella Listbox
        for v in files:
            lista_video.insert(tk.END, v)

carica_video()

# Nuovo frame bottoni affiancato alla listbox video
frame_button_video = tk.Frame(frame_video, bg='gray')
frame_button_video.grid(row=0, column=1)

def f_su_video():
    sel = lista_video.curselection()
    if sel and sel[0] > 0:
        i = sel[0]
        testo = lista_video.get(i)
        lista_video.delete(i)
        lista_video.insert(i - 1, testo)
        lista_video.select_set(i - 1)

def f_elimina_video():
    sel = lista_video.curselection()
    if sel:
        lista_video.delete(sel[0])

def f_giu_video():
    sel = lista_video.curselection()
    if sel and sel[0] < lista_video.size() - 1:
        i = sel[0]
        testo = lista_video.get(i)
        lista_video.delete(i)
        lista_video.insert(i + 1, testo)
        lista_video.select_set(i + 1)

def f_save_lista():
    global clip_corrente, photo_corrente
    path_video = "./videos"

    # --- SBLOCCO DEL FILE ---
    if clip_corrente is not None:
        try:
            clip_corrente.close() # Chiude il file reader di MoviePy
            del clip_corrente     # Rimuove il riferimento
            clip_corrente = None  # Reset variabile globale
        except:
            pass

    # Pulisci anche la memoria della canvas
    photo_corrente = None 
    frame.delete("all")
    lista_video.selection_clear(0, tk.END)

    # --- ORA PUOI RINOMINARE ---
    video_correnti = lista_video.get(0, tk.END)
    if not video_correnti: return

    try:
        temp_names = []
        for i, nome_file in enumerate(video_correnti, start=1):
            vecchio_path = os.path.normpath(os.path.join(path_video, nome_file))
            nuovo_path_temp = os.path.normpath(os.path.join(path_video, f"temp_{i}.mp4"))
            
            if os.path.exists(vecchio_path):
                os.rename(vecchio_path, nuovo_path_temp)
                temp_names.append(f"temp_{i}.mp4")
        
        for i, temp_file in enumerate(temp_names, start=1):
            path_temp = os.path.join(path_video, temp_file)
            path_finale = os.path.join(path_video, f"v{i}.mp4")
            os.rename(path_temp, path_finale)

        # Aggiorna Listbox
        lista_video.delete(0, tk.END)
        for v in sorted(os.listdir(path_video), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 0):
            if v.endswith(".mp4"):
                lista_video.insert(tk.END, v)

        print("✅ File rinominati e sbloccati!")
    except OSError as e:
        print(f"❌ Errore: Il file è ancora bloccato. Assicurati di aver chiuso la clip. {e}")


su_video = tk.Button(frame_button_video, text='⬆', command=f_su_video)
su_video.grid(row=0, column=0, pady=5, padx=2)
elimina_video = tk.Button(frame_button_video, text="🗑", command=f_elimina_video)
elimina_video.grid(row=1, column=0, pady=2, padx=2)
giu_video = tk.Button(frame_button_video, text="⬇", command=f_giu_video)
giu_video.grid(row=2, column=0, pady=2, padx=2)
# Sostituisci la riga del bottone con questa:
salva_ordine_lista = tk.Button(
    frame_button_video, 
    text='💾',             # Icona del disco
    font=("Arial", 12),    # Opzionale: per ingrandire l'icona
    command=f_save_lista
)
salva_ordine_lista.grid(row=3, column=0, pady=2, padx=2)



def rinomina_se_doppio(path_video, nome_file):
    """Se il file esiste già, rinomina: v.mp4 → v1.mp4 → v2.mp4 ecc."""
    dest = os.path.join(path_video, nome_file)
    if not os.path.exists(dest):
        return nome_file

    nome, ext = os.path.splitext(nome_file)

    # controlla se finisce già con un numero: "v1" → "v2"
    match = re.search(r'^(.*?)(\d+)$', nome)
    if match:
        base = match.group(1)
        indice = int(match.group(2)) + 1
    else:
        # "v" → "v1"
        base = nome
        indice = 1

    while True:
        nuovo_nome = f"{base}{indice}{ext}"
        if not os.path.exists(os.path.join(path_video, nuovo_nome)):
            return nuovo_nome
        indice += 1


def f_copy():
    path_video = "./videos"
    path_download = r"C:\Users\User\Downloads"
    os.makedirs(path_video, exist_ok=True)
    ora_corrente = datetime.now()
    min_ora = ora_corrente - timedelta(hours=12)
    max_ora = ora_corrente + timedelta(hours=12)

    esito = []
    for v in os.listdir(path_download):
        if v.endswith('.mp4'):
            percorso_file = os.path.join(path_download, v)
            data_creazione = datetime.fromtimestamp(os.path.getctime(percorso_file))

            if min_ora <= data_creazione <= max_ora:
                # ✅ passa "v.mp4" come nome base, non solo "v"
                nome_finale = rinomina_se_doppio(path_video, "v.mp4")
                shutil.move(percorso_file, os.path.join(path_video, nome_finale))
                esito.append(nome_finale)
                lista_video.insert(tk.END, nome_finale)

    if esito:
        print(f"Copiatura riuscita: {len(esito)} file copiati → {esito}")
    else:
        print(f"Nessun file .mp4 trovato tra {min_ora.strftime('%H:%M')} e {max_ora.strftime('%H:%M')} del {ora_corrente.strftime('%d/%m/%Y')}")

copy_file = tk.Button(frame_video, text="Copy Video Down//Videos", command=f_copy)
copy_file.grid(row=1, column=0)

from moviepy import AudioFileClip, VideoFileClip
from PIL import Image, ImageTk
import re

clip_corrente = None
photo_corrente = None

def get_video_selezionato():
    sel = lista_video.curselection()
    if not sel:
        return None
    nome = lista_video.get(sel[0])
    return os.path.join("./videos", nome)

def mostra_frame(numero_frame):
    global clip_corrente, photo_corrente,frame

    if clip_corrente is None:
        return

    t = numero_frame / clip_corrente.fps
    t = min(t, clip_corrente.duration - 1/clip_corrente.fps)
    frame_img = clip_corrente.get_frame(t)

    img = Image.fromarray(frame_img)

    # ✅ nome corretto della tua canvas
    wc = frame.winfo_width()
    hc = frame.winfo_height()
    if wc <= 1 or hc <= 1:
        wc, hc = 640, 360

    w, h = img.size
    if w / h >= wc / hc:
        nuovo_w = wc
        nuovo_h = (wc * h) // w
    else:
        nuovo_h = hc
        nuovo_w = (hc * w) // h

    img = img.resize((nuovo_w, nuovo_h), Image.LANCZOS)
    photo_corrente = ImageTk.PhotoImage(img)

    # ✅ nome corretto della tua canvas
    frame.delete("all")
    frame.create_image(wc // 2, hc // 2, anchor="center", image=photo_corrente)

    n_totale = int(clip_corrente.fps * clip_corrente.duration)
    label_frame_info.config(text=f"Frame: {numero_frame} / {n_totale - 1}")

def f_selezione_f(event=None):
    global clip_corrente

    path = get_video_selezionato()
    if not path:
        return

    # Se c'era una clip precedente, chiudila per bene
    if clip_corrente:
        try:
            clip_corrente.close()
            del clip_corrente
        except:
            pass

    try:
        clip_corrente = VideoFileClip(path)
        n_frames = int(clip_corrente.fps * clip_corrente.duration)
        scorri_fotogrammi.config(to=n_frames - 1)
        scorri_fotogrammi.set(0)
        mostra_frame(0)
    except Exception as e:
        print(f"Errore caricamento clip: {e}")


def f_scorri(val):
    mostra_frame(int(float(val)))

def f_estrai():
    global clip_corrente

    path = get_video_selezionato()
    if not path or clip_corrente is None:
        print("Nessun video selezionato")
        return

    path_estra = "./output_image"
    os.makedirs(path_estra, exist_ok=True)

    numero_frame = int(float(scorri_fotogrammi.get()))
    t = numero_frame / clip_corrente.fps
    t = min(t, clip_corrente.duration - 1/clip_corrente.fps)

    frame_img = clip_corrente.get_frame(t)
    img = Image.fromarray(frame_img)

    # ✅ nome: est_frame_{primi 5 caratteri del video}_{numero frame}
    nome_video = os.path.splitext(os.path.basename(path))[0]
    prefisso = nome_video[:5]
    nome_file = f"est_frame_{prefisso}_{numero_frame}.png"
    path_out = os.path.join(path_estra, nome_file)

    # gestione doppio file con indice x1, x2 ecc.
    if os.path.exists(path_out):
        nome_out, ext_out = os.path.splitext(nome_file)
        match = re.search(r'^(.*x)(\d+)$', nome_out)
        if match:
            base = match.group(1)
            indice = int(match.group(2)) + 1
        else:
            base = nome_out + "x"
            indice = 1
        while os.path.exists(os.path.join(path_estra, f"{base}{indice}{ext_out}")):
            indice += 1
        nome_file = f"{base}{indice}{ext_out}"
        path_out = os.path.join(path_estra, nome_file)

    img.save(path_out)
    print(f"Frame salvato: {path_out}")

lista_video.bind('<<ListboxSelect>>', f_selezione_f)

# ✅ etichetta indicatore frame  
label_frame_info = tk.Label(frame_video, text="Frame: 0 / 0", bg='gray', fg='white')
label_frame_info.grid(row=2, column=1, padx=5)

estrai_framecorrente = tk.Button(frame_video, text="📷 Estrai Frame", command=f_estrai)
estrai_framecorrente.grid(row=1, column=1)

scorri_fotogrammi = ttk.Scale(frame_video, from_=0, to=100, orient="horizontal", command=f_scorri)
scorri_fotogrammi.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

import webbrowser

path_wanflash = "https://video.a2e.ai/wan-2-6?model=wan26-flash"

# Corretto: usa webbrowser.open invece di .get
Apri_A2e = tk.Button(
    frame_video, 
    text="genera Video A2E", 
    command=lambda: webbrowser.open(path_wanflash)
)
Apri_A2e.grid(row=3, column=0, padx=5, pady=5)

import os
import tkinter as tk
from moviepy import VideoFileClip, concatenate_videoclips,AudioFileClip,vfx

path_audio=''
def f_rendering():
    global path_audio
    path_video = "./videos"
    files_ordinati = lista_video.get(0, tk.END)
    
    if not files_ordinati:
        print("La lista è vuota!")
        return

    # --- ANALISI RISOLUZIONE (come prima) ---
    max_w, max_h = 960, 960
    for nome_file in files_ordinati:
        full_path = os.path.join(path_video, nome_file)
        if os.path.exists(full_path):
            try:
                with VideoFileClip(full_path) as clip:
                    w, h = clip.size
                    if w > max_w: max_w = w
                    if h > max_h: max_h = h
            except: pass

    # --- CARICAMENTO CLIP ---
    CLIPS = []
    for nome_file in files_ordinati:
        full_path = os.path.join(path_video, nome_file)
        if os.path.exists(full_path):
            try:
                clip = VideoFileClip(full_path)
                clip_resized = clip.resized(width=max_w, height=max_h)
                CLIPS.append(clip_resized)
            except Exception as e:
                print(f"Errore caricamento {nome_file}: {e}")

    if not CLIPS: return

    print("Inizio concatenazione...")
    video_finale = concatenate_videoclips(CLIPS, method="compose")

   # --- GESTIONE AUDIO DI BACKGROUND ---
    audio_clip = None
    if path_audio and os.path.exists(path_audio):
        try:
            # Importiamo l'effetto specifico direttamente dalla classe v2
            from moviepy.audio.fx import AudioFadeOut
            
            # Carica l'audio
            audio_bg = AudioFileClip(path_audio)
            
            # Taglia l'audio alla durata del video
            audio_bg = audio_bg.with_duration(video_finale.duration)
            
            # Applichiamo l'effetto usando la nuova sintassi .with_effects()
            # Questo evita l'errore di importazione del vecchio 'audio_fadeout'
            audio_bg = audio_bg.with_effects([AudioFadeOut(2)])
            
            # Applichiamo l'audio al video finale
            video_finale = video_finale.with_audio(audio_bg)
            audio_clip = audio_bg 
            print("🎵 Audio applicato con sfumatura finale di 2 secondi.")
        except Exception as e:
            print(f"⚠️ Errore audio (FX): {e}")

    # --- RENDERING FINALE ---
    try:
        output_name = "video_output_completo.mp4"
        video_finale.write_videofile(
            output_name, 
            fps=24, 
            codec="h264_nvenc" if "nvdia" else "libx264", # Shortcut logica
            audio_codec="aac"
        )
    except Exception as e:
        print(f"Fallback su CPU: {e}")
        video_finale.write_videofile(output_name, fps=24, codec="libx264", audio_codec="aac")

    # --- PULIZIA ---
    finally:
        try:
            video_finale.close()
            if audio_clip: audio_clip.close()
            for c in CLIPS: c.close()
        except: pass
    
    print("✨ Tutto pronto!")

# --- CORREZIONE BOTTONE TKINTER ---
# 'Impact' (senza la e), 'bold' invece di grossetto, 'fg' invece di color
Rendering = tk.Button(
    frame_video, 
    text="🎬 Rendering", 
    font=('Impact', 10, 'bold'), 
    bg='green', 
    fg='white', 
    command=f_rendering
)
Rendering.grid(row=3, column=1, padx=2, pady=2)

from tkinter import filedialog

def f_select_audio():
    global path_audio
    # Corretto l'uso di filedialog
    file_scelto = filedialog.askopenfilename(
        title="Seleziona Audio",
        filetypes=[("File Audio", "*.mp3 *.wav *.m4a *.aac")]
    )
    if file_scelto:
        path_audio = file_scelto
        print(f"✅ Audio caricato: {os.path.basename(path_audio)}")
    


seleziona_audio= tk.Button(frame_video,text='Select Audio',command=f_select_audio)
seleziona_audio.grid(row=4,column=1,padx=2,pady=2)











# Frame inferiore
frame3 = tk.Frame(window, bg='gray')
frame3.grid(row=1, column=0, columnspan=2, sticky="ew")

text = tk.Text(frame3, width=80, height=8)
text.grid(row=0, column=0, padx=5, pady=5, sticky="w")

framestrumenti = tk.Frame(frame3, bg='gray')
framestrumenti.grid(row=1, column=0, sticky="w", padx=5, pady=5)

tk.Label(framestrumenti, text='Steps',            bg='gray', fg='white').grid(row=0, column=0, padx=10)
tk.Label(framestrumenti, text='Lora',             bg='gray', fg='white').grid(row=0, column=1, padx=10)
tk.Label(framestrumenti, text='Seleziona Azione', bg='gray', fg='white').grid(row=0, column=2, padx=10)
tk.Label(framestrumenti, text='Nuova Azione', bg='gray', fg='white').grid(row=0, column=3, padx=10)

steps = tk.Scale(framestrumenti, from_=1, to=50, resolution=1, orient=tk.HORIZONTAL)
steps.grid(row=1, column=0, padx=10)
steps.set(8)

def load_lora(event=None):
    loramodels = ['no_lora']
    loramodels += [os.path.basename(l).split('.')[0] for l in os.listdir("Lora")]
    lora['values'] = loramodels

lora = ttk.Combobox(framestrumenti, values=[])
lora.grid(row=1, column=1, padx=10)
lora.bind('<ButtonPress-1>', load_lora)

seleziona_azione = ttk.Combobox(framestrumenti, values=[])
seleziona_azione.grid(row=1, column=2, padx=10)

prompts = []
loras = []

def f_azioni():
    global prompts, loras
    azioni = []
    prompts = []
    loras = []
    try:
        with open("prompt_define.txt", 'r') as f:
            for p in f.readlines():
                p = p.strip()
                if ':' in p:
                    parti = p.split(':', 2)  # max 3 parti: azione:prompt:lora
                    azioni.append(parti[0])
                    prompts.append(parti[1].replace('_', '').strip())
                    loras.append(parti[2].strip() if len(parti) > 2 else 'no_lora')
    except FileNotFoundError:
        pass
    seleziona_azione['values'] = azioni

f_azioni()

def scegli_selezione(event):
    global elementi_selezionati, lora
    idx = seleziona_azione.current()
    if idx >= 0 and idx < len(prompts):
        text.delete('1.0', tk.END)
        text.insert('1.0', prompts[idx])
        lora.set(loras[idx])

seleziona_azione.bind("<<ComboboxSelected>>", scegli_selezione)

new_azione= tk.Entry(framestrumenti)
new_azione.grid(row=1,column=3,padx=10)

from lycoris import create_lycoris_from_weights
from diffusers import Flux2KleinPipeline
from optimum.quanto import freeze, qfloat8, quantize
from deep_translator import GoogleTranslator
import torch
import gc
from safetensors import safe_open

def is_lokr_lora(path):
    try:
        with safe_open(path, framework="pt", device="cpu") as f:
            keys = list(f.keys())
        return any("lokr_w" in k for k in keys)
    except Exception:
        try:
            sd = torch.load(path, map_location="cpu", weights_only=True)
            return any("lokr_w" in k for k in sd.keys())
        except Exception:
            return False

def carica_lora(pipe, lora_path, adapter_name, weight=1.0):
    if is_lokr_lora(lora_path):
        print(f"  → Formato LoKr rilevato, uso LyCORIS per '{adapter_name}'")
        try:
            wrapper, _ = create_lycoris_from_weights(weight, lora_path, pipe.transformer)
            wrapper.merge_to()
            print(f"  → LoKr/LyCORIS merged nel transformer ✓")
            return "lycoris"
        except Exception as e:
            print(f"  ✗ Errore LyCORIS: {e}")
            return False
    else:
        print(f"  → Formato standard LoRA, uso Diffusers per '{adapter_name}'")
        try:
            pipe.load_lora_weights(lora_path, adapter_name=adapter_name)
            print(f"  → LoRA standard caricata ✓")
            return "diffusers"
        except Exception as e:
            print(f"  ✗ Errore Diffusers: {e}")
            return False

def resize_img(path):
    img = Image.open(path).convert('RGB')
    w, h = img.size
    rw, rh = 512, 512
    if w >= h:
        rh = (rw * h) // w
    else:
        rw = (rh * w) // h
    return img.resize((rw, rh), Image.BICUBIC)

def carica_immagini_riferimento(ref1, ref2, ref3):
    images = []
    for ref in [ref1, ref2, ref3]:
        if not ref or ref in ('no_riferimento', '-- image reference --', '-- image output --'):
            continue
        for folder in ['image_referenze', 'output_image']:
            for ext in ['.jpg', '.png']:
                path = os.path.join(folder, ref + ext)
                if os.path.exists(path):
                    images.append(resize_img(path))
                    break
    return images

def prepara_pipe(lora_name):
    dtype = torch.bfloat16
    gc.collect()
    torch.cuda.empty_cache()
    print(f"[VRAM] Libera: {torch.cuda.mem_get_info()[0] / 1024**3:.2f} GB")
    print("Caricamento pipeline FLUX.2 klein 9B...")

    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-9B",
        torch_dtype=dtype,
        low_cpu_mem_usage=False
    )
    if hasattr(pipe, 'safety_checker'):
        pipe.safety_checker = None

    # carica lora se presente
    if lora_name and lora_name != 'no_lora':
        lora_path = os.path.join("Lora", lora_name + ".safetensors")
        if not os.path.exists(lora_path):
            # prova senza estensione (nome già completo)
            lora_path = os.path.join("Lora", lora_name)
        if os.path.exists(lora_path):
            result = carica_lora(pipe, lora_path, "lora1", weight=1.0)
            if result == "diffusers":
                pipe.set_adapters("lora1", adapter_weights=1.0)
        else:
            print(f"  ✗ File lora non trovato: {lora_path}")

    print("Quantizzazione transformer...")
    quantize(pipe.transformer, weights=qfloat8)
    freeze(pipe.transformer)
    if hasattr(pipe, 'text_encoder') and pipe.text_encoder is not None:
        quantize(pipe.text_encoder, weights=qfloat8)
        freeze(pipe.text_encoder)

    pipe.enable_model_cpu_offload()
    pipe.enable_attention_slicing()
    pipe.vae.enable_slicing()
    pipe.vae.enable_tiling()
    gc.collect()
    torch.cuda.empty_cache()
    return pipe

def genera_immagine(pipe, prompt, images, steps_val, output_path):
    try:
        prompt_en = GoogleTranslator(source='it', target='en').translate(prompt)
    except Exception:
        prompt_en = prompt

    gen_params = {
        "prompt":              prompt_en,
        "height":              1024,
        "width":               1024,
        "guidance_scale":      1.0,
        "num_inference_steps": steps_val,
        "generator":           torch.Generator(device="cpu").manual_seed(0)
    }
    if len(images) == 1:
        gen_params["image"] = images[0]
    elif len(images) > 1:
        gen_params["image"] = images

    image = pipe(**gen_params).images[0]
    image.save(output_path)
    print(f"[OK] Immagine salvata: {output_path}")

def libera_pipe(pipe):
    del pipe
    gc.collect()
    torch.cuda.empty_cache()
    torch.cuda.synchronize()

def flux2():
    global text, lora, elementi_selezionati, lista_azioni
    global combo_riferenze1, combo_riferenze2, combo_riferenze3, steps

    steps_val = steps.get()

    # ── CASO 1: lista vuota o elementi_selezionati vuoti ──────────────────────
    if len(elementi_selezionati) == 0:
        print("[CASO 1] Nessun elemento in lista, uso widget correnti")
        lora_name  = lora.get()
        prompt     = text.get('1.0', tk.END).strip()
        ref1       = combo_riferenze1.get()
        ref2       = combo_riferenze2.get()
        ref3       = combo_riferenze3.get()
        images     = carica_immagini_riferimento(ref1, ref2, ref3)
        pipe       = prepara_pipe(lora_name)

        out = "output_image/flux_out.jpg"
        if os.path.exists(out):
            k = 1
            while os.path.exists(f"output_image/flux_out_{k}.jpg"):
                k += 1
            out = f"output_image/flux_out_{k}.jpg"

        genera_immagine(pipe, prompt, images, steps_val, out)
        libera_pipe(pipe)
        return

    selezione = lista_azioni.curselection()

    # ── CASO 2: elemento selezionato nella lista ───────────────────────────────
    if selezione:
        idx = selezione[0]
        el  = elementi_selezionati[idx]
        print(f"[CASO 2] Elemento selezionato idx={idx}: {el['azione']}")
        images = carica_immagini_riferimento(el['ref1'], el['ref2'], el['ref3'])
        pipe   = prepara_pipe(el['lora'])
        output = f"output_image/0_{idx}_{el['azione']}.jpg"
        genera_immagine(pipe, el['descrizione'], images, steps_val, output)
        libera_pipe(pipe)
        return

    # ── CASO 3: lista non vuota ma nessun elemento selezionato → ciclo tutti ──
    print(f"[CASO 3] Ciclo su {len(elementi_selezionati)} elementi")
    for i, el in enumerate(elementi_selezionati):
        print(f"  [{i+1}/{len(elementi_selezionati)}] {el['azione']}")
        images = carica_immagini_riferimento(el['ref1'], el['ref2'], el['ref3'])
        pipe   = prepara_pipe(el['lora'])
        output = f"output_image/{i}_{el['azione']}.jpg"
        genera_immagine(pipe, el['descrizione'], images, steps_val, output)
        libera_pipe(pipe)

genera = tk.Button(framestrumenti, text='Genera immagine', command=flux2)
genera.grid(row=1, column=4, padx=10)

# Array multiplo: ogni elemento è un dict con tutti i campi
elementi_selezionati = []

_aggiornando = False

def aggiorna_listbox():
    global _aggiornando
    _aggiornando = True
    lista_azioni.delete(0, tk.END)
    for el in elementi_selezionati:
        lista_azioni.insert(tk.END, f"{el['azione']}  |  lora: {el['lora']}")
    _aggiornando = False

def F_aggiungialista():
    testo_new_azione = new_azione.get().strip()
    idx_azione = seleziona_azione.current()

    # serve almeno una delle due: azione selezionata o nuova azione
    if idx_azione < 0 and testo_new_azione == '':
        return

    # se c'è una nuova azione la aggiunge ai valori della combobox
    if testo_new_azione != '':
        azione_finale = testo_new_azione
        valori_attuali = list(seleziona_azione['values'])
        if testo_new_azione not in valori_attuali:
            valori_attuali.append(testo_new_azione)
            seleziona_azione['values'] = valori_attuali
            prompts.append('')      # prompt vuoto per la nuova azione
            loras.append('no_lora') # lora default per la nuova azione
        new_azione.delete(0, tk.END)
    else:
        azione_finale = seleziona_azione.get()

    nuovo = {
        'azione':      azione_finale,
        'descrizione': text.get('1.0', tk.END).strip(),
        'lora':        lora.get() or 'no_lora',
        'ref1':        combo_riferenze1.get(),
        'ref2':        combo_riferenze2.get(),
        'ref3':        combo_riferenze3.get(),
    }

    selezione = lista_azioni.curselection()
    if selezione:
        idx = selezione[0]
        elementi_selezionati[idx] = nuovo
        print(f"[MODIFICA idx={idx}]")
    else:
        elementi_selezionati.append(nuovo)
        print(f"[AGGIUNTA idx={len(elementi_selezionati)-1}]")

    aggiorna_listbox()

    print(f"  azione      : {nuovo['azione']}")
    print(f"  descrizione : {nuovo['descrizione']}")
    print(f"  lora        : {nuovo['lora']}")
    print(f"  ref1        : {nuovo['ref1']}")
    print(f"  ref2        : {nuovo['ref2']}")
    print(f"  ref3        : {nuovo['ref3']}")
    if selezione:
        print(f"  array elemento modificato: {elementi_selezionati[idx]}")
    else:
        print(f"  array elemento aggiunto:   {elementi_selezionati[-1]}")
    print("-" * 60)

aggiungi_a_lista = tk.Button(framestrumenti, text='Aggiungi a lista', command=F_aggiungialista)
aggiungi_a_lista.grid(row=1, column=5, padx=10)

def scegli_da_lista(event):
    if _aggiornando:  # <-- blocca durante aggiorna_listbox
        return
    selezione = lista_azioni.curselection()
    if not selezione:
        return
    idx = selezione[0]
    el = elementi_selezionati[idx]

    text.delete('1.0', tk.END)
    text.insert('1.0', el['descrizione'])
    lora.set(el['lora'])
    combo_riferenze1.set(el['ref1'])
    combo_riferenze2.set(el['ref2'])
    combo_riferenze3.set(el['ref3'])

    valori = list(seleziona_azione['values'])
    if el['azione'] in valori:
        seleziona_azione.current(valori.index(el['azione']))
    print(elementi_selezionati[idx])

lista_azioni.bind("<<ListboxSelect>>", scegli_da_lista)
def deseleziona_lista(event):
    lista_azioni.selection_clear(0, tk.END)

lista_azioni.bind('<Button-3>', deseleziona_lista)

from tkinter import ttk, messagebox

def salva():
    global prompts, elementi_selezionati
    salva_elementi = []
    try:
        with open("prompt_define.txt", 'r') as f:
            righe = f.readlines()

        # aggiorna le azioni già presenti nel file
        azioni_nel_file = []
        for p in righe:
            p = p.strip()
            if ':' not in p:
                continue
            parti = p.split(':', 2)
            azione = parti[0]
            prompt = parti[1].replace('_', '').strip()
            azioni_nel_file.append(azione)

            trovato = False
            for el in elementi_selezionati:
                if azione == el['azione']:
                    trovato = True
                    lora_str = el['lora'] if el['lora'] != 'no_lora' else ''
                    if prompt != el['descrizione']:
                        salva_elementi.append(f"{azione}:{el['descrizione']}_:{lora_str}\n")
                    else:
                        salva_elementi.append(f"{azione}:{prompt}_:{lora_str}\n")
                    break

            if not trovato:
                lora_orig = parti[2].strip() if len(parti) > 2 else ''
                salva_elementi.append(f"{azione}:{prompt}_:{lora_orig}\n")

        # aggiunge le nuove azioni NON presenti nel file
        for el in elementi_selezionati:
            if el['azione'] not in azioni_nel_file:
                lora_str = el['lora'] if el['lora'] != 'no_lora' else ''
                salva_elementi.append(f"{el['azione']}:{el['descrizione']}_:{lora_str}\n")

        with open("prompt_define.txt", 'w') as f:
            f.writelines(salva_elementi)

        # ricarica prompts e loras dal file aggiornato
        f_azioni()

        messagebox.showinfo("Salvataggio", f"Prompts salvati con successo!\n{len(salva_elementi)} azioni salvate.")

    except FileNotFoundError:
        # se il file non esiste lo crea da zero con gli elementi_selezionati
        with open("prompt_define.txt", 'w') as f:
            for el in elementi_selezionati:
                lora_str = el['lora'] if el['lora'] != 'no_lora' else ''
                f.write(f"{el['azione']}:{el['descrizione']}_:{lora_str}\n")
        f_azioni()
        messagebox.showinfo("Salvataggio", "File creato con successo!")
    except Exception as e:
        messagebox.showerror("Errore", f"Errore durante il salvataggio:\n{e}")


salva_su_disco = tk.Button(framestrumenti, text='Salva su disco', command=salva)
salva_su_disco.grid(row=1, column=6)



# --- Frame riferimenti immagini ---
framestrumenti2 = tk.Frame(frame3, bg='Gray')
framestrumenti2.grid(row=2, column=0)

def load_reference_and_out(combo_ref):
    def _load(event=None):
        images = ['no_riferimento']
        images += ['-- image reference --']
        images += [os.path.basename(img).split('.')[0] for img in os.listdir("image_referenze")]
        images += ['-- image output --']
        images += [os.path.basename(img).split('.')[0] for img in os.listdir("output_image")]
        combo_ref['values'] = images
    return _load

canvas_images = {}

def select_reference(combo, canvas):
    def _select(event=None):
        name = combo.get()
        path = None

        if name in ('no_riferimento', '-- image reference --', '-- image output --'):
            canvas.delete('all')
            return

        for folder in ["image_referenze", "output_image"]:
            for ext in [".jpg", ".png"]:
                candidate = os.path.join(folder, name + ext)
                if os.path.exists(candidate):
                    path = candidate
                    break
            if path:
                break

        if path is None:
            canvas.delete('all')
            return

        img = Image.open(path).convert('RGB')
        w, h = img.size
        rw, rh = 128, 128
        if w >= h:
            rh = (128 * h) // w
        else:
            rw = (128 * w) // h

        img = img.resize((rw, rh), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        canvas_images[canvas] = photo
        canvas.delete('all')
        canvas.create_image(64, 64, anchor='center', image=photo)
        canvas.update()
    return _select

# --- Gruppo 1 ---
tk.Label(framestrumenti2, text="Image riferimento 1").grid(row=0, column=0)
canvas1 = tk.Canvas(framestrumenti2, width=128, height=128, bg='red')
canvas1.grid(row=1, column=0, padx=10, pady=5)
combo_riferenze1 = ttk.Combobox(framestrumenti2)
combo_riferenze1.grid(row=2, column=0)
combo_riferenze1.bind('<ButtonPress-1>', load_reference_and_out(combo_riferenze1))
combo_riferenze1.bind('<<ComboboxSelected>>', select_reference(combo_riferenze1, canvas1))

# --- Gruppo 2 ---
tk.Label(framestrumenti2, text="Image riferimento 2").grid(row=0, column=1)
canvas2 = tk.Canvas(framestrumenti2, width=128, height=128, bg='red')
canvas2.grid(row=1, column=1, padx=10, pady=5)
combo_riferenze2 = ttk.Combobox(framestrumenti2)
combo_riferenze2.grid(row=2, column=1)
combo_riferenze2.bind('<ButtonPress-1>', load_reference_and_out(combo_riferenze2))
combo_riferenze2.bind('<<ComboboxSelected>>', select_reference(combo_riferenze2, canvas2))

# --- Gruppo 3 ---
tk.Label(framestrumenti2, text="Image riferimento 3").grid(row=0, column=2)
canvas3 = tk.Canvas(framestrumenti2, width=128, height=128, bg='red')
canvas3.grid(row=1, column=2, padx=10, pady=5)
combo_riferenze3 = ttk.Combobox(framestrumenti2)
combo_riferenze3.grid(row=2, column=2)
combo_riferenze3.bind('<ButtonPress-1>', load_reference_and_out(combo_riferenze3))
combo_riferenze3.bind('<<ComboboxSelected>>', select_reference(combo_riferenze3, canvas3))

window.mainloop()