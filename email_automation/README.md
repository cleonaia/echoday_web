# Echoday Email Automation System

Sistema completo de automatización para campañas masivas de outreach digital dirigidas a empresas locales en Sabadell, Barcelona y alrededores.

## 🎯 Descripción del Sistema

Este sistema automatiza completamente el proceso de captación de clientes para los servicios digitales de Echoday, desde la identificación de empresas potenciales hasta el envío de propuestas personalizadas y el seguimiento de respuestas.

### Características Principales

✅ **Scraping de Datos Reales**: Extrae información de empresas locales desde Google Maps, LinkedIn y directorios públicos  
✅ **Análisis de Inteligencia de Negocio**: Evalúa la presencia digital y necesidades específicas de cada empresa  
✅ **Emails Personalizados**: Genera propuestas de 400-600 palabras en español/catalán adaptadas al sector  
✅ **Envío Automatizado**: Gestiona lotes de 200-2000 emails diarios con múltiples proveedores  
✅ **Cumplimiento RGPD**: Incluye disclaimers legales y gestión de bajas  
✅ **Reportes Diarios**: Métricas detalladas por sector y área geográfica  
✅ **Sistema Anti-Repetición**: Evita contactos duplicados automáticamente  

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- Cuenta de correo SMTP (Gmail recomendado)
- APIs opcionales: Google Maps, LinkedIn, Mailchimp, Instantly

### Instalación

1. **Clonar el repositorio**:
```bash
git clone https://github.com/cleonaia/echoday_web.git
cd echoday_web/email_automation
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**:
```bash
# Crear archivo .env
cp .env.example .env

# Editar las variables de entorno
SMTP_PASSWORD=tu_password_email
GOOGLE_MAPS_API_KEY=tu_api_key_opcional
LINKEDIN_API_KEY=tu_api_key_opcional
MAILCHIMP_API_KEY=tu_api_key_opcional
INSTANTLY_API_KEY=tu_api_key_opcional
```

4. **Configurar datos de contacto** (en `config.py`):
```python
# Leonardo's contact information
name: str = "Leonardo"
email: str = "contact@echoday.tech"
whatsapp: str = "+34 643 032 807"
website: str = "https://www.echoday.tech"
```

## 📋 Estructura del Proyecto

```
email_automation/
├── main.py                    # Script principal de ejecución
├── config.py                  # Configuración y parámetros del sistema
├── data_scraper.py           # Módulo de scraping de datos empresariales
├── business_intelligence.py  # Análisis de presencia digital
├── email_templates.py        # Generación de emails personalizados
├── send_engine.py            # Motor de envío y gestión de campañas
├── requirements.txt          # Dependencias de Python
├── README.md                 # Este archivo
└── data/                     # Directorio de datos y logs
    ├── outreach_log.db       # Base de datos SQLite
    └── automation_YYYYMMDD.log # Logs diarios
