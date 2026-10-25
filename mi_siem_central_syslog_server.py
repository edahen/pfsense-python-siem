import socket
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ==========================================
# CONFIGURACIÓN GENERAL Y CORREO ELECTRONICO
# ==========================================
HOST_ESCUCHA = "0.0.0.0"  # Escucha en todas las interfaces de Kali (redes aisladas y NAT)
PUERTO_SYSLOG = 514       # Puerto estándar de Syslog (UDP)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587           # Puerto para STARTTLS
REMITENTE = "eedenkely@gmail.com"
DESTINATARIO = "eedenkely@gmail.com"

# Reemplaza el texto entre comillas con tu contraseña de aplicación de 16 caracteres de Google
APP_PASSWORD = "mcvujtxmdgqouxup"


# ==========================================
# FUNCIÓN PARA ENVIAR ALERTAS POR CORREO
# ==========================================
def enviar_alerta_correo(ip_origen, log_mensaje):
    """Envia un correo electronico de alerta a traves del servidor SMTP de Gmail."""
    try:
        mensaje = MIMEMultipart()
        mensaje["From"] = REMITENTE
        mensaje["To"] = DESTINATARIO
        mensaje["Subject"] = f"[ALERTA SIEM] Evento crítico detectado en pfSense ({ip_origen})"

        cuerpo = f"""
==================================================
           ALERTA DE SEGURIDAD - SIEM
==================================================
Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Origen del Log: {ip_origen}

Detalle del Evento Registrado:
--------------------------------------------------
{log_mensaje}
--------------------------------------------------

Este es un mensaje automatico generado por tu SIEM central en Kali Linux.
        """
        
        mensaje.attach(MIMEText(cuerpo, "plain"))

        # Conexión al servidor SMTP de Google
        servidor = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        servidor.starttls()  # Activar cifrado TLS
        servidor.login(REMITENTE, APP_PASSWORD)
        servidor.sendmail(REMITENTE, DESTINATARIO, mensaje.as_string())
        servidor.quit()
        
        print(f"\n[+] [SMTP] ¡Alerta por correo enviada con éxito a {DESTINATARIO}!")
    
    except Exception as e:
        print(f"\n[-] [SMTP] Error al enviar el correo de alerta: {e}")


# ==========================================
# FUNCIÓN ANALIZADORA DE LOGS (REGLAS DE SIEM)
# ==========================================
def analizar_registro(ip_origen, log_texto):
    """Analiza el contenido del log y decide si dispara una alerta."""
    log_lower = log_texto.lower()
    
    # Palabras clave críticas que activarán el envío de correo
    palabras_clave = ["block", "blocked", "deny", "denied", "failed", "unauthorized", "login error"]
    
    for palabra in palabras_clave:
        if palabra in log_lower:
            print(f"\n[!] [REGLA ACTIVADA] Evento sospechoso ('{palabra}') detectado desde {ip_origen}.")
            
            # Lanzamos el envío del correo en un hilo secundario para no detener la recepción de logs
            hilo_correo = threading.Thread(target=enviar_alerta_correo, args=(ip_origen, log_texto))
            hilo_correo.start()
            break


# ==========================================
# RECEPTOR SYSLOG UDP
# ==========================================
def iniciar_siem():
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        sock.bind((HOST_ESCUCHA, PUERTO_SYSLOG))
        print("==================================================")
        print("    SIEM CENTRALIZADO EN KALI LINUX ACTIVADO      ")
        print("==================================================")
        print(f"[*] Escuchando Syslogs UDP en el puerto {PUERTO_SYSLOG}...")
        print(f"[*] Alertas de correo dirigidas a: {DESTINATARIO}")
        print("--------------------------------------------------\n")
    except Exception as e:
        print(f"[-] Error al iniciar el servidor en el puerto {PUERTO_SYSLOG}: {e}")
        print("[-] Recuerda ejecutar el script con permisos de root (sudo).")
        return

    while True:
        try:
            datos, direccion = sock.recvfrom(4096)
            ip_origen = direccion[0]
            log_texto = datos.decode("utf-8", errors="replace").strip()
            
            # Muestra el log en pantalla en tiempo real
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{ip_origen}] {log_texto}")
            
            # Analiza si el log cumple con alguna regla de alerta
            analizar_registro(ip_origen, log_texto)
            
        except KeyboardInterrupt:
            print("\n[*] Deteniendo el servidor SIEM...")
            break
        except Exception as e:
            print(f"[-] Error en recepción de datos: {e}")

    sock.close()

if __name__ == "__main__":
    iniciar_siem()
