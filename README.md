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
## 🧪 Pruebas y Validación del Sistema

Para verificar que el script reacciona correctamente ante eventos maliciosos o bloqueos perimetrales, se realizaron pruebas simulando tráfico de registros (*syslogs*) hacia el nodo receptor mediante el protocolo **UDP** (*User Datagram Protocol* / Protocolo de Datagramas de Usuario) en el puerto `514`.

### 1. Ejemplo de Registro (*Log*) Simulado
Cuando un cortafuegos (como **pfSense**) bloquea un paquete entrante, genera una trama similar a esta:

```text
Dec 25 10:15:30 firewall filterlog[79]: 4,,1000000103,match,block,in,on em0,ipv4,tcp,192.168.1.100,203.0.113.50,45210,80,0,S,2456789,,64,,SYN

### 2. Respuesta en la Terminal del SIEM (*Security Information and Event Management* / Gestión de Información y Eventos de Seguridad)
Al recibir la trama anterior, el script centralizado en **Kali Linux** procesa el mensaje mediante su motor léxico, identifica la palabra clave `block` y genera la siguiente traza en consola junto con la dirección **IP** (*Internet Protocol* / Protocolo de Internet) de origen:

```text
==================================================
    SIEM CENTRALIZADO EN KALI LINUX ACTIVADO      
==================================================
[*] Escuchando Syslogs UDP en el puerto 514...
--------------------------------------------------

 [192.168.1.100] Dec 25 10:15:30 firewall filterlog[79]: ... block ...
[!] [REGLA ACTIVADA] Evento sospechoso ('block') detectado desde 192.168.1.100.
[+] [SMTP] ¡Alerta por correo enviada con éxito a tucorreo@gmail.com!

### 3. Alerta Automatizada por Correo Electrónico
De manera simultánea, el sistema utiliza **SMTP** (*Simple Mail Transfer Protocol* / Protocolo Simple de Transferencia de Correo) para enviar un reporte detallado con la fecha, la hora exacta y el contenido íntegro del evento detectado.

