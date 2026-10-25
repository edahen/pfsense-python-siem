# 🛡️ Mini-SIEM Centralizado con Python y pfSense

Sistema SIEM (*Security Information and Event Management*) ligero desarrollado en Python para la recolección, análisis en tiempo real y alertamiento automatizado de eventos de seguridad (syslogs) en un entorno de laboratorio aislado.

## 🏗️ Arquitectura del Laboratorio
- **pfSense Firewall**: Dispositivo perimetral que genera y exporta registros de auditoría mediante Syslog (UDP 514).
- **Kali Linux**: Nodo de monitoreo central que aloja el script receptor, analiza tramas y procesa alertas vía SMTP con multihilos (`threading`).

## 🚀 Funcionalidades Principales
- Recepción activa de paquetes UDP en el puerto estándar 514.
- Motor de análisis léxico con detección de palabras clave críticas (`block`, `deny`, `failed`, `unauthorized`).
- Envío concurrente de alertas por correo electrónico utilizando cifrado TLS con servidores SMTP de Google.
-
