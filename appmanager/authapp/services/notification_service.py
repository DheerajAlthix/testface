import requests
import json
from django.core.mail import EmailMessage

class NotificationService:
    def send_sms(self, phone_number: str, otp: str) -> bool:
        url = "https://restapi.smscountry.com/v0.1/Accounts/y6NxBh5Bk2O734ZDFVcf/SMSes/"
        username = "y6NxBh5Bk2O734ZDFVcf"
        password = "80CRswePCxLycTKBHpB8LruzOiaKzqPy7ObtYc1U"
        
        if not phone_number.startswith('91'):
            phone_number = '91' + phone_number
        
        payload = {
            "Text": f"User Admin login OTP is** - SMSCOU",
            "Number": phone_number,
            "SenderId": "SMSCOU",
            "Tool": "API"
        }
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(
                url, auth=(username, password), headers=headers, data=json.dumps(payload)
            )
            return response.status_code in [200, 201, 202]
        except Exception:
            return False

    def send_email(self, data: dict) -> bool:
        subject = 'Welcome to Althix Pvt Ltd'
        message = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Welcome to Althix Pvt Ltd</title>
            <style>
                body {{ font-family: 'Arial', sans-serif; background-color: #f8f9fa; margin: 0; padding: 0; text-align: center; }}
                .container {{ max-width: 600px; margin: 40px auto; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); text-align: center; }}
                .logo {{ width: 180px; margin-bottom: 20px; display: block; margin-left: auto; margin-right: auto; }}
                h1 {{ color: #1577f3; font-size: 28px; margin-bottom: 10px; }}
                p {{ color: #555; font-size: 16px; line-height: 1.8; margin-bottom: 20px; }}
                .otp {{ font-size: 20px; font-weight: bold; color: #d9534f; background: #f8d7da; padding: 10px; display: inline-block; border-radius: 5px; margin: 10px 0; }}
                .btn {{ display: inline-block; padding: 12px 25px; font-size: 16px; background: #1577f3; color: #fff; text-decoration: none; border-radius: 8px; }}
                .footer {{ margin-top: 30px; font-size: 14px; color: #777; border-top: 1px solid #ddd; padding-top: 15px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <img src="https://your-transparent-logo-url.com/logo.png" alt="Althix Pvt Ltd Logo" class="logo">
                <h1>Welcome, {data['phone_number']}!</h1>
                <p>We are delighted to have you at <strong>Althix Pvt Ltd</strong>.</p>
                <p>Your OTP for verification:</p>
                <div class="otp">{data['otp']}</div>
                <p>Please enter this OTP to complete your registration.</p>
                <a href="https://althix.com" class="btn">Get in Touch</a>
                <p class="footer">Best Regards, <br><strong>Althix Pvt Ltd Team</strong></p>
            </div>
        </body>
        </html>
        """
        email = EmailMessage(
            subject, message, 'badgotidheeraj@gmail.com', [data['phone_number']]
        )
        email.content_subtype = 'html'
        try:
            email.send()
            return True
        except Exception:
            return False