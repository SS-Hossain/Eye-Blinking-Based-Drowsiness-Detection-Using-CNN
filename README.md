# Eye-Blinking-Based Drowsiness Detection Using CNN

## 📌 Overview
This project implements a **Convolutional Neural Network (CNN)** to detect driver drowsiness by analyzing **eye-blinking patterns** from video or image input.  
The system raises an **audio alert** if prolonged eye closure is detected, helping reduce accidents caused by fatigue.

---

## 📂 Repository Structure

```
.
├── Model_Train.ipynb               # CNN model training script
├── Model_test_image.ipynb           # Test model with single images
├── model_test_video.ipynb           # Real-time/video testing
├── haarcascade_eye.xml              # Haar Cascade for eye detection
├── haarcascade_frontalface_default.xml  # Haar Cascade for face detection
├── alarm-sound.mp3                  # Alert sound when drowsiness is detected
├── Custom Dataset.zip               # User-collected dataset
├── Google Sourced Dataset.zip       # Dataset from Google images
├── TrainedModel/                    # Saved trained models
└── README.md                        # Project documentation
```

---

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/SS-Hossain/Eye-Blinking-Based-Drowsiness-Detection-Using-CNN.git
   cd Eye-Blinking-Based-Drowsiness-Detection-Using-CNN
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   # Activate the environment
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Usage

### **1. Training the Model**
- Open `Model_Train.ipynb` in Jupyter Notebook.
- Load and preprocess datasets (`Custom Dataset.zip` or `Google Sourced Dataset.zip`).
- Train the CNN model and save it to the `TrainedModel/` folder.

### **2. Testing on Images**
- Open `Model_test_image.ipynb`.
- Load the trained model.
- Provide an image as input to check drowsiness detection.

### **3. Testing on Videos / Real-Time**
- Open `model_test_video.ipynb`.
- Use webcam or pre-recorded video as input.
- If prolonged eye closure is detected, `alarm-sound.mp3` will play.

---

## 📊 Expected Results
- High accuracy for distinguishing between **open** and **closed** eyes.
- Real-time detection with minimal latency.
- Audio alerts for timely driver notification.

---

## 📦 Dataset Preparation
- Extract datasets to an accessible directory.
- Organize into subfolders (e.g., `OpenEyes/`, `ClosedEyes/`).
- Preprocess images (resize, normalize) before training.

---

## 🛠 Requirements
See [`requirements.txt`](requirements.txt) for full list.

---

## 📜 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements
- Haar Cascade XML files from **OpenCV** for face and eye detection.
- Inspiration from academic research on driver drowsiness detection.
- TensorFlow/Keras community for deep learning frameworks.
