# Kiosbank Authentication & Sign-On Module

## Project Overview

**Subject:** Create a Robust Kiosbank Authentication & Sign-On Module (Digest Auth Implementation)

**Context:** Implementation of a secure "Sign On" mechanism for a third-party payment gateway called Kiosbank. The documentation specifies a custom Digest Authentication flow using MD5.

---

## Goal

Create a reusable function/class that handles the full authentication handshake automatically:

1. Initiate a request to trigger the server challenge
2. Capture the nonce and other headers from the 401 response
3. Calculate the MD5 Authorization header manually (as per specific formulas)
4. Resend the request with the payload to get the sessionID

---

## Technical Specifications

### Endpoints

- **URL:** `[Base_URL]/auth/sign-on`
- **Method:** `POST` (for the final payload transmission)

---

## Challenge-Response Logic (The Workflow)

### Step A: The Probe

Send a request to the endpoint. The server will reply with **HTTP 401 Unauthorized** and a `WWW-Authenticate` header containing:

- `realm`
- `qop`
- `nonce`
- `opaque`

### Step B: The Calculation

Parse those values and generate client-side values:

- **`cnonce`** (Client Nonce): a random unique string
- **`nc`** (Nonce Count): usually `"00000001"`

### Step C: The Formulas

Calculate the response string using MD5:

```
HA1 = MD5(username + ":" + realm + ":" + password)
HA2 = MD5(method + ":" + uri)
response = MD5(HA1 + ":" + nonce + ":" + nc + ":" + cnonce + ":" + qop + ":" + HA2)
```

### Step D: The Execution

Construct the Authorization header string:

**Format:**
```
Digest username="...", realm="...", nonce="...", uri="...", qop=..., nc=..., cnonce="...", response="...", opaque="..."
```

### Step E: Final Request

Send the POST request again with:

- The generated `Authorization` header
- Header `Content-Type: application/json`
- **JSON Body:**
  ```json
  {
    "mitra": "...",
    "accountID": "...",
    "merchantID": "...",
    "merchantName": "...",
    "counterID": "..."
  }
  ```

---

## Implementation Example (PHP/Laravel)

### KiosbankService Class

Complete implementation of the Digest Authentication flow in PHP using Laravel:

```php
<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;

class KiosbankService
{
    private $baseUrl;
    private $username;
    private $password;

    public function __construct()
    {
        // Sebaiknya ambil dari .env
        $this->baseUrl = 'https://development.kiosbank.com'; 
        $this->username = 'testUser'; // Ganti dengan user asli
        $this->password = 'testPass'; // Ganti dengan pass asli
    }

    public function getSessionId()
    {
        $uri = '/auth/sign-on';
        $url = $this->baseUrl . $uri;
        
        // Data Payload sesuai gambar sign-on.png
        $payload = [
            "mitra" => "DJI",
            "accountID" => "testAccount",
            "merchantID" => "TST956124",
            "merchantName" => "PT.Testing",
            "counterID" => "1"
        ];

        // --- LANGKAH 1: Request Pancingan (Probe) ---
        // Kita harap dapat 401 untuk ambil Nonce
        $response = Http::post($url, $payload);

        if ($response->status() !== 401) {
            // Jika tiba-tiba 200 (mungkin auth mati/cache), langsung return
            return $response->json()['sessionID'] ?? null;
        }

        // --- LANGKAH 2: Ambil Bahan dari Header Server ---
        $authHeader = $response->header('WWW-Authenticate');
        
        // Parsing Header (Mengambil nilai realm, nonce, qop, opaque)
        // Format header biasanya: Digest realm="...", nonce="...", ...
        preg_match('/realm="([^"]+)"/', $authHeader, $realm);
        preg_match('/nonce="([^"]+)"/', $authHeader, $nonce);
        preg_match('/qop="([^"]+)"/', $authHeader, $qop);
        preg_match('/opaque="([^"]+)"/', $authHeader, $opaque);

        $data = [
            'realm'  => $realm[1] ?? '',
            'nonce'  => $nonce[1] ?? '',
            'qop'    => $qop[1] ?? 'auth',
            'opaque' => $opaque[1] ?? '',
            'nc'     => '00000001', // Nonce Count (biasanya mulai dari 1)
            'cnonce' => uniqid(),   // Client Nonce (acak dari kita)
            'uri'    => $uri,
            'method' => 'POST'
        ];

        // --- LANGKAH 3: Kalkulasi Rumus MD5 (Sesuai Gambar) ---
        
        // HA1 = MD5(username:realm:password)
        $ha1 = md5("{$this->username}:{$data['realm']}:{$this->password}");
        
        // HA2 = MD5(method:uri)
        $ha2 = md5("{$data['method']}:{$data['uri']}");
        
        // Response = MD5(HA1:nonce:nc:cnonce:qop:HA2)
        $responseStr = md5("{$ha1}:{$data['nonce']}:{$data['nc']}:{$data['cnonce']}:{$data['qop']}:{$ha2}");

        // --- LANGKAH 4: Susun Header Authorization ---
        $digestHeader = sprintf(
            'Digest username="%s", realm="%s", nonce="%s", uri="%s", qop=%s, nc=%s, cnonce="%s", response="%s", opaque="%s"',
            $this->username, $data['realm'], $data['nonce'], $data['uri'], 
            $data['qop'], $data['nc'], $data['cnonce'], $responseStr, $data['opaque']
        );

        // --- LANGKAH 5: Request Ulang dengan Header ---
        $finalResponse = Http::withHeaders([
            'Authorization' => $digestHeader,
            'Content-Type'  => 'application/json'
        ])->post($url, $payload);

        if ($finalResponse->successful()) {
            return $finalResponse->json()['sessionID'];
        }

        // Handle error
        throw new \Exception("Gagal Sign On: " . $finalResponse->body());
    }
}
```

