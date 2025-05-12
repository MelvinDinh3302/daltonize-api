# Daltonize API

This **Daltonize API** processes images to generate colorblind-friendly versions. It takes an input image and returns a modified image that are more visible for colorblind viewers. This API is made to serve as the backend for a future React Native front-end app.

## Run It on Your Own Machine

### Requirements
Python 3.x

### Installation & Usage

1. **Install dependencies**  
   Run the following command to install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Flask server**  
   Launch the API locally by running:
   ```bash
   python3 app.py
   ```

3. **Send a request using curl**  
   Use the following command to send an image to the API and receive the daltonized version:
   ```bash
   curl -X POST -F "image=@<input>" http://<your_host_ip>:5000/daltonize --output <output>
   ```
   **Example:**
   ```bash
   curl -X POST -F "image=@flower.jpg" http://127.0.0.1:5000/daltonize --output result.jpg
   ```
