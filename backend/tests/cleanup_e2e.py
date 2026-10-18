"""Cleanup helper: removes E2E test inscription/cadastro (CPF 52998224725)."""
import requests
B = [l.split("=", 1)[1].strip() for l in open("/app/frontend/.env") if l.startswith("REACT_APP_BACKEND_URL=")][0]
t = requests.post(f"{B}/api/admin/auth/login", json={"username": "donas", "password": "Seinao10@@"}).json()["token"]
h = {"Authorization": f"Bearer {t}"}
for q in ["TEST E2E", "TEST_RESEND"]:
    for i in requests.get(f"{B}/api/admin/inscriptions", params={"q": q}, headers=h).json().get("items", []):
        print("del insc", i["nome"], requests.delete(f"{B}/api/admin/inscriptions/{i['id']}", headers=h).status_code)
for cpf in ["52998224725", "11144477735"]:
    print("del cad", cpf, requests.delete(f"{B}/api/admin/cadastros/{cpf}", headers=h).json())
print("remaining:", [(i["nome"], i.get("cargo_titulo")) for i in requests.get(f"{B}/api/admin/inscriptions", headers=h).json()["items"]])
