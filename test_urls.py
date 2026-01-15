import requests
from requests.auth import HTTPDigestAuth

# List of possible URLs with different ports and paths
urls_to_try = [
    'https://development.kiosbank.com:4432/auth/Sign-On',
    'http://development.kiosbank.com:4432/auth/Sign-On',  # Try HTTP instead of HTTPS
    'https://development.kiosbank.com:4432/auth/sign-on',
    'http://development.kiosbank.com:4432/auth/sign-on',
]

username = ''
password = ''
payload = {
	"mitra"		: "DJI",
	"accountID"	: "081310307754",
	"merchantID"	: "DJI000651",
    "merchantName": "Sinara Artha Mandiri",
	"counterID"	: "1"
}
headers = {'Content-Type': 'application/json'}

print("Testing URLs with port 4432...\n")

for url in urls_to_try:
    print(f"Trying: {url}")
    try:
        response = requests.post(
            url,
            auth=HTTPDigestAuth(username, password),
            headers=headers,
            json=payload,
            verify=False,
            timeout=10
        )
        
        print(f"  ✓ Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"  ✓✓ SUCCESS! SessionID: {response.json().get('SessionID')}")
            print(f"  Full Response: {response.text}")
            break
        elif response.status_code == 401:
            print(f"  ⚠ Authentication issue (but endpoint exists!)")
            print(f"  Response: {response.text[:200]}")
        else:
            print(f"  Response preview: {response.text[:200]}")
    except requests.exceptions.ConnectionError as e:
        print(f"  ✗ Connection Error: {str(e)[:100]}")
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout")
    except Exception as e:
        print(f"  ✗ Error: {str(e)[:100]}")
    
    print()

print("\n" + "="*60)
print("If all failed, please verify:")
print("1. The correct base URL and port from KIOSBANK team")
print("2. Whether the development server is currently running")
print("3. Your network can access the server (firewall/VPN)")
print("="*60)
