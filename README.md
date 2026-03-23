# 🚗 Radar Tools – ARS408 CAN Visualization & Configuration

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![PyQt6](https://img.shields.io/badge/UI-PyQt6-green)
![Status](https://img.shields.io/badge/status-active-success)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows-lightgrey)

---

## 📡 Overview

**Radar Tools** is a desktop application for **real-time visualization, decoding, and configuration** of ARS408 automotive radar sensors via CAN.

It is designed for:

* Embedded engineers
* Automotive radar validation
* CAN debugging and analysis

---

## ✨ Features

### 🔌 CAN Interface

* Supports:

  * `socketcan`
  * `pcan`
* Configurable:

  * Channel
  * Bitrate

---

### 🎯 Radar Modes

#### 🟢 Object Mode

* Frames:

  * `0x60A` – Measurement cycle
  * `0x60B/C/D` – Object data
* Data:

  * Distance (Long / Lat)
  * Velocity
  * Classification
  * Probability of existence

---

#### 🔵 Cluster Mode

* Frames:

  * `0x70x` (DBC dependent)
* Data:

  * Cluster position
  * RCS
  * Velocity

---

### 🧠 Multi-Radar Support (0–7)

* Automatic radar ID extraction:

```python
radar_id = (arbitration_id >> 8) & 0xF
```

* Independent cycle per radar
* Unified visualization (no flicker)
* Color-coded rendering per radar

---

### 🎨 Visualization

* Real-time 2D scatter plot
* Axes:

  * X → Lateral distance
  * Y → Longitudinal distance

#### Features:

* Zoom (mouse scroll)
* Grid with fixed spacing
* Auto scaling
* Bulk rendering (high performance)

---

### 🎛️ Radar Visibility Toggle

* Enable/disable visualization per radar
* Instant update
* Does not affect processing

---

### 🔍 Filters (Real-Time)

| Filter            | Mode           |
| ----------------- | -------------- |
| DistLong min/max  | Object/Cluster |
| DistLat min/max   | Object/Cluster |
| RCS min/max       | Object/Cluster |
| ProbOfExist (min) | Object only    |

✔ Applied in backend
✔ Snapshot-based
✔ Zero UI lag

---

### 📊 Live Views

#### Object Table

* Radar ID
* Object ID
* Distance
* Velocity
* Class

#### Cluster Table

* Radar ID
* Cluster ID
* Distance
* RCS

---

### ⚙️ Radar Info Panels

* 📡 `0x201` → Radar configuration
* 🧾 `0x700` → Firmware information

Accessible via UI buttons.

---

## 🏗️ Architecture

```text
CAN Bus
   ↓
DBC Decoder
   ↓
ObjectCache / ClusterCache
   ↓
Filter Engine
   ↓
Snapshot (Merged Multi-Radar)
   ↓
UI (Plot + Tables)
```

---

## 📁 Project Structure

```
Radar-Tools/
│
├── processing/
│   ├── object_cache.py
│   ├── cluster_cache.py
│   ├── numeric_filter.py
│   ├── radar_mode.py
│
├── gui/
│   ├── main_window.py
│   ├── radar_view.py
│   ├── live_view.py
│   ├── connection_panel.py
│   ├── numeric_filter_panel.py
│   ├── radar_visibility_panel.py
│   ├── radar_selector_dialog.py
|   ├── config_panel.py
|   ├── radar_visibility_panel.py
│
├── resources/
│   ├── *.dbc
|
├── can_interface/
│   ├── can_manager.py
|   ├── dbc_decoder.py
│
├── main.py
└── README.md
```

---

## 🔄 Data Flow

```
CAN Frame
   ↓
DBC Decode
   ↓
Per-Radar Cache
   ↓
Cycle Aggregation
   ↓
Merged Snapshot
   ↓
Filter Engine
   ↓
UI Rendering
```

---

## 🎨 Radar Color Map

| Radar | Color      |
| ----- | ---------- |
| 0     | 🔴 Red     |
| 1     | 🟢 Green   |
| 2     | 🔵 Blue    |
| 3     | 🟡 Yellow  |
| 4     | 🟣 Magenta |
| 5     | 🔷 Cyan    |
| 6     | 🟠 Orange  |
| 7     | 🟤 Purple  |

---

## 📸 Screenshots

> will be added

```
docs/
 ├── plot.png
 ├── table.png
 └── filters.png
```

---

## ⚡ Performance

* Bulk updates (`update_plot_bulk`)
* No UI blocking loops
* Snapshot-based rendering
* Thread-safe caches

---

## 🧩 Dependencies

```bash
pip install pyqt6 pyqtgraph python-can cantools
```

---

## ▶️ Running

```bash
python main.py
```

---

## 🧪 Supported Hardware

* Continental ARS408 Radar
* CAN interfaces:

  * PCAN
  * SocketCAN (Linux)

---

## 🔧 Roadmap

* [ ] Object tracking (history trails)
* [ ] Heatmap visualization
* [ ] Recording & playback (CAN logs)
* [ ] Multi-radar statistics
* [ ] Combined Object + Cluster mode
* [ ] Advanced UI filters (sliders)

---

## 🤝 Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss.

---

## 👨‍💻 Author

**Matheus Nascimento**
Electrical Engineer – Embedded Systems & Radar Processing

---

## 📄 License

public

---

