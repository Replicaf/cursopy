# Copilot Instructions - cursopy

## Project Overview
**cursopy** es un curso introductorio de Python organizado como módulos educativos progresivos. El objetivo es enseñar fundamentos de programación desde variables hasta aplicaciones prácticas.

**Estructura:**
- Archivos raíz (`format.py`, `intro.py`): ejemplos básicos y punto de entrada
- Carpeta `tipos/`: módulos temáticos numerados que construyen progresivamente

## Key Patterns & Conventions

### File Organization
- **Nomenclatura**: `NN-nombre-tema.py` (ej: `01-variables.py`, `08-calculadora.py`)
- **Propósito**: Cada archivo es una lección autónoma, no requiere importaciones externas
- **Progresión**: Los números indican orden secuencial de dificultad creciente

### Python Conventions Used
1. **Naming Style**:
   - Variables simples: `snake_case` (ej: `nombre_curso`, `alumnos`)
   - Constantes: `UPPER_SNAKE_CASE` (ej: `NOMBRE_CURSO`)
   - No se requiere PEP 8 estricto en código de ejemplo

2. **String Operations**: 
   - Uso extensivo de f-strings para interpolación moderna (ej: `f"""para los números {n1}...`)
   - Triple comillas para multi-línea

3. **Type Conversion**:
   - Conversión explícita `int()`, `float()` cuando sea necesario
   - Input del usuario requiere conversión manual a tipos numéricos (ver `08-calculadora.py`)

### Common Patterns by Topic

| Tema | Archivo | Concepto Clave |
|------|---------|---|
| Variables básicas | `01-variables.py` | Asignación, tipos implícitos |
| Strings | `02-strings.py` | Indexación, slicing con `[:]` |
| Métodos string | `04-metodos-strings.py` | `.upper()`, `.lower()`, `.strip()`, `.find()`, `.replace()` |
| Números | `06-numeros.py` | Operadores augmentados (`+=`, `-=`), operadores especiales (`//`, `%`, `**`) |
| Calculadora | `08-calculadora.py` | `input()`, f-strings, operaciones aritméticas |

## Development Guidelines

### When Adding Content
- Mantén archivos independientes: no uses imports entre módulos
- Cada archivo debe ejecutarse sin dependencias externas: `python archivo.py`
- Proporciona ejemplos prácticos después de conceptos teóricos
- Usa comentarios en español para explicaciones

### Code Style for Examples
```python
# ✓ Correcto: variable clara, sin imports
animal = "  chanCHito  feliz "
print(animal.upper())

# ✗ Evitar: sintaxis confusa o múltiples conceptos
result = (lambda x: x.upper())(animal)
```

### Common Pitfalls
1. **Type Mismatch**: Input siempre retorna string; convertir antes de operaciones numéricas
   ```python
   n1 = int(input("Número: "))  # Correcto
   ```

2. **String Interpolation**: Usa f-strings modernas, no format antiguo
   ```python
   f"valor: {n1}"  # Preferido
   "{} valor".format(n1)  # Evitar en nuevo código
   ```

## Running & Testing
```powershell
# Ejecutar un módulo específico
python .\tipos\01-variables.py

# Ejecutar desde la raíz
cd e:\workspace\cursopy
python tipos/08-calculadora.py
```

---

**Last Updated**: 28 de noviembre de 2025  
**Next Module Expected**: Probablemente listas, diccionarios, o control de flujo
