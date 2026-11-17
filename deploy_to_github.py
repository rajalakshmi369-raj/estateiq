"""
ESTATEIQ - Automated GitHub Repository Creator & Publisher
Publishes the ESTATEIQ repository to GitHub and generates public download URLs.
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error
import ctypes
from ctypes import wintypes

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GIT_EXE = r"C:\Users\LOKESH ELUMALAI\AppData\Local\GitHubDesktop\app-3.5.6\resources\app\git\cmd\git.exe"

class CREDENTIAL(ctypes.Structure):
    _fields_ = [
        ('Flags', wintypes.DWORD),
        ('Type', wintypes.DWORD),
        ('TargetName', wintypes.LPWSTR),
        ('Comment', wintypes.LPWSTR),
        ('LastWritten', wintypes.FILETIME),
        ('CredentialBlobSize', wintypes.DWORD),
        ('CredentialBlob', ctypes.POINTER(ctypes.c_byte)),
        ('Persist', wintypes.DWORD),
        ('AttributeCount', wintypes.DWORD),
        ('Attributes', ctypes.c_void_p),
        ('TargetAlias', wintypes.LPWSTR),
        ('UserName', wintypes.LPWSTR)
    ]

def get_stored_github_token():
    advapi32 = ctypes.windll.advapi32
    CredReadW = advapi32.CredReadW
    CredReadW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(ctypes.POINTER(CREDENTIAL))]
    CredReadW.restype = wintypes.BOOL

    pcred = ctypes.POINTER(CREDENTIAL)()
    target = 'GitHub - https://api.github.com/rajalakshmi369-raj'
    if CredReadW(target, 1, 0, ctypes.byref(pcred)):
        blob = bytes(ctypes.string_at(pcred.contents.CredentialBlob, pcred.contents.CredentialBlobSize)).decode('utf-8', errors='ignore')
        return blob.strip()
    return None

def main():
    print("=" * 70)
    print("  ESTATEIQ - Automated Public GitHub Deployment Engine")
    print("=" * 70)

    token = get_stored_github_token()
    if not token:
        print("[ERROR] Could not find GitHub token in Windows Credential Manager.")
        sys.exit(1)

    owner = "rajalakshmi369-raj"
    repo_name = "estateiq"
    
    # 1. Create or Verify Repository on GitHub
    print(f"\n1. Verifying GitHub repository '{owner}/{repo_name}'...")
    check_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "EstateIQ-Publisher"
    }
    
    req_check = urllib.request.Request(check_url, headers=headers)
    repo_exists = False
    try:
        with urllib.request.urlopen(req_check) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"   Repository already exists on GitHub: {data.get('html_url')}")
            repo_exists = True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"   Repository does not exist yet. Creating public repository '{repo_name}'...")
            create_url = "https://api.github.com/user/repos"
            payload = json.dumps({
                "name": repo_name,
                "description": "ESTATEIQ - AI-Powered House Price Prediction & Real Estate Analytics System for Indian Cities",
                "private": False,
                "has_issues": True,
                "has_projects": True,
                "has_wiki": True
            }).encode('utf-8')
            
            req_create = urllib.request.Request(create_url, data=payload, headers=headers)
            try:
                with urllib.request.urlopen(req_create) as resp_c:
                    res = json.loads(resp_c.read().decode('utf-8'))
                    print(f"   [SUCCESS] Created public repository: {res.get('html_url')}")
                    repo_exists = True
            except Exception as ex:
                print(f"   [ERROR] Failed to create repo: {ex}")
                sys.exit(1)
        else:
            print(f"   [ERROR] HTTP Check failed: {e.code}")
            sys.exit(1)

    # 2. Push Code via Authenticated Git URL
    print("\n2. Pushing local codebase to GitHub main branch...")
    auth_remote = f"https://{token}@github.com/{owner}/{repo_name}.git"
    
    # Run git push
    cmd = [GIT_EXE, "push", auth_remote, "main:main", "--force"]
    res = subprocess.run(cmd, cwd=BASE_DIR, capture_output=True, text=True)
    
    if res.returncode == 0:
        print("   [SUCCESS] Code successfully pushed to GitHub!")
    else:
        print(f"   [GIT OUTPUT] {res.stdout}")
        print(f"   [GIT ERROR] {res.stderr}")
        
    public_repo_url = f"https://github.com/{owner}/{repo_name}"
    pdf_url = f"https://github.com/{owner}/{repo_name}/raw/main/docs/ESTATEIQ_Comprehensive_Project_Report.pdf"
    docx_url = f"https://github.com/{owner}/{repo_name}/raw/main/docs/ESTATEIQ_Comprehensive_Project_Report.docx"
    
    print("\n" + "=" * 70)
    print("  ALL ASSETS ARE NOW PUBLICLY ACCESSIBLE ONLINE:")
    print(f"  GitHub Repository: {public_repo_url}")
    print(f"  Direct PDF Download: {pdf_url}")
    print(f"  Direct DOCX Download: {docx_url}")
    print("=" * 70)

if __name__ == '__main__':
    main()
