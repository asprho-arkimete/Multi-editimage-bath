Multi-Edit Image Batch — FLUX.2-klein-9B
Modifica immagini con FLUX.2-klein-9B tramite funzione batch, che ti permette di gestire:

Multi reference images — più immagini di riferimento contemporaneamente
Multi LoRA — caricamento e combinazione di più LoRA in un unico processo
Una delle batch di editing immagini più complete disponibili per FLUX.2-klein-9B

Collegamento integrato ad A2E per la generazione video e rendering con selezione di background audio.

Installazione
Clona il repository:
git clone https://github.com/asprho-arkimete/Multi-editimage-bath.git
cd Multi-editimage-bath
Crea e attiva l'ambiente virtuale:
python -m venv vselect
cd .\vselect\Scripts
activate
cd ..\..
Installa PyTorch con supporto CUDA 12.8:
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu128
Installa le dipendenze:
pip install -r requirements.txt

LoRA
Scarica i LoRA da Civitai filtrando per: FLUX.2-klein-9B
Inseriscili nella cartella Lora/ — i nomi dei file sono definiti nel file prompt_define.

Avvio
python select_action.py