### Key Features of This Implementation:

1. **Two-Step Request Process:**
   - First request triggers 401 response with authentication challenge
   - Second request includes calculated Digest authentication header

2. **Header Parsing:**
   - Uses regex to extract `realm`, `nonce`, `qop`, and `opaque` from `WWW-Authenticate` header
   - Generates client-side `cnonce` and `nc` values

3. **MD5 Calculation:**
   - Follows exact formula: `HA1`, `HA2`, and final `response` hash
   - Matches Kiosbank's specific Digest Auth requirements

4. **Error Handling:**
   - Handles unexpected 200 responses (cached auth)
   - Throws exception on authentication failure
   - Returns sessionID on success

### Usage Example:

```php
// In a Controller
use App\Services\KiosbankService;

public function authenticate()
{
    $kiosbank = new KiosbankService();
    
    try {
        $sessionId = $kiosbank->getSessionId();
        return response()->json(['sessionID' => $sessionId]);
    } catch (\Exception $e) {
        return response()->json(['error' => $e->getMessage()], 500);
    }
}
```

---

## Implementation Example (Python)

### Standalone Function Implementation

Complete implementation using Python's `requests` library with manual Digest Auth construction:

```python
import requests
import hashlib
import re
import uuid

def get_kiosbank_session():
    # Konfigurasi
    base_url = "https://development.kiosbank.com"
    endpoint = "/auth/sign-on"
    url = base_url + endpoint
    username = "testUser"
    password = "testPass"

    # Payload Body
    payload = {
        "mitra": "DJI",
        "accountID": "testAccount",
        "merchantID": "TST956124",
        "merchantName": "PT.Testing",
        "counterID": "1"
    }

    # --- LANGKAH 1: Request Pancingan ---
    # Kirim request polos untuk memancing error 401
    r1 = requests.post(url, json=payload)

    if r1.status_code != 401:
        print("Server tidak meminta otentikasi (mungkin sudah login?)")
        return r1.json().get("sessionID")

    # --- LANGKAH 2: Parse Header ---
    auth_header = r1.headers.get("WWW-Authenticate")
    
    # Helper regex untuk ambil value di antara tanda kutip
    def parse(key):
        match = re.search(f'{key}="([^"]+)"', auth_header)
        if not match: # Kadang ada yg tidak pakai tanda kutip (misal qop)
             match = re.search(f'{key}=([^, ]+)', auth_header)
        return match.group(1) if match else None

    realm = parse("realm")
    nonce = parse("nonce")
    qop = parse("qop") or "auth"
    opaque = parse("opaque")
    
    # Parameter Client
    nc = "00000001"
    cnonce = uuid.uuid4().hex[:16] # Random string unik

    # --- LANGKAH 3: Hitung MD5 ---
    def md5(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    # HA1: username:realm:password
    ha1 = md5(f"{username}:{realm}:{password}")
    
    # HA2: method:uri (Method harus sama dengan request asli yaitu POST)
    ha2 = md5(f"POST:{endpoint}")
    
    # Response: HA1:nonce:nc:cnonce:qop:HA2
    response_str = md5(f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}")

    # --- LANGKAH 4: Susun Header ---
    # Perhatikan spasi dan koma sesuai standar Digest
    auth_header_value = (
        f'Digest username="{username}", realm="{realm}", nonce="{nonce}", '
        f'uri="{endpoint}", qop={qop}, nc={nc}, cnonce="{cnonce}", '
        f'response="{response_str}", opaque="{opaque}"'
    )

    # --- LANGKAH 5: Eksekusi Final ---
    headers = {
        "Authorization": auth_header_value,
        "Content-Type": "application/json"
    }

    r2 = requests.post(url, json=payload, headers=headers)

    if r2.status_code == 200:
        data = r2.json()
        print(f"Sukses! Session ID: {data.get('sessionID')}")
        return data.get('sessionID')
    else:
        print(f"Gagal: {r2.status_code} - {r2.text}")
        return None

# Cara Menjalankan
# session_id = get_kiosbank_session()
```

