#!/usr/bin/env python3
# AUMC FINAL - RENE RAMIREZ SANCHES - VALIDACION 9 9 9 OK
# SOLO USAR EN REPOS CON PERMISO: wrongsecrets, juice-shop, DVWA, o tus propios archivos
import re, os, datetime

REGLAS = {
  "AWS_KEY": (r"AKIA[0-9A-Z]{16}", "CRITICO", 1500, "Clave AWS expuesta - Pagan $1500 en HackerOne"),
  "GITHUB_TOKEN": (r"ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{80,}", "CRITICO", 1000, "Token GitHub - Pagan $1000"),
  "PRIVATE_KEY": (r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----", "CRITICO", 2000, "Llave privada - Pagan $2000"),
  "PASSWORD_HARDCODED": (r"password\s*[:=]\s*['\"][^\s'\"]{6,}['\"]", "ALTO", 500, "Password en codigo - Pagan $500"),
  "API_KEY": (r"(?i)api_key\s*[:=]\s*['\"][a-zA-Z0-9_\-]{20,}['\"]", "ALTO", 750, "API Key - Pagan $750"),
}

def escanear(ruta):
    hallazgos=[]
    total=0
    for root, dirs, files in os.walk(ruta):
        # Ignora.git para no trabarse
        if ".git" in root: continue
        for f in files:
            if not f.endswith((".java",".py",".js",".env",".yml",".yaml",".json",".properties")):
                continue
            path=os.path.join(root,f)
            try:
                with open(path,'r',errors='ignore',encoding='utf-8') as fd:
                    for num, line in enumerate(fd,1):
                        for nombre,(pat,sev,precio,desc) in REGLAS.items():
                            if re.search(pat, line):
                                hallazgos.append((nombre,sev,precio,desc,path,num,line.strip()[:120]))
                                total+=precio
            except: pass
    return hallazgos, total

# === INICIO ===
print("==========================================")
print(" AUMC FINAL - RENE RAMIREZ SANCHES")
print(" VALIDACION 18 27 18 => 9 9 9 OK")
print(" MODO LEGAL: Solo repos con permiso")
print("==========================================\n")

ruta = "." # escanea tu carpeta actual
if os.path.exists("wrongsecrets"):
    ruta="wrongsecrets"

hallazgos, total = escanear(ruta)

for nombre,sev,precio,desc,path,num,code in hallazgos:
    print(f"[{sev}] ${precio} - {nombre} en {path}:{num}")
    print(f" -> {code}")
    print(f" {desc}\n")

print(f"--- RESUMEN FINAL ---")
print(f"Archivos escaneados con permiso: {ruta}")
print(f"Fallos encontrados: {len(hallazgos)}")
print(f"Valor estimado si fuera bug bounty real: ${total} USD")
print(f"VALIDACION 9 9 9 OK - RENE RAMIREZ SANCHES")

# Reporte
nombre_reporte=f"Reporte_FINAL_{datetime.datetime.now().strftime('%d%m_%H%M')}.md"
with open(nombre_reporte,"w",encoding='utf-8') as out:
    out.write(f"# AUMC - Reporte Final - {len(hallazgos)} hallazgos\n")
    out.write(f"**Autor: RENE RAMIREZ SANCHES - 9 9 9 OK**\n\n")
    out.write(f"Valor potencial: ${total} USD\n\n")
    for h in hallazgos:
        out.write(f"### {h[0]} - ${h[2]}\nArchivo: {h[4]}:{h[5]}\n```\n{h[6]}\n```\n{h[3]}\n\n")

print(f"\nReporte guardado: {nombre_reporte}")
