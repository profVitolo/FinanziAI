# Utilizzo della GPU NVIDIA (opzionale)
Per impostazione predefinita il progetto utilizza la versione CPU di `llama-cpp-python`.
Se disponi di una GPU NVIDIA, puoi ottenere prestazioni nettamente superiori installando la build CUDA.

## 1. Installa il CUDA Toolkit
Scarica e installa il CUDA Toolkit >= 12.5 (ad esempio la versione **12.8**):
https://developer.nvidia.com/cuda-12-8-0-download-archive

Al termine dell'installazione verifica che CUDA sia correttamente configurato:
```
nvcc --version
```

Dovresti ottenere un output simile a:
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Jan_15_19:38:46_Pacific_Standard_Time_2025
Cuda compilation tools, release 12.8, V12.8.61
Build cuda_12.8.r12.8/compiler.35404655_0
```

---

## 2. Installa la build CUDA di llama-cpp-python
Se hai già installato le dipendenze del progetto, puoi reinstallarlo completamente:
```bash
pip uninstall llama-cpp-python
pip cache purge
pip install --only-binary=:all: --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu125 llama-cpp-python
```

---

## 3. Verifica l'installazione
Controlla che il modulo venga caricato correttamente:
```python
from llama_cpp import llama_print_system_info
print(llama_print_system_info())
```

Se non vengono sollevate eccezioni, la libreria è installata correttamente.
L'output tipico è questo
```
ggml_cuda_init: found 1 CUDA devices (Total VRAM: 12287 MiB):
  Device 0: NVIDIA GeForce RTX 3060, compute capability 8.6, VMM: yes, VRAM: 12287 MiB
b'CUDA : ARCHS = 600,610,700,750,800,860,890,900 | FORCE_MMQ = 1 | USE_GRAPHS = 1 | PEER_MAX_BATCH_SIZE = 128 | CPU : SSE3 = 1 | SSSE3 = 1 | AVX = 1 | AVX2 = 1 | F16C = 1 | FMA = 1 | LLAMAFILE = 1 | OPENMP = 1 | REPACK = 1 | '
```

---

## 4. Abilita la GPU
Nel file `config.py` imposta:
```python
LLM_GPU_LAYERS = -1
```

Il valore `-1` indica a `llama.cpp` di caricare automaticamente il maggior numero possibile di layer del modello nella GPU, sfruttando tutta la VRAM disponibile.

---

## 5. Verifiche finali
Per verificare che il modello stia realmente utilizzando la GPU durante l'inferenza (ti basta lanciare il test 20):
```bash
nvidia-smi -l 1
```

Durante la generazione della risposta dovresti osservare:
- il processo `python.exe`;
- alcuni GB di VRAM occupata;
- un utilizzo della GPU.

---

## Note
- La versione CUDA deve essere compatibile con il CUDA Toolkit installato.
- Attualmente la build `cu125` risulta compatibile anche con sistemi che utilizzano CUDA Toolkit 12.8.
- Se non disponi di una GPU NVIDIA, non è necessario eseguire questa procedura: il progetto funzionerà regolarmente utilizzando la CPU.