### Key Features of This Implementation:

1. **Flexible Header Parsing:**
   - Uses regex to handle both quoted and unquoted values
   - Fallback mechanism for optional parameters
   - Handles variations in server response format

2. **Clean MD5 Helper:**
   - Reusable `md5()` function for all hash calculations
   - Proper UTF-8 encoding
   - Follows exact Digest Auth formula

3. **Robust Error Handling:**
   - Checks for unexpected 200 responses (cached sessions)
   - Detailed error messages with status codes
   - Returns `None` on failure for easy error checking

4. **UUID-based Client Nonce:**
   - Uses `uuid.uuid4()` for cryptographically random cnonce
   - Ensures uniqueness for each authentication attempt

### Usage Example:

```python
# Simple usage
session_id = get_kiosbank_session()

if session_id:
    print(f"Authentication successful: {session_id}")
    # Proceed with authenticated requests
else:
    print("Authentication failed")
```

### Integration with Environment Variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

def get_kiosbank_session():
    # Load from environment
    base_url = os.getenv("KIOSBANK_BASE_URL", "https://development.kiosbank.com")
    username = os.getenv("KIOSBANK_USERNAME")
    password = os.getenv("KIOSBANK_PASSWORD")
    
    # ... rest of the implementation
```

---

## Required Output

### Implementation Requirements

- **Language:** Python
- **Structure:** Clean, modular structure (Service class or Helper function)
- **Authentication Method:** Manual construction of the header string
  - ⚠️ **Crucial:** Do not rely solely on a standard "HTTP Digest Auth" library if it doesn't allow customizing specific fields (like `nc` or `cnonce`)
  - Legacy banking APIs are often strict - prefer manual construction to match the logic above
- **Error Handling:**
  - Handle cases where Step A doesn't return a 401
  - Handle errors returned in Step E

---

## Testing Data

### Placeholders

Use environment variables for sensitive data:

- `USERNAME`
- `PASSWORD`
- `BASE_URL`

### Payload Example

```json
{
  "mitra": "DJI",
  "accountID": "testAccount",
  "merchantID": "...",
  "merchantName": "...",
  "counterID": "..."
}
```

---

## ⚠️ Poin Kritis untuk Diperhatikan

### 1. URI vs URL dalam Hash Calculation

**PENTING:** Pada rumus MD5 HA2, variabel yang digunakan adalah **URI** (path-nya saja), **BUKAN URL lengkap**.

✅ **BENAR:**
```python
ha2 = md5("POST:/auth/sign-on")
```

❌ **SALAH:**
```python
ha2 = md5("POST:https://development.kiosbank.com/auth/sign-on")
```

> **Catatan:** Jika Anda memasukkan `https://` ke dalam rumus hash, server akan menolak dengan error **Invalid Signature**.

### 2. Urutan dan Format Parameter Authorization Header

Pastikan urutan penyusunan string di dalam header `Authorization` rapi dan mengikuti format standar Digest Auth.

**Format yang Benar:**
```
Digest username="...", realm="...", nonce="...", uri="...", qop=..., nc=..., cnonce="...", response="...", opaque="..."
```

**Poin Penting:**
- Gunakan format `key="value"` dengan tanda kutip untuk string values
- Pisahkan setiap parameter dengan koma dan spasi (`, `)
- Parameter `qop` dan `nc` biasanya tidak menggunakan tanda kutip
- Meskipun urutan key tidak wajib baku, konsistensi format **sangat penting**

### 3. HTTP Method Harus Sesuai

Pastikan method di rumus HA2 sesuai dengan HTTP method yang digunakan pada request.

**Untuk Sign-On (POST):**
```python
ha2 = md5("POST:/auth/sign-on")
```

**Untuk Cek Saldo (GET):**
```python
ha2 = md5("GET:/balance/check")
```

> **Catatan:** Method harus **UPPERCASE** dan **EXACT MATCH** dengan request yang dikirim. Jika tidak sesuai, autentikasi akan gagal.

### 4. Encoding dan Character Set

- Semua string harus di-encode dalam **UTF-8** sebelum di-hash dengan MD5
- Pastikan tidak ada whitespace atau karakter tersembunyi dalam string yang di-hash
- Hash hasil harus dalam format **hexadecimal lowercase**

### 5. Nonce dan Opaque Values

- **Nonce** dari server harus digunakan **persis seperti yang diterima**
- **Opaque** value (jika ada) juga harus dikembalikan **tanpa modifikasi**
- Jangan menambahkan atau menghilangkan karakter apapun dari nilai-nilai ini

---

## Implementation Status

- ✅ Core authentication module implemented
- ✅ Environment configuration setup
- ✅ Security documentation
- ✅ VPS Gateway solutions
- 🔄 GUI tools for easier management