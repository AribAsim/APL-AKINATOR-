# Setup Plan: APL-AKINATOR-

## 1. Code Analysis
Your project is a full-stack application structured into two main parts:
- **Backend**: A Python-based API built using **FastAPI**. It includes modules for game logic (probability engine, question selector), data generation, and API routing. It also uses the Gemini API (`google-genai`) for question generation and BeautifulSoup for scraping.
- **Frontend**: A React application built with **Vite**. It uses `axios` for HTTP requests, `animejs` for animations, and `lucide-react` for icons.

## 2. Backend Setup & Virtual Environment
To keep your Python dependencies isolated, you should create a virtual environment.

### Step 1: Navigate to the backend directory
Open your terminal and run:
```bash
cd backend
```

### Step 2: Create a Virtual Environment
Run the following command to create a virtual environment named `venv`:
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment
- **On Windows (Command Prompt)**: `venv\Scripts\activate.bat`
- **On Windows (PowerShell)**: `venv\Scripts\Activate.ps1`
- **On macOS/Linux**: `source venv/bin/activate`

### Step 4: Install Dependencies
Based on the code analysis, your backend uses several external libraries. Run the following command to install them:
```bash
pip install fastapi uvicorn pydantic requests beautifulsoup4 tqdm google-genai python-dotenv
```
*(Optional but recommended: After installing, save them to a file by running `pip freeze > requirements.txt`)*

### Step 5: Run the Backend
You can start your FastAPI server by running:
```bash
uvicorn main:app --reload
```
The backend will run on `http://localhost:8000`.

---

## 3. Frontend Setup
The frontend uses Node.js and npm (or yarn/pnpm). 

### Step 1: Navigate to the frontend directory
Open a new terminal window and run:
```bash
cd frontend
```

### Step 2: Install Dependencies
All the dependencies are already listed in your `package.json` (like React, Vite, Axios, AnimeJS, etc.). Simply run:
```bash
npm install
```

### Step 3: Run the Frontend
Start the Vite development server by running:
```bash
npm run dev
```
The frontend will typically run on `http://localhost:5173`.

---

## 4. Connecting Frontend and Backend
To make your React frontend communicate with your FastAPI backend:

1. **Backend CORS Configuration**:
   Your backend `main.py` already includes a permissive CORS configuration (Allowing all origins `["*"]`). This is great for local development, as it will naturally allow your React app on port 5173 to talk to your FastAPI app on port 8000 without cross-origin errors.

2. **Making API Calls from Frontend**:
   In your frontend, you have `axios` installed. When making requests from your React components, point them to your backend API URL (`http://localhost:8000/api`).
   
   *Example Axios call in your React code:*
   ```javascript
   import axios from 'axios';

   // Start the game or fetch data
   const startGame = async () => {
     try {
       const response = await axios.post('http://localhost:8000/api/start');
       console.log(response.data);
     } catch (error) {
       console.error("Error connecting to backend:", error);
     }
   };
   ```

3. **Best Practice (Environment Variables)**:
   Instead of hardcoding `http://localhost:8000` everywhere in your frontend, create a `.env` file in your `frontend` directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```
   Then in your code, you can use:
   ```javascript
   const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/start`);
   ```
