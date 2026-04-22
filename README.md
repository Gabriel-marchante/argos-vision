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
- [ ] Módulo de reconocimiento facial
- [ ] Módulo de captura de audio
- [ ] Módulo de lectura de labios
- [ ] Fusión audio-visual
- [ ] Integración con LLM
- [ ] Base de datos vectorial
- [ ] Interfaz gráfica
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

## 🤝 Contribuir

Las contribuciones son bienvenidas. Abre un issue para discutir cambios importantes antes de enviar un PR.

1. Haz fork del proyecto
2. Crea tu rama de feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

---

## 📜 Licencia

MIT License — Ver [LICENSE](LICENSE) para más detalles.

---

<div align="center">

*"Cien ojos abiertos. Nada escapa."*

**ARGOS** · 2026

</div>
