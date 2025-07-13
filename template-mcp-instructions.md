# Template - Instrucciones IA para Proyectos MCP

## 🚨 **CONTEXTO CRÍTICO - LEE ESTO PRIMERO**

### **Ubicación y Ambiente**
- **Directorio de trabajo**: `[RUTA_PROYECTO]`
- **Sistema**: Linux (bash shell)
- **Ambiente principal**: **[STACK_PRINCIPAL]**
- **Idioma**: **SIEMPRE responder en ESPAÑOL**
- **Tipo de proyecto**: **[TIPO_PROYECTO]**

### **Estado Actual del Proyecto ([FECHA])**
- ✅ **[COMPONENTE_1]**: [ESTADO]
- ✅ **[COMPONENTE_2]**: [ESTADO]
- ✅ **[COMPONENTE_3]**: [ESTADO]
- 🔴 **NUNCA** asumir que algo está "instalado globalmente"
- 🔴 **SIEMPRE** usar comandos específicos del proyecto

### **Flujo de Trabajo Obligatorio**
1. **ANTES de cualquier acción**: verificar ubicación y contexto
2. **Para setup inicial**: SIEMPRE usar `[COMANDO_SETUP]`
3. **Para comandos**: SIEMPRE usar `[PATRON_COMANDOS]`
4. **Para debugging**: usar `[COMANDO_DEBUG]`
5. **Antes de commits**: verificar que archivos sensibles no se incluyan

### **Comandos que NUNCA debes sugerir**
- ❌ `[COMANDO_PROHIBIDO_1]` (razón)
- ❌ `[COMANDO_PROHIBIDO_2]` (razón)
- ❌ `[COMANDO_PROHIBIDO_3]` (razón)

### **Comandos que SÍ debes usar siempre**
- ✅ `[COMANDO_RECOMENDADO_1]` - [descripción]
- ✅ `[COMANDO_RECOMENDADO_2]` - [descripción]
- ✅ `[COMANDO_RECOMENDADO_3]` - [descripción]

## 🏗️ Arquitectura del Proyecto

[DESCRIPCIÓN_ARQUITECTURA]

```
📁 [NOMBRE_PROYECTO]/
├── [ARCHIVO_PRINCIPAL_1]    # [descripción]
├── [ARCHIVO_PRINCIPAL_2]    # [descripción]
├── [ARCHIVO_PRINCIPAL_3]    # [descripción]
├── [DIRECTORIO_CONFIG]/     # [descripción]
└── [DIRECTORIO_RECURSOS]/   # [descripción]
```

## 🛠️ Flujos de Trabajo Esenciales

### Setup Inicial Automático
```bash
[COMANDOS_SETUP]
```

### Comandos Diarios
```bash
[COMANDOS_FRECUENTES]
```

### Debugging y Mantenimiento
```bash
[COMANDOS_DEBUG]
```

## 🎯 Patrones de Performance Críticos

### Objetivos Específicos
| Proceso | Target | Estado Actual |
|---------|--------|---------------|
| [PROCESO_1] | [TARGET_1] | [ESTADO_1] |
| [PROCESO_2] | [TARGET_2] | [ESTADO_2] |
| [PROCESO_3] | [TARGET_3] | [ESTADO_3] |

### Optimizaciones Implementadas
- **[OPTIMIZACIÓN_1]**: [descripción]
- **[OPTIMIZACIÓN_2]**: [descripción]
- **[OPTIMIZACIÓN_3]**: [descripción]

## 🔧 Configuración Específica

### Configuración Automática
[DETALLES_CONFIGURACIÓN]

### Integración con .bashrc del Usuario
El usuario ya tiene configurado:
- ✅ [CONFIGURACIÓN_BASHRC_1]
- ✅ [CONFIGURACIÓN_BASHRC_2]
- ✅ [CONFIGURACIÓN_BASHRC_3]

## 📁 Convenciones de Archivos

### Variables de Entorno
```bash
[VARIABLE_1]=[valor]           # [descripción]
[VARIABLE_2]=[valor]           # [descripción]
```

### Archivos Ejecutables
- **[ARCHIVO_EJECUTABLE_1]**: [descripción]
- **[ARCHIVO_EJECUTABLE_2]**: [descripción]

### Portabilidad
- **Ubicación estándar**: [UBICACIÓN_ESTÁNDAR]
- **Variables portátiles**: [PATRÓN_VARIABLES]
- **Dependencias**: [GESTIÓN_DEPENDENCIAS]

## 🧹 Gestión de Estado

### Archivos que NUNCA commitear
- [ARCHIVO_SENSIBLE_1] - [razón]
- [ARCHIVO_SENSIBLE_2] - [razón]
- [ARCHIVO_SENSIBLE_3] - [razón]

### Reset Completo
```bash
[COMANDOS_RESET]
```

## 🚨 Errores Comunes

### "[ERROR_COMÚN_1]"
- **Causa**: [causa]
- **Solución**: [solución]

### "[ERROR_COMÚN_2]"
- **Causa**: [causa]
- **Solución**: [solución]

### "[ERROR_COMÚN_3]"
- **Causa**: [causa]
- **Solución**: [solución]

## 🎯 **REGLAS DE ORO PARA AGENTES**

### **SIEMPRE hacer esto ANTES de responder:**
1. **Responder en ESPAÑOL** - el usuario es hispanohablante
2. Verificar ubicación y contexto del proyecto
3. Recordar stack y dependencias específicas
4. Usar comandos específicos del proyecto
5. Verificar configuración si hay dudas

### **NUNCA sugerir:**
- [ANTI_PATRÓN_1]
- [ANTI_PATRÓN_2]
- [ANTI_PATRÓN_3]
- **Responder en inglés** (solo español)

### **SIEMPRE preguntar si no estás seguro de:**
- [DUDA_COMÚN_1]
- [DUDA_COMÚN_2]
- [DUDA_COMÚN_3]

### **Respuestas típicas que debes dar:**
- Usuario: "[PROBLEMA_TÍPICO_1]" → "[SOLUCIÓN_ESPECÍFICA_1]"
- Usuario: "[PROBLEMA_TÍPICO_2]" → "[SOLUCIÓN_ESPECÍFICA_2]"
- Usuario: "[PROBLEMA_TÍPICO_3]" → "[SOLUCIÓN_ESPECÍFICA_3]"
- **Todas las respuestas en español, con comandos específicos y explicaciones claras**

---
**[TAGLINE_PROYECTO]**

## 📝 Instrucciones para usar este template:

1. Reemplazar todos los `[MARCADORES]` con información específica del proyecto
2. Completar secciones con comandos y configuraciones reales
3. Validar que todas las rutas y comandos sean correctos
4. Agregar contexto específico del usuario si aplica
5. Probar las instrucciones con diferentes escenarios
