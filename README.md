# 📄 AI Resume Analyzer

AI-powered Resume Analyzer built with **Streamlit + CrewAI + LangChain**.  
This tool parses resumes, extracts job description (JD) keywords, calculates an **ATS score**, and suggests targeted **resume improvements**.

👉 Live Demo: `https://resume.sabarinextgen.dev`

---

## 🚀 Features
- Upload your **Resume (PDF)**.
- Paste a **Job Description**.
- AI parses the resume into structured JSON (Name, Skills, Education, Work Experience).
- Extracts **keywords & skills** from the JD.
- Provides an **ATS score (0–100)** with missing keywords & match percentage.
- Suggests **resume improvements** tailored to the JD.

---

## 🛠️ Tech Stack
- [Python 3.11+](https://www.python.org/)
- [Streamlit](https://streamlit.io/) – Web UI
- [CrewAI](https://github.com/joaomdmoura/crewai) – Multi-agent orchestration
- [LangChain](https://www.langchain.com/) – LLM integration
- [LiteLLM](https://github.com/BerriAI/litellm) – Model wrapper
- [PyPDF2](https://pypi.org/project/PyPDF2/) – PDF text extraction
- [dotenv](https://pypi.org/project/python-dotenv/) – Environment variables

---

## 📦 Installation (Local Development)

1. **Clone the repo**
   ```bash
   git clone https://github.com/Sabarivenkatesh3/ai-resume-analyzer.git
   cd ai-resume-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux/Mac
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up API key**  
   Create a `.env` file in the root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Run the app**
   ```bash
   streamlit run app.py
   ```
   Open browser → [http://localhost:8501](http://localhost:8501)

---

## 🐳 Run with Docker

1. **Build image**
   ```bash
   docker build -t ai-resume-analyzer .
   ```

2. **Run container**
   ```bash
   docker run -d -p 8501:8501 --env-file .env ai-resume-analyzer
   ```

3. Open browser → [http://localhost:8501](http://localhost:8501)

---

## 🌍 Hosting with Cloudflare Tunnel (Custom Domain)

If you want to host on a subdomain (e.g., `resume.sabarinextgen.dev`):

1. Install [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/).
2. Create/configure tunnel (`config.yml`):
   ```yaml
   tunnel: <your-tunnel-id>
   credentials-file: C:\Users\<you>\.cloudflared\<your-tunnel-id>.json

   ingress:
     - hostname: resume.sabarinextgen.dev
       service: http://localhost:8501
     - service: http_status:404
   ```
3. Map DNS:
   ```bash
   cloudflared tunnel route dns <your-tunnel-name> resume.sabarinextgen.dev
   ```

4. Run tunnel:
   ```bash
   cloudflared tunnel run <your-tunnel-name>
   ```

Now your app is accessible at  
👉 `https://resume.sabarinextgen.dev`

---

## 📂 Project Structure
```
ai-resume-analyzer/
│── app.py               # Streamlit UI
│── agents.py            # CrewAI agents
│── resume_workflow.py   # Workflow orchestration
│── requirements.txt     # Python dependencies
│── Dockerfile           # For containerization
│── docker-compose.yml   # Optional multi-service setup
│── .env.example         # Example environment file
│── .gitignore
```

---

## 📝 Example Usage
1. Upload `resume.pdf`
2. Paste job description
3. Click **Analyze Resume**
4. Get:
   - ✅ Parsed Resume JSON
   - ✅ JD Keywords JSON
   - ✅ ATS Score
   - ✅ Resume Improvement Suggestions

---

## 🤝 Contributing
PRs and suggestions are welcome!  
Fork this repo → create a new branch → make changes → submit a PR.

---

## 📜 License
This project is open-source under the **MIT License**.

---

👨‍💻 Developed by **[Sabari Venkatesh](https://github.com/Sabarivenkatesh3)**
