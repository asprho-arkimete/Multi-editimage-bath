# Multi-editimage-bath
Edita imagini con flux 2 kelvien 9B con funzione bath, che ti permette di avere un multi reference images, multi lora, un delle bath di editing images in flux 2 klein 9b. collegamento a A2E per generare video e rendering Video con select background  Audio.

clona: git clone: https://github.com/asprho-arkimete/Multi-editimage-bath.git
cd Multi-editimage-bath
crea ambiente virtuale: python -m venv vselect
cd .\vselect\Scripts
activate
cd.. cd..

scarica i lora da civitai filtri:[flux 2 klein 9b] mettili nella cartella Lora
trovi i nomi dei lora nel file prompt define

pip install -r requirements.txt

python select_action.py


