## DSS Vanthora
DSS Vanthora is a Decision Support System (DSS) designed for route optimization and logistics management. Its primary objective is to reduce travel times, minimize operating costs, and improve logistics efficiency for companies.

## Implemented Features (v1.0)
- Authentication via official Google OAuth2 API
- Frontend -> Streamlit
- Data Processing -> Pandas
- Administrator and administrative roles
- Obtain location coordinates from text
- PDF report generation

## Project Architecture
PROYECTO_P1/
├── .streamlit/
│   └── secrets.toml          
├── credentials/
│   └── oauth2-google.json
├── data_test
|   └── test_01.xlsx 
├── database/
|   └── test_01.xlsx               
├── services/
│   ├── auth.py
|   └── geocoders.py
|   reports/            
├── pages/
│   ├── admin.py  
│   └── client.py   
├── app.py          
├── requirements.txt
└── README.md

## Prerequisites
- Python 3.14+
- Git
- Google Cloud Console

## Execution Instructions
1. Clone the repository:
    git clone https://github.com/jmendez-git/logistics-optimization.git

2. Create and Activate Virtual Environment
    -> Linux / macOS:
        python3 -m venv venv
        source venv/bin/activate

    -> Windows:
        python -m venv venv
        venv\Scripts\activate

3. Install Dependencies
    pip install -r requirements.txt

4. Configure Environment Variables and Credentials
    Create the .streamlit/secrets.toml file in the project root:
        [auth]
        redirect_uri = "http://localhost:8501"
        client_id = "YOUR_CLIENT_ID.apps.googleusercontent.com"
        client_secret = "YOUR_CLIENT_SECRET"

5. streamlit run app.py