```

## 🎮 Uso del Sistema

### Modo Completo (Recomendado)
Ejecuta todo el workflow: scraping → análisis → emails → reportes

```bash
python main.py --mode full --max-emails 100
```

### Modos Individuales

**Solo scraping de datos**:
```bash
python main.py --mode scrape
```

**Solo análisis de empresas**:
```bash
python main.py --mode analyze
```

**Solo campaña de emails**:
```bash
python main.py --mode email --max-emails 50 --min-priority 60
```

**Follow-ups automáticos**:
```bash
python main.py --mode followup
```

**Generar reporte diario**:
```bash
python main.py --mode report
```

**Probar plantillas de email**:
```bash
python main.py --mode test --business-name "Restaurante Ca la Maria" --sector restaurants
```

**Programador automático**:
```bash
python main.py --mode schedule
```

### Parámetros Avanzados

- `--max-emails N`: Máximo de emails por campaña (default: 50)
- `--min-priority N`: Puntuación mínima de prioridad (0-100, default: 40)
- `--verbose`: Logging detallado para debugging
- `--business-name "Nombre"`: Nombre de empresa para testing
- `--sector sector`: Sector específico (restaurants, clinics, academies, etc.)

## 🎯 Sectores y Áreas Objetivo

### Sectores Configurados
- **Restaurantes**: Reservas online, pedidos a domicilio, presencia digital
- **Clínicas**: Sistema de citas, portal del paciente, telemedicina
- **Academias**: Plataforma e-learning, gestión de estudiantes
- **Construcción**: Portfolio digital, presupuestador online
- **Comercio**: Tienda online, gestión de inventario
- **Servicios**: CRM, automatización de procesos

### Áreas Geográficas
- Sabadell y comarca
- Barcelona ciudad
- Terrassa, Rubí, Sant Cugat
- Granollers, Manresa
- Vallès Oriental y Occidental

## 📧 Plantillas de Email

### Tipos de Email Generados

1. **Alta Oportunidad**: Para empresas sin presencia digital
2. **Mejora**: Para empresas con presencia básica
3. **Sector Específico**: Propuestas adaptadas al sector
4. **Follow-ups**: Secuencia de seguimiento automático

### Personalización Incluida

- Nombre de empresa y ubicación
- Análisis específico de su presencia digital actual
- Dolor points identificados automáticamente
- Propuestas técnicas realistas con presupuestos
- Casos de éxito similares
- Call-to-action personalizado

### Ejemplo de Email Generado

```
Subject: 🚀 Restaurante Ca la Maria: Multiplica tu facturación con presencia digital

Estimado/a responsable de Restaurante Ca la Maria,

Me llamo Leonardo y dirijo Echoday, una empresa especializada en transformación 
digital para negocios locales en Sabadell y alrededores.

He analizado la presencia digital de Restaurante Ca la Maria y he identificado 
una oportunidad extraordinaria para multiplicar vuestro crecimiento...

[Análisis personalizado de 400-600 palabras]

