<div align="center">

# 👁️ ARGOS

### *El vigilante de los cien ojos*

**A**utomated · **R**ecognition & **G**athering · **O**bservation **S**ystem

---

*"Y Hera tomó los cien ojos de Argos Panoptes y los colocó en la cola del pavo real,  
para que la vigilancia nunca cesara."*

---

![Status](https://img.shields.io/badge/status-in%20development-orange)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

</div>

---

## 🏛️ El mito

En la mitología griega, **Argos Panoptes** (Ἄργος Πανόπτης, "el que todo lo ve") era un gigante con cien ojos repartidos por todo el cuerpo. Hera lo designó como guardián eterno porque, incluso durmiendo, cincuenta de sus ojos permanecían abiertos. Era el vigilante perfecto: nada escapaba a su mirada.

Este proyecto hereda su nombre y su propósito.

---

## 🎯 ¿Qué es ARGOS?

ARGOS es un asistente inteligente de reconocimiento e identificación de personas que combina **visión por computadora**, **reconocimiento de voz**, **lectura de labios** e **IA generativa** para construir perfiles contextuales de forma automática.

No se limita a "ver" — también **escucha, contrasta y recuerda**.

---

## ✨ Características

- 👁️ **Reconocimiento facial en tiempo real** — Detecta e identifica rostros conocidos desde la base de datos.
- 🆕 **Auto-registro de desconocidos** — Los rostros no identificados se almacenan con un alias temporal (`sinreconocer1`, `sinreconocer2`…) y se enriquecen con el tiempo.
- 🎤 **Captura conversacional dual** — Recoge audio por micrófono y lo contrasta con lectura de labios por visión para maximizar la precisión en entornos ruidosos.
- 🧠 **Análisis con IA** — Un modelo de lenguaje filtra la conversación y decide qué información es relevante guardar (intereses, relaciones, contexto, datos personales).
- 💾 **Memoria evolutiva** — El perfil de cada persona se enriquece automáticamente con cada nueva interacción.
- 🔒 **Privacidad por diseño** — Datos cifrados, control total del usuario sobre qué se guarda.

---

## 🖥️ Dashboard (Centro de Control)

La interfaz web de Argos está dividida en tres paneles principales diseñados para funcionar como un centro de vigilancia integral:

- **Panel Izquierdo ("Observatory Targets")**: Funciona como un radar de personas. Muestra una lista en tiempo real de todas las caras detectadas por la cámara. A los desconocidos se les asigna un alias automático, mientras que a los conocidos se les identifica por su nombre. Al hacer clic en cualquier persona, se despliega su información.
- **Panel Central ("Live Feed")**: Muestra la transmisión de vídeo en directo de la cámara, complementada con un efecto visual de escáner (scanline) que refuerza la estética de monitorización avanzada.
- **Panel Derecho ("Intelligence Debrief")**: Es el cerebro analítico del sistema. Al seleccionar un objetivo en el panel izquierdo, este panel muestra:
  - **Perfil Dinámico**: Información, gustos, intereses o contexto que la IA ha deducido y almacenado automáticamente al procesar conversaciones pasadas.
  - **Transcripts Recientes**: Un registro textual de las últimas interacciones captadas por Argos utilizando el modelo Whisper.

---

## 🏗️ Arquitectura

```
   ┌─────────────┐
   │   CÁMARA    │
   └──────┬──────┘
          │
    ┌─────┴──────┐
    ▼            ▼
┌────────┐  ┌──────────┐
│ Rostro │  │  Labios  │
└───┬────┘  └────┬─────┘
    │            │
    ▼            │
┌────────┐       │     ┌────────────┐
│  Base  │       │     │ MICRÓFONO  │
│   de   │       │     └─────┬──────┘
│ datos  │       │           │
└───┬────┘       ▼           ▼
    │      ┌─────────────────────┐
    │      │  Fusión audio+vídeo │
    │      └──────────┬──────────┘
    │                 │
    └────────┐        ▼
             ▼   ┌─────────┐
          ┌───────┐   IA   │
          │ PERFIL│◄──────┤  (LLM)  │
          └───────┘   └─────────┘
```

---

## 🛠️ Stack técnico (propuesto)

| Componente | Tecnología sugerida |
|------------|---------------------|
| Reconocimiento facial | `face_recognition` / `InsightFace` / `DeepFace` |
| Detección de rostros | `OpenCV` + `MediaPipe` |
| Lectura de labios | `AV-HuBERT` / `LipNet` |
| Speech-to-text | `Whisper` (OpenAI) / `Vosk` |
| IA generativa | `Claude API` / `GPT-4` / modelo local con `Ollama` |
| Base de datos | `SQLite` (local) / `PostgreSQL` + `pgvector` (vectorial) |
| Backend | `Python 3.10+` con `FastAPI` |

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/TU_USUARIO/argos.git
cd argos

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus claves de API

# Inicializar base de datos
python scripts/init_db.py

# Ejecutar
python main.py
```

---

## 📁 Estructura del proyecto

```
argos/
├── src/
│   ├── vision/          # Reconocimiento facial y lectura de labios
│   ├── audio/           # Captura y transcripción de voz
│   ├── fusion/          # Cruce audio-visual
│   ├── ai/              # Integración con LLM
│   ├── database/        # Modelos y gestión de BD
│   └── core/            # Lógica principal
├── models/              # Modelos preentrenados
├── data/                # Base de datos local
├── tests/
├── scripts/
└── main.py
```

---

## 🧭 Roadmap

- [x] Definición del proyecto
- [x] Módulo de reconocimiento facial
- [x] Módulo de captura de audio
- [x] Módulo de lectura de labios
- [ ] Fusión audio-visual avanzada
- [x] Integración con LLM (OpenAI / Anthropic)
- [ ] Base de datos vectorial
- [x] Interfaz gráfica (Dashboard Web)
- [ ] Modo offline completo
- [ ] Cifrado end-to-end de perfiles

---

## 🔒 Privacidad y ética

ARGOS maneja **datos biométricos y conversaciones privadas**. Este proyecto se desarrolla bajo los siguientes principios:

- ⚖️ **Cumplimiento RGPD** — Diseñado desde cero bajo la legislación europea de protección de datos.
- 🔐 **Cifrado local** — Ningún dato biométrico sale del dispositivo sin consentimiento explícito.
- 🗑️ **Derecho al olvido** — Cualquier perfil puede eliminarse completamente en cualquier momento.
- 🚫 **Uso responsable** — Este software NO debe usarse para vigilancia masiva, acoso ni sin el consentimiento de las personas identificadas.

> ⚠️ **Advertencia legal:** El uso de reconocimiento facial sobre terceros sin su consentimiento puede ser ilegal en tu jurisdicción. El autor no se hace responsable del uso indebido de esta herramienta.


---

## ✍️ Créditos

Desarrollado por **Macloud Team (Gabriel Marchante)**. Inspirado en herramientas de seguridad clásicas y estética retro-futurista.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/gabriel-m-833856242/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Gabriel-marchante)

---

<div align="center">

*"Cien ojos abiertos. Nada escapa."*



</div>
