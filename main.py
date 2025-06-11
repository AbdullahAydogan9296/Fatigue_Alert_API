import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

class AlertData(BaseModel):
    user_id: str
    location: str
    message: str
    user_email: EmailStr

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "abdullahaydogan9296@gmail.com"
SENDER_PASSWORD = "bayyozulpfxpolun"

RECEIVER_EMAIL = "sehmusaltas47@gmail.com"

def send_email(alert: AlertData):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECEIVER_EMAIL
        msg["Subject"] = "Yorgunluk Uyarısı"

        body = f"""
Kullanıcı ID: {alert.user_id}
Konum: {alert.location}
Mesaj: {alert.message}
"""

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        # Hata detayını konsola yazdır
        logging.error("E-posta gönderilemedi:", exc_info=True)
        # Daha sonra FastAPI'de 500 dönecek
        raise RuntimeError(f"E-posta gönderilemedi: {str(e)}")

@app.post("/alert/")
async def receive_alert(alert: AlertData):
    try:
        send_email(alert)
        return {"status": "success", "detail": "Alert email sent."}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Fatigue Alert API is running!"}