Leonardo
Fundador & CEO - Echoday
📧 contact@echoday.tech
📱 +34 643 032 807
🌐 www.echoday.tech
```

## 📊 Sistema de Análisis e Inteligencia

### Métricas de Evaluación Digital

- **Puntuación de Sitio Web** (0-10): Calidad, SEO, mobile-friendly
- **Presencia en Redes Sociales** (0-10): Facebook, Instagram, LinkedIn
- **Puntuación Google** (0-10): Reviews, Google My Business
- **Madurez Digital**: Básica, Intermedia, Avanzada
- **Puntuación de Prioridad** (0-100): Likelihood de conversión

### Identificación Automática de Pain Points

- Ausencia de sitio web profesional
- Sitio no responsivo para móviles
- Baja visibilidad en buscadores
- Sin sistema de reservas/pedidos online
- Presencia limitada en redes sociales
- Falta de herramientas de gestión digital

## 🔄 Automatización y Programación

### Programa Diario Automático

- **09:00**: Campaña principal de outreach (100 emails)
- **14:00**: Follow-ups a empresas contactadas hace 7-14 días
- **18:00**: Generación y envío de reporte diario

### Límites y Controles

- **Límite diario**: 500 emails máximo
- **Lotes**: 50 emails por lote con pausas de 60 segundos
- **Delays**: 5-15 segundos aleatorios entre emails
- **Anti-spam**: Rotación de servidores y user agents
- **RGPD**: Gestión automática de bajas y disclaimers

## 📈 Reportes y Métricas

### Reporte Diario Incluye

```
📊 ECHODAY DAILY REPORT - 2024-01-15
====================================
📧 Total emails sent: 127
✅ Successful: 119
❌ Failed: 8
🔄 Bounced: 3
👀 Opened: 42
💬 Responded: 7
📈 Success rate: 93.7%
🏢 Businesses contacted: 119
====================================
```

### Métricas Segmentadas

- Por sector (restaurantes, clínicas, etc.)
- Por área geográfica (Sabadell, Barcelona, etc.)
- Por tipo de email (outreach, follow-up)
- Tasas de apertura y respuesta
- ROI estimado por campaña

## 🛡️ Cumplimiento Legal y Ético

### RGPD y Privacidad

- ✅ Emails dirigidos solo a empresas con actividad pública
- ✅ Disclaimer legal en cada email
- ✅ Sistema de baja automático
- ✅ Retención de datos limitada (2 años)
- ✅ No almacenamiento de datos personales sensibles

### Práticas Anti-Spam

- ✅ Límites de envío conservadores
- ✅ Contenido personalizado y relevante
- ✅ Headers SMTP correctos
- ✅ Lista de supresión automática
- ✅ Monitoring de reputation del dominio

## 🔧 Configuración Avanzada

### Múltiples Proveedores de Email

```python
EMAIL_SERVICES = {
    "smtp": {"enabled": True},           # Gmail/SMTP básico
    "mailchimp": {"enabled": False},     # Mailchimp Transactional
    "instantly": {"enabled": False}      # Instantly.ai
}
```

### Personalización de Sectores

```python
TARGET_SECTORS = {
    "tu_sector": {
        "keywords": ["palabra1", "palabra2"],
        "digital_needs": ["necesidad1", "necesidad2"],
        "avg_budget": "1500-3000€",
        "language_preference": "es"
    }
}
```

### Configuración de Areas

```python
TARGET_AREAS = [
    "Tu Ciudad, Provincia, Spain",
    "Otra Ciudad, Provincia, Spain"
]
```

## 🚨 Troubleshooting

### Problemas Comunes

**Error de autenticación SMTP**:
```bash
# Verificar credenciales en .env
# Para Gmail, usar "App Password" no la contraseña normal
```

**Rate limiting en APIs**:
```bash
# Aumentar delays en config.py
delay_between_batches: int = 120  # seconds
```

**Base de datos bloqueada**:
```bash
# Verificar que no hay múltiples instancias ejecutándose
ps aux | grep python
```

**Emails marcados como spam**:
```bash
# Reducir volumen diario y mejorar reputación
daily_limit: int = 200
```

### Logs y Debugging

Los logs se guardan en `email_automation/data/automation_YYYYMMDD.log`

Activar logging verbose:
```bash
python main.py --mode full --verbose
```

## 🎯 Resultados Esperados

### Métricas de Éxito

- **Tasa de entrega**: >95%
- **Tasa de apertura**: 25-35%
- **Tasa de respuesta**: 3-8%
- **Conversión a reunión**: 1-3%
- **Conversión a cliente**: 0.5-1.5%

### ROI Proyectado

Con 500 emails/día durante un mes:
- Emails enviados: 15,000
- Respuestas esperadas: 450-1,200
- Reuniones: 150-450
- Clientes nuevos: 75-225
- Facturación mensual: 15,000-45,000€

## 📞 Soporte y Contacto

Para soporte técnico o personalización del sistema:

**Leonardo - Echoday**  
📧 contact@echoday.tech  
📱 +34 643 032 807  
🌐 www.echoday.tech  

### Servicios de Personalización

- Configuración inicial completa
- Integración con CRM existente
- Plantillas de email personalizadas
- Análisis de resultados y optimización
- Entrenamiento del equipo comercial

## 📜 Licencia

Este sistema está desarrollado exclusivamente para Echoday. Uso comercial autorizado únicamente para Echoday y sus clientes directos.

## 🔄 Actualizaciones

### Versión 1.0 (Actual)
- Sistema completo funcional
- Scraping básico de Google Maps
- Plantillas personalizadas ES/CA
- Envío SMTP con límites
- Reportes diarios automáticos

### Roadmap Futuro
- Integración WhatsApp Business API
- Machine Learning para optimización
- Dashboard web de administración
- API REST para integraciones
- Análisis predictivo de conversión

---

**🚀 ¡Listo para generar 2000€+ semanales en nuevos clientes!**

El sistema está diseñado para funcionar de forma autónoma, requiriendo supervisión mínima una vez configurado. Ideal para escalar la captación B2B de Echoday de forma eficiente y profesional.