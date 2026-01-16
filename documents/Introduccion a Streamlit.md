### DevMentor AI - Introducción a Streamlit

📋 Índice
---------

1. [Instalación y Configuración](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#instalaci%C3%B3n-y-configuraci%C3%B3n)
2. [¿Qué es Streamlit?](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#qu%C3%A9-es-streamlit)
3. [Conceptos Fundamentales](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#conceptos-fundamentales)
4. [Widgets de Entrada](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#widgets-de-entrada)
5. [Organización y Layout](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#organizaci%C3%B3n-y-layout)
6. [Elementos Visuales y Media](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#elementos-visuales-y-media)
7. [Estado de Sesión](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#estado-de-sesi%C3%B3n)
8. [Formularios](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#formularios)
9. [Ejemplos Prácticos Completos](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#ejemplos-pr%C3%A1cticos-completos)
10. [Mejores Prácticas](https://apps.abacus.ai/chatllm/?appId=15304b1852&convoId=11af58238&playgroundType=markdown#mejores-pr%C3%A1cticas)

* * *

Instalación y Configuración
---------------------------

### Prerrequisitos

* Python 3.9 o superior
* pip funcionando correctamente

### Instalación

    pip install streamlit

### Verificar instalación

    streamlit --version

### Primera aplicación de prueba

    streamlit hello

* * *

¿Qué es Streamlit?
------------------

**Streamlit** es un framework de Python que permite crear aplicaciones web interactivas escribiendo únicamente código Python, sin necesidad de HTML, CSS o JavaScript.

### Características principales:

* **Simplicidad**: Solo Python
* **Reactividad**: La interfaz se actualiza automáticamente
* **Rapidez**: De script a web app en minutos

### Modelo de ejecución

**Concepto clave**: Streamlit ejecuta tu script **de arriba hacia abajo** cada vez que:

* El usuario interactúa con un widget

* Cambia un valor

* Presiona un botón

```python
import streamlit as st

# Esto se ejecuta CADA VEZ que hay una interacción
st.title("Mi App")
print("Script ejecutándose...")  # Verás esto en consola cada vez
contador = 0  # Se reinicia en cada ejecución
```

**Implicación importante**: Las variables normales se reinician. Para mantener datos entre ejecuciones, usaremos `st.session_state` (lo veremos más adelante).

* * *

Conceptos Fundamentales
-----------------------

### 1. Estructura básica de una aplicación

```python
    import streamlit as st

    # 1. Configuración (DEBE ser lo primero)
    st.set_page_config(
        page_title="Mi App",  # Título en la pestaña del navegador
        page_icon="🚀",       # Icono en la pestaña
        layout="centered"     # "centered" o "wide"
    ) 
    # 2. Título y descripción
    st.title("🚀 Mi Aplicación")
    st.write("Descripción de la aplicación")

    # 3. Contenido principal
    # Aquí va tu lógica y widgets
```

### 2. Diferencia entre `page_title` y `st.title`

* **`page_title`** (en `set_page_config`): Aparece en la **pestaña del navegador**
* **`st.title`**: Aparece **dentro de la aplicación** como encabezado grande

### 3. Opciones de `set_page_config`

```python
    st.set_page_config(
        page_title="Mi App",              # Título de la pestaña
        page_icon="🚀",                    # Emoji o URL de imagen
        layout="wide",                     # "centered" o "wide"
        initial_sidebar_state="expanded"   # "auto", "expanded", "collapsed"
    )
```

**Nota sobre `layout`**:

* `"centered"`: Contenido centrado con ancho máximo fijo (~730px)
* `"wide"`: Contenido ocupa todo el ancho del navegador

**Nota sobre `initial_sidebar_state`**:

* Solo tiene efecto si defines un sidebar posteriormente
* Es solo una sugerencia inicial; el navegador recuerda la preferencia del usuario

* * *

Widgets de Entrada
------------------

### Introducción a los Widgets

Los **widgets** son elementos interactivos que permiten al usuario ingresar datos. Streamlit ofrece una amplia variedad de widgets, cada uno optimizado para diferentes tipos de entrada.

**Comportamiento importante de los widgets**:

* Los widgets retornan su valor actual
* Cuando el usuario interactúa con un widget, Streamlit re-ejecuta el script
* Los valores se actualizan automáticamente

### 1. Entrada de Texto

#### Teoría: Widgets de texto disponibles

| Widget                             | Uso                | Características                        |
| ---------------------------------- | ------------------ | -------------------------------------- |
| `text_input`                       | Texto de una línea | Ideal para nombres, emails, búsquedas  |
| `text_area`                        | Texto multilínea   | Para comentarios, descripciones largas |
| `text_input(..., type="password")` | Contraseñas        | Oculta el texto ingresado              |

#### Parámetros importantes de `text_input`:

```python
    st.text_input(
        label="Etiqueta",           # Texto que ve el usuario
        value="",                   # Valor por defecto
        max_chars=None,             # Límite de caracteres
        key=None,                   # Identificador único (para session_state)
        type="default",             # "default" o "password"
        placeholder="Texto guía",   # Texto de ayuda
        disabled=False,             # Si está deshabilitado
        label_visibility="visible"  # "visible", "hidden", "collapsed"
    )
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Formulario de Registro")

    # Texto simple
    nombre = st.text_input(
        "Nombre completo:",
        placeholder="Ej: Juan Pérez"
    )

    # Email con validación visual
    email = st.text_input(
        "Email:",
        placeholder="tu@email.com"
    )

    if email and "@" not in email:
        st.error("⚠️ Email inválido")

    # Contraseña
    password = st.text_input(
        "Contraseña:",
        type="password",
        help="Mínimo 8 caracteres"
    )

    # Área de texto
    comentarios = st.text_area(
        "Comentarios adicionales:",
        height=100,
        placeholder="Escribe aquí tus comentarios..."
    )

    # Mostrar resultados
    if nombre:
        st.success(f"¡Bienvenido {nombre}!")
```

### 2. Entrada Numérica

#### Teoría: Widgets numéricos disponibles

| Widget           | Uso                       | Características                         |
| ---------------- | ------------------------- | --------------------------------------- |
| `number_input`   | Número con controles +/-  | Precisión exacta, ideal para cantidades |
| `slider`         | Selección visual en rango | Intuitivo, ideal para ajustes           |
| `slider` (rango) | Selección de rango        | Para filtros de precio, fechas, etc.    |

#### Parámetros de `number_input`:

```python
    st.number_input(
        label="Etiqueta",
        min_value=None,    # Valor mínimo permitido
        max_value=None,    # Valor máximo permitido
        value=0,           # Valor por defecto
        step=1,            # Incremento al usar +/-
        format=None,       # Formato de visualización (ej: "%.2f")
        key=None
    )
```

#### Parámetros de `slider`:

```python
    st.slider(
        label="Etiqueta",
        min_value=0,
        max_value=100,
        value=50,              # Valor inicial (o tupla para rango)
        step=1,                # Incremento
        format=None,           # Formato de visualización
        key=None
    )
```

**Comportamiento del slider**:

* El valor se actualiza **al soltar** el slider, no mientras arrastras
* Esto es intencional para mejorar el rendimiento
* No hay forma de cambiar este comportamiento en la versión actual

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Calculadora de IMC")

    st.write("""
    El Índice de Masa Corporal (IMC) es una medida que relaciona tu peso y altura.
    """)

    # Number input para valores precisos
    peso = st.number_input(
        "Peso (kg):",
        min_value=1.0,
        max_value=300.0,
        value=70.0,
        step=0.1,
        format="%.1f"
    )

    # Slider para selección visual
    altura = st.slider(
        "Altura (cm):",
        min_value=50,
        max_value=250,
        value=170,
        step=1
    )

    # Calcular IMC
    if peso > 0 and altura > 0:
        altura_m = altura / 100
        imc = peso / (altura_m ** 2)

        st.metric("Tu IMC", f"{imc:.1f}")

        # Interpretación
        if imc < 18.5:
            st.info("Bajo peso")
        elif imc < 25:
            st.success("Peso normal")
        elif imc < 30:
            st.warning("Sobrepeso")
        else:
            st.error("Obesidad")

    # Ejemplo de slider de rango
    st.subheader("Filtro de Precios")

    rango_precio = st.slider(
        "Rango de precios (€):",
        min_value=0,
        max_value=1000,
        value=(200, 800),  # Tupla para rango
        step=10
    )

    st.write(f"Mostrando productos entre €{rango_precio[0]} y €{rango_precio[1]}")
```

### 3. Selección

#### Teoría: Widgets de selección disponibles

| Widget        | Uso                        | Características                   |
| ------------- | -------------------------- | --------------------------------- |
| `selectbox`   | Selección única (dropdown) | Ahorra espacio, muchas opciones   |
| `radio`       | Selección única (botones)  | Todas las opciones visibles       |
| `multiselect` | Selección múltiple         | Usuario puede elegir varias       |
| `checkbox`    | Opción binaria (sí/no)     | Para activar/desactivar funciones |

#### Cuándo usar cada uno:

* **`selectbox`**: Cuando tienes muchas opciones (>5) y el usuario elige una
* **`radio`**: Cuando tienes pocas opciones (2-5) y quieres que todas sean visibles
* **`multiselect`**: Cuando el usuario puede elegir varias opciones
* **`checkbox`**: Para opciones binarias (activar/desactivar)

#### Parámetros de `selectbox`:

```python
    st.selectbox(
        label="Etiqueta",
        options=[...],         # Lista de opciones
        index=0,               # Índice de la opción por defecto
        format_func=lambda x: x,  # Función para formatear visualización
        key=None
    )
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Configurador de Producto")

    # Selectbox - muchas opciones
    ciudad = st.selectbox(
        "Ciudad de envío:",
        ["Madrid", "Barcelona", "Valencia", "Sevilla", "Bilbao", 
         "Málaga", "Zaragoza", "Murcia", "Palma", "Las Palmas"]
    )

    # Radio - pocas opciones, todas visibles
    metodo_pago = st.radio(
        "Método de pago:",
        ["Tarjeta de crédito", "PayPal", "Transferencia"],
        help="Selecciona tu método de pago preferido"
    )

    # Multiselect - múltiples opciones
    extras = st.multiselect(
        "Extras opcionales:",
        ["Envío express", "Embalaje regalo", "Seguro", "Garantía extendida"],
        default=[]  # Ninguno seleccionado por defecto
    )

    # Checkboxes - opciones binarias
    acepta_terminos = st.checkbox("Acepto los términos y condiciones")
    suscribir_newsletter = st.checkbox("Quiero recibir ofertas por email")

    # Mostrar resumen
    if acepta_terminos:
        st.success("✅ Configuración completada")

        with st.expander("Ver resumen del pedido"):
            st.write(f"**Ciudad:** {ciudad}")
            st.write(f"**Pago:** {metodo_pago}")
            st.write(f"**Extras:** {', '.join(extras) if extras else 'Ninguno'}")
            st.write(f"**Newsletter:** {'Sí' if suscribir_newsletter else 'No'}")
    else:
        st.warning("⚠️ Debes aceptar los términos para continuar")
```

### 4. Fechas y Tiempo

#### Teoría: Widgets de fecha/hora disponibles

| Widget       | Uso                | Retorna         |
| ------------ | ------------------ | --------------- |
| `date_input` | Selección de fecha | `datetime.date` |
| `time_input` | Selección de hora  | `datetime.time` |

#### Ejemplo práctico:

```python
    import streamlit as st
    from datetime import datetime, date, time, timedelta

    st.title("Reserva de Cita")

    # Fecha
    fecha_cita = st.date_input(
        "Fecha de la cita:",
        value=date.today(),
        min_value=date.today(),  # No permitir fechas pasadas
        max_value=date.today() + timedelta(days=90)  # Máximo 90 días adelante
    )

    # Hora
    hora_cita = st.time_input(
        "Hora de la cita:",
        value=time(9, 0)  # 9:00 AM por defecto
    )

    # Mostrar confirmación
    if fecha_cita and hora_cita:
        st.success(f"Cita reservada para: {fecha_cita.strftime('%d/%m/%Y')} a las {hora_cita.strftime('%H:%M')}")

        # Calcular días hasta la cita
        dias_hasta = (fecha_cita - date.today()).days
        if dias_hasta == 0:
            st.info("¡Tu cita es hoy!")
        elif dias_hasta == 1:
            st.info("Tu cita es mañana")
        else:
            st.info(f"Faltan {dias_hasta} días para tu cita")
```

### 5. Archivos

#### Teoría: `file_uploader`

Permite al usuario subir archivos desde su computadora.

#### Parámetros importantes:

```python
    st.file_uploader(
        label="Etiqueta",
        type=None,                    # Lista de extensiones permitidas
        accept_multiple_files=False,  # Si permite múltiples archivos
        key=None
    )
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Procesador de Archivos")

    # Subir un solo archivo
    archivo = st.file_uploader(
        "Sube un archivo de texto:",
        type=['txt', 'md'],
        help="Solo archivos .txt o .md"
    )

    if archivo is not None:
        # Información del archivo
        st.write(f"**Nombre:** {archivo.name}")
        st.write(f"**Tamaño:** {archivo.size} bytes")
        st.write(f"**Tipo:** {archivo.type}")

        # Leer contenido
        contenido = archivo.read().decode('utf-8')

        st.subheader("Contenido del archivo:")
        st.text_area("", contenido, height=200)

        # Estadísticas
        palabras = len(contenido.split())
        lineas = len(contenido.split('\n'))

        col1, col2 = st.columns(2)
        col1.metric("Palabras", palabras)
        col2.metric("Líneas", lineas)

    # Subir múltiples archivos
    st.subheader("Subir múltiples archivos")

    archivos = st.file_uploader(
        "Sube varios archivos:",
        accept_multiple_files=True
    )

    if archivos:
        st.write(f"Has subido {len(archivos)} archivo(s):")
        for archivo in archivos:
            st.write(f"- {archivo.name}")
```

### 6. Botones

#### Teoría: Tipos de botones disponibles

| Widget               | Uso               | Características                   |
| -------------------- | ----------------- | --------------------------------- |
| `button`             | Acción simple     | Retorna `True` cuando se presiona |
| `download_button`    | Descargar archivo | Permite descargar datos           |
| `form_submit_button` | Enviar formulario | Solo dentro de `st.form`          |

#### Comportamiento importante de `button`:

```python
    # El botón retorna True SOLO en la ejecución donde se presiona
    if st.button("Hacer clic"):
        st.write("¡Botón presionado!")  # Esto desaparece en la siguiente interacción
```

**Para mantener el estado**, usa `session_state` (lo veremos más adelante).

#### Parámetros de `button`:

```python
    st.button(
        label="Texto del botón",
        key=None,
        help=None,
        on_click=None,              # Función callback
        type="secondary",           # "primary" o "secondary"
        disabled=False,
        use_container_width=False   # Si ocupa todo el ancho
    )
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Tipos de Botones")

    # Botón simple
    if st.button("Botón Normal"):
        st.success("¡Botón presionado!")

    # Botón primario (destacado)
    if st.button("Botón Primario", type="primary"):
        st.balloons()  # Animación de celebración

    # Botón de ancho completo
    if st.button("Botón Ancho", use_container_width=True):
        st.info("Este botón ocupa todo el ancho")

    # Botón de descarga
    datos = "Este es el contenido del archivo\nLínea 2\nLínea 3"

    st.download_button(
        label="📥 Descargar archivo",
        data=datos,
        file_name="mi_archivo.txt",
        mime="text/plain"
    )

    # Botones en columnas
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Opción A"):
            st.write("Elegiste A")

    with col2:
        if st.button("Opción B"):
            st.write("Elegiste B")

    with col3:
        if st.button("Opción C"):
            st.write("Elegiste C")
```

* * *

Organización y Layout
---------------------

### Introducción al Layout

Streamlit organiza el contenido de forma **secuencial** por defecto (de arriba hacia abajo). Para crear layouts más complejos, disponemos de varios contenedores y herramientas de organización.

### 1. Columnas

#### Teoría: `st.columns`

Divide el espacio horizontal en columnas.
    # Columnas de igual ancho
    col1, col2, col3 = st.columns(3)
    # Columnas con proporciones personalizadas
    col1, col2 = st.columns([2, 1])  # col1 es el doble de ancha que col2

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Dashboard con Columnas")

    # Métricas en columnas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Usuarios", "1,234", "+12%")

    with col2:
        st.metric("Ventas", "€45,678", "+8%")

    with col3:
        st.metric("Conversión", "3.2%", "-0.5%")

    with col4:
        st.metric("Satisfacción", "4.8/5", "+0.2")

    # Layout de contenido principal + sidebar
    col_main, col_side = st.columns([3, 1])

    with col_main:
        st.subheader("Contenido Principal")
        st.write("Este es el área principal de contenido")
        st.line_chart([1, 2, 3, 4, 5])

    with col_side:
        st.subheader("Panel Lateral")
        filtro = st.selectbox("Filtro:", ["Todos", "Activos", "Archivados"])
        st.button("Aplicar")
```

### 2. Sidebar

#### Teoría: `st.sidebar`

Crea una barra lateral colapsable. Ideal para controles y configuración.

**Dos formas de usar el sidebar:**

```python
    # Forma 1: Prefijo
    st.sidebar.title("Título en sidebar")
    st.sidebar.button("Botón en sidebar")
    # Forma 2: Context manager (recomendado)
    with st.sidebar:
        st.title("Título en sidebar")
        st.button("Botón en sidebar")
```

**Nota**: El sidebar solo aparece si le agregas contenido.

#### Ejemplo práctico:

```python
    import streamlit as st

    st.set_page_config(
        page_title="App con Sidebar",
        initial_sidebar_state="expanded"  # Expandido por defecto
    )

    # Sidebar con controles
    with st.sidebar:
        st.header("⚙️ Configuración")

        modo = st.radio(
            "Modo de visualización:",
            ["Claro", "Oscuro"]
        )

        st.divider()  # Línea separadora

        st.subheader("Filtros")
        categoria = st.selectbox(
            "Categoría:",
            ["Todas", "Tecnología", "Deportes", "Cultura"]
        )

        fecha_desde = st.date_input("Desde:")
        fecha_hasta = st.date_input("Hasta:")

        st.divider()

        if st.button("Aplicar Filtros", type="primary"):
            st.success("Filtros aplicados")

    # Contenido principal
    st.title("Contenido Principal")
    st.write(f"Modo: {modo}")
    st.write(f"Categoría: {categoria}")
    st.write(f"Período: {fecha_desde} - {fecha_hasta}")
```

### 3. Tabs (Pestañas)

#### Teoría: `st.tabs`

Organiza contenido en pestañas, similar a las pestañas de un navegador.

```python
    tab1, tab2, tab3 = st.tabs(["Pestaña 1", "Pestaña 2", "Pestaña 3"])
    with tab1:
        # Contenido de la pestaña 1
        pass
    with tab2:
        # Contenido de la pestaña 2
        pass
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Panel de Control")

    # Crear tabs con iconos
    tab1, tab2, tab3 = st.tabs(["📊 Datos", "📈 Gráficos", "⚙️ Configuración"])

    with tab1:
        st.header("Datos")
        st.write("Aquí se muestran los datos en formato tabla")

        import pandas as pd
        df = pd.DataFrame({
            'Producto': ['A', 'B', 'C'],
            'Ventas': [100, 150, 120]
        })
        st.dataframe(df)

    with tab2:
        st.header("Gráficos")
        st.write("Visualización de los datos")
        st.bar_chart(df.set_index('Producto'))

    with tab3:
        st.header("Configuración")
        st.checkbox("Mostrar totales")
        st.checkbox("Exportar automáticamente")
        st.selectbox("Formato de exportación:", ["CSV", "Excel", "JSON"])
```

### 4. Expanders (Secciones Colapsables)

#### Teoría: `st.expander`

Crea secciones que el usuario puede expandir/colapsar. Útil para información adicional o detalles opcionales.

```python
    with st.expander("Ver detalles"):
        st.write("Contenido que se puede ocultar")
```

#### Parámetros:

```python
    st.expander(
        label="Etiqueta",
        expanded=False  # Si está expandido por defecto
    )
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Artículo con Secciones Colapsables")

    st.write("""
    Este es el contenido principal que siempre está visible.
    """)

    # Expander para información adicional
    with st.expander("📖 Leer más"):
        st.write("""
        Aquí va información adicional que el usuario puede elegir ver o no.
        Esto ayuda a mantener la interfaz limpia.
        """)

    # Expander para detalles técnicos
    with st.expander("🔧 Detalles técnicos"):
        st.code("""
        def ejemplo():
            return "Código de ejemplo"
        """)

    # Expander expandido por defecto
    with st.expander("⚠️ Información importante", expanded=True):
        st.warning("Este expander está abierto por defecto")
```

### 5. Containers

#### Teoría: `st.container`

Agrupa elementos en un contenedor. Útil para organizar lógicamente el código y para actualizar secciones específicas.

```python
    with st.container():
        st.write("Contenido en container")
        st.button("Botón")
```

#### Parámetros:

```python
    st.container(
        border=False  # Si muestra borde visual
    )
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Organización con Containers")

    # Container sin borde
    with st.container():
        st.subheader("Sección 1")
        st.write("Contenido de la sección 1")

    # Container con borde
    with st.container(border=True):
        st.subheader("Sección 2 (con borde)")
        st.write("Este container tiene un borde visual")
        st.button("Botón en container")

    # Uso avanzado: placeholder que se puede llenar después
    placeholder = st.empty()

    if st.button("Llenar placeholder"):
        with placeholder.container():
            st.success("¡Contenido añadido dinámicamente!")
            st.write("Este contenido apareció después de presionar el botón")
```

* * *

Elementos Visuales y Media
--------------------------

### Introducción

Además de widgets de entrada, Streamlit ofrece múltiples formas de **mostrar** información: texto formateado, imágenes, gráficos, audio, video, etc.

### 1. Texto y Markdown

#### Teoría: Formas de mostrar texto

| Función        | Uso                  | Características                              |
| -------------- | -------------------- | -------------------------------------------- |
| `st.write`     | Propósito general    | Detecta automáticamente el tipo de contenido |
| `st.markdown`  | Markdown             | Soporta formato Markdown y HTML limitado     |
| `st.title`     | Título principal     | Equivalente a `# Título` en Markdown         |
| `st.header`    | Encabezado           | Equivalente a `## Encabezado`                |
| `st.subheader` | Subencabezado        | Equivalente a `### Subencabezado`            |
| `st.text`      | Texto plano          | Sin formato                                  |
| `st.code`      | Código               | Con resaltado de sintaxis                    |
| `st.latex`     | Fórmulas matemáticas | Notación LaTeX                               |

#### Ejemplo práctico:

```python
    import streamlit as st

    # Títulos jerárquicos
    st.title("Título Principal")
    st.header("Encabezado")
    st.subheader("Subencabezado")

    # Texto con formato Markdown
    st.markdown("""
    ### Markdown soporta:
    - **Negrita**
    - *Cursiva*
    - `código inline`
    - [Enlaces](https://streamlit.io)

    1. Listas numeradas
    2. También funcionan
    """)

    # Código con resaltado
    st.code("""
    def saludar(nombre):
        return f"Hola {nombre}!"
    """, language="python")

    # Fórmulas matemáticas
    st.latex(r"E = mc^2")
    st.latex(r"\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n")

    # st.write es "mágico" - detecta el tipo
    st.write("Texto simple")
    st.write({"clave": "valor"})  # Muestra como JSON
    st.write([1, 2, 3, 4, 5])     # Muestra como lista
```

### 2. Mensajes de Estado

#### Teoría: Tipos de mensajes

| Función        | Uso         | Color              |
| -------------- | ----------- | ------------------ |
| `st.success`   | Éxito       | Verde              |
| `st.info`      | Información | Azul               |
| `st.warning`   | Advertencia | Amarillo           |
| `st.error`     | Error       | Rojo               |
| `st.exception` | Excepción   | Rojo con traceback |

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Mensajes de Estado")

    st.success("✅ Operación completada exitosamente")
    st.info("ℹ️ Información importante para el usuario")
    st.warning("⚠️ Advertencia: verifica los datos")
    st.error("❌ Error: no se pudo completar la operación")

    # Mostrar excepciones
    try:
        resultado = 10 / 0
    except Exception as e:
        st.exception(e)
```

### 3. Imágenes

#### Teoría: `st.image`

Muestra imágenes desde archivos locales, URLs o arrays de NumPy.

#### Parámetros importantes:

```python
    st.image(
        image,                    # Ruta, URL o array
        caption=None,             # Texto debajo de la imagen
        width=None,               # Ancho en píxeles
        use_column_width=None,    # "auto", "always", "never", True, False
        channels="RGB"            # "RGB" o "BGR"
    )
```

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Galería de Imágenes")

    # Imagen desde URL
    st.subheader("Imagen desde URL")
    st.image(
        "https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png",
        caption="Logo de Streamlit",
        width=300
    )

    # Múltiples imágenes en columnas
    st.subheader("Galería")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("https://via.placeholder.com/150", caption="Imagen 1")

    with col2:
        st.image("https://via.placeholder.com/150", caption="Imagen 2")

    with col3:
        st.image("https://via.placeholder.com/150", caption="Imagen 3")

    # Imagen subida por el usuario
    st.subheader("Sube tu imagen")

    archivo_imagen = st.file_uploader("Elige una imagen:", type=['png', 'jpg', 'jpeg'])

    if archivo_imagen is not None:
        st.image(archivo_imagen, caption="Tu imagen", use_column_width=True)
```

### 4. Gráficos Simples

#### Teoría: Gráficos integrados de Streamlit

Streamlit incluye gráficos simples sin necesidad de librerías externas:

| Función         | Tipo de gráfico   |
| --------------- | ----------------- |
| `st.line_chart` | Gráfico de líneas |
| `st.area_chart` | Gráfico de área   |
| `st.bar_chart`  | Gráfico de barras |

**Nota**: Para gráficos más avanzados, se usan librerías como Plotly, Matplotlib, Altair, etc.

#### Ejemplo práctico:

```python
    import streamlit as st
    import pandas as pd
    import numpy as np

    st.title("Gráficos Simples")

    # Datos de ejemplo
    datos = pd.DataFrame({
        'Ventas': np.random.randn(20).cumsum(),
        'Costos': np.random.randn(20).cumsum()
    })

    # Gráfico de líneas
    st.subheader("Gráfico de Líneas")
    st.line_chart(datos)

    # Gráfico de área
    st.subheader("Gráfico de Área")
    st.area_chart(datos)

    # Gráfico de barras
    st.subheader("Gráfico de Barras")
    datos_barras = pd.DataFrame({
        'Producto A': [10, 20, 30],
        'Producto B': [15, 25, 35]
    })
    st.bar_chart(datos_barras)
```

### 5. Tablas y DataFrames

#### Teoría: Formas de mostrar datos tabulares

| Función        | Uso               | Características       |
| -------------- | ----------------- | --------------------- |
| `st.dataframe` | Tabla interactiva | Scrollable, ordenable |
| `st.table`     | Tabla estática    | No interactiva        |
| `st.metric`    | Métrica con delta | Para KPIs             |

#### Ejemplo práctico:

```python
    import streamlit as st
    import pandas as pd

    st.title("Visualización de Datos")

    # Crear datos de ejemplo
    df = pd.DataFrame({
        'Producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor'],
        'Precio': [999, 29, 79, 299],
        'Stock': [15, 50, 30, 20],
        'Categoría': ['Computadoras', 'Accesorios', 'Accesorios', 'Computadoras']
    })

    # DataFrame interactivo
    st.subheader("DataFrame Interactivo")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Tabla estática
    st.subheader("Tabla Estática")
    st.table(df.head(2))

    # Métricas
    st.subheader("Métricas")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Productos Totales",
        len(df),
        delta=2,
        delta_color="normal"
    )

    col2.metric(
        "Valor Inventario",
        f"€{(df['Precio'] * df['Stock']).sum():,}",
        delta="€5,000",
        delta_color="normal"
    )

    col3.metric(
        "Stock Promedio",
        f"{df['Stock'].mean():.1f}",
        delta=-3,
        delta_color="inverse"
    )
```

### 6. Elementos de Progreso

#### Teoría: Indicadores de progreso

| Función       | Uso                |
| ------------- | ------------------ |
| `st.progress` | Barra de progreso  |
| `st.spinner`  | Indicador de carga |
| `st.status`   | Estado con pasos   |

#### Ejemplo práctico:

```python
    import streamlit as st
    import time

    st.title("Indicadores de Progreso")

    # Barra de progreso
    st.subheader("Barra de Progreso")

    if st.button("Iniciar proceso"):
        barra_progreso = st.progress(0)

        for i in range(100):
            time.sleep(0.01)
            barra_progreso.progress(i + 1)

        st.success("¡Proceso completado!")

    # Spinner
    st.subheader("Spinner")

    if st.button("Cargar datos"):
        with st.spinner("Cargando..."):
            time.sleep(3)
        st.success("Datos cargados")

    # Status con pasos
    st.subheader("Status con Pasos")

    if st.button("Ejecutar pipeline"):
        with st.status("Ejecutando pipeline...", expanded=True) as status:
            st.write("Paso 1: Cargando datos...")
            time.sleep(1)

            st.write("Paso 2: Procesando...")
            time.sleep(1)

            st.write("Paso 3: Guardando resultados...")
            time.sleep(1)

            status.update(label="¡Pipeline completado!", state="complete", expanded=False)
```

### 7. Audio y Video

#### Teoría: Multimedia

| Función    | Uso                  |
| ---------- | -------------------- |
| `st.audio` | Reproductor de audio |
| `st.video` | Reproductor de video |

#### Ejemplo práctico:

```python
    import streamlit as st

    st.title("Multimedia")

    # Audio
    st.subheader("Audio")

    archivo_audio = st.file_uploader("Sube un archivo de audio:", type=['mp3', 'wav'])

    if archivo_audio is not None:
        st.audio(archivo_audio)

    # Video desde URL
    st.subheader("Video")

    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    # Video subido
    archivo_video = st.file_uploader("Sube un video:", type=['mp4', 'mov'])

    if archivo_video is not None:
        st.video(archivo_video)
```

* * *

Estado de Sesión
----------------

### Introducción al Problema

Recuerda: Streamlit **re-ejecuta todo el script** en cada interacción. Esto significa que las variables normales se reinician:

```python
    # ❌ PROBLEMA: Este contador siempre será 1
    contador = 0
    if st.button("Incrementar"):
        contador += 1  # Se incrementa...
        st.write(contador)  # Muestra 1...
        # Pero en la siguiente ejecución, contador vuelve a ser 0

**Solución**: `st.session_state` - un diccionario que persiste entre ejecuciones.
```

### Teoría: `st.session_state`

`st.session_state` es un diccionario especial que mantiene su contenido entre re-ejecuciones del script.

#### Formas de usar session_state:

```python
    # Forma 1: Como diccionario
    if 'contador' not in st.session_state:
        st.session_state['contador'] = 0

    # Forma 2: Como atributo (más común)
    if 'contador' not in st.session_state:
        st.session_state.contador = 0
```

### Patrón Básico

```python
    import streamlit as st

    # 1. Inicializar (siempre al inicio)
    if 'contador' not in st.session_state:
        st.session_state.contador = 0

    # 2. Mostrar valor actual
    st.write(f"Contador: {st.session_state.contador}")

    # 3. Modificar valor
    if st.button("Incrementar"):
        st.session_state.contador += 1
        st.rerun()  # Opcional: forzar re-ejecución inmediata
```

### Ejemplo Práctico 1: Contador Persistente

```python
    import streamlit as st

    st.title("Contador Persistente")

    # Inicializar
    if 'contador' not in st.session_state:
        st.session_state.contador = 0

    # Mostrar
    st.metric("Contador", st.session_state.contador)

    # Controles
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("➕ Incrementar"):
            st.session_state.contador += 1
            st.rerun()

    with col2:
        if st.button("➖ Decrementar"):
            st.session_state.contador -= 1
            st.rerun()

    with col3:
        if st.button("🔄 Resetear"):
            st.session_state.contador = 0
            st.rerun()
```

### Ejemplo Práctico 2: Lista de Tareas

```python
    import streamlit as st

    st.title("📝 Lista de Tareas")

    # Inicializar lista de tareas
    if 'tareas' not in st.session_state:
        st.session_state.tareas = []

    # Agregar nueva tarea
    nueva_tarea = st.text_input("Nueva tarea:")

    if st.button("Agregar") and nueva_tarea:
        st.session_state.tareas.append({
            'texto': nueva_tarea,
            'completada': False
        })
        st.rerun()

    # Mostrar tareas
    if st.session_state.tareas:
        for i, tarea in enumerate(st.session_state.tareas):
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                if tarea['completada']:
                    st.write(f"~~{tarea['texto']}~~")
                else:
                    st.write(tarea['texto'])

            with col2:
                if st.button("✓", key=f"completar_{i}"):
                    st.session_state.tareas[i]['completada'] = not tarea['completada']
                    st.rerun()

            with col3:
                if st.button("🗑️", key=f"eliminar_{i}"):
                    st.session_state.tareas.pop(i)
                    st.rerun()
    else:
        st.info("No hay tareas. ¡Agrega una!")
```

* * *

Formularios
-----------

### Introducción al Problema

Sin formularios, cada interacción con un widget causa una re-ejecución:

```python
    # ❌ PROBLEMA: Cada tecla causa re-ejecución
    nombre = st.text_input("Nombre:")  # Re-ejecuta al escribir
    email = st.text_input("Email:")    # Re-ejecuta al escribir
    edad = st.number_input("Edad:")    # Re-ejecuta al cambiar
```

**Solución**: `st.form` - agrupa widgets y solo re-ejecuta al enviar el formulario.

### Teoría: `st.form`

Un formulario agrupa widgets y solo dispara re-ejecución cuando se presiona el botón de envío.

```python
    with st.form("mi_formulario"):
        # Widgets dentro del formulario
        nombre = st.text_input("Nombre:")
        email = st.text_input("Email:")
        # Botón de envío (obligatorio)
        submitted = st.form_submit_button("Enviar")
        if submitted:
            # Procesar datos
            st.write(f"Nombre: {nombre}, Email: {email}")
```

### Reglas de los Formularios

1. **Debe tener un `form_submit_button`** (obligatorio)
2. **Los widgets dentro no disparan re-ejecución** hasta enviar
3. **No se puede usar `st.button` normal** dentro de un formulario
4. **No se puede anidar formularios**

### Ejemplo Práctico: Formulario de Contacto

```python
    import streamlit as st

    st.title("📧 Formulario de Contacto")

    with st.form("formulario_contacto"):
        st.write("Completa el formulario:")

        nombre = st.text_input("Nombre completo:")
        email = st.text_input("Email:")
        asunto = st.selectbox("Asunto:", ["Consulta", "Soporte", "Sugerencia"])
        mensaje = st.text_area("Mensaje:", height=150)

        # Checkbox dentro del formulario
        acepta = st.checkbox("Acepto la política de privacidad")

        # Botón de envío
        submitted = st.form_submit_button("Enviar Mensaje")

        if submitted:
            if not nombre or not email or not mensaje:
                st.error("Por favor completa todos los campos")
            elif not acepta:
                st.warning("Debes aceptar la política de privacidad")
            else:
                st.success("¡Mensaje enviado exitosamente!")
                st.balloons()
```

* * *

Ejemplos Prácticos Completos
----------------------------

### Ejemplo 1: Calculadora Avanzada

```python
    import streamlit as st
    import math

    st.set_page_config(page_title="Calculadora", page_icon="🧮")

    st.title("🧮 Calculadora Avanzada")

    # Tabs para diferentes tipos de cálculos
    tab1, tab2 = st.tabs(["Básica", "Científica"])

    with tab1:
        st.subheader("Calculadora Básica")

        col1, col2 = st.columns(2)

        with col1:
            num1 = st.number_input("Primer número:", value=0.0, format="%.2f")

        with col2:
            num2 = st.number_input("Segundo número:", value=0.0, format="%.2f")

        operacion = st.radio(
            "Operación:",
            ["➕ Suma", "➖ Resta", "✖️ Multiplicación", "➗ División"],
            horizontal=True
        )

        if st.button("Calcular", type="primary"):
            try:
                if "Suma" in operacion:
                    resultado = num1 + num2
                elif "Resta" in operacion:
                    resultado = num1 - num2
                elif "Multiplicación" in operacion:
                    resultado = num1 * num2
                elif "División" in operacion:
                    if num2 == 0:
                        st.error("No se puede dividir por cero")
                        resultado = None
                    else:
                        resultado = num1 / num2

                if resultado is not None:
                    st.success(f"Resultado: {resultado:.2f}")

            except Exception as e:
                st.error(f"Error: {e}")

    with tab2:
        st.subheader("Calculadora Científica")

        numero = st.number_input("Número:", value=0.0)

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("√ Raíz Cuadrada"):
                if numero >= 0:
                    st.write(f"√{numero} = {math.sqrt(numero):.4f}")
                else:
                    st.error("No se puede calcular raíz de número negativo")

        with col2:
            if st.button("x² Cuadrado"):
                st.write(f"{numero}² = {numero**2:.4f}")

        with col3:
            if st.button("x³ Cubo"):
                st.write(f"{numero}³ = {numero**3:.4f}")
```

### Ejemplo 2: Gestor de Notas

```python
    import streamlit as st
    from datetime import datetime

    st.set_page_config(page_title="Gestor de Notas", page_icon="📝", layout="wide")

    st.title("📝 Gestor de Notas")

    # Inicializar notas
    if 'notas' not in st.session_state:
        st.session_state.notas = []

    # Sidebar para crear nota
    with st.sidebar:
        st.header("➕ Nueva Nota")

        with st.form("nueva_nota"):
            titulo = st.text_input("Título:")
            contenido = st.text_area("Contenido:", height=150)
            categoria = st.selectbox("Categoría:", ["Personal", "Trabajo", "Estudio", "Ideas"])

            submitted = st.form_submit_button("Guardar Nota")

            if submitted and titulo and contenido:
                nueva_nota = {
                    'titulo': titulo,
                    'contenido': contenido,
                    'categoria': categoria,
                    'fecha': datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state.notas.append(nueva_nota)
                st.success("Nota guardada")
                st.rerun()

    # Contenido principal
    if st.session_state.notas:
        # Filtros
        col1, col2 = st.columns([3, 1])

        with col1:
            busqueda = st.text_input("🔍 Buscar notas:", placeholder="Escribe para buscar...")

        with col2:
            filtro_categoria = st.selectbox("Filtrar por:", ["Todas"] + ["Personal", "Trabajo", "Estudio", "Ideas"])

        # Filtrar notas
        notas_filtradas = st.session_state.notas

        if filtro_categoria != "Todas":
            notas_filtradas = [n for n in notas_filtradas if n['categoria'] == filtro_categoria]

        if busqueda:
            notas_filtradas = [n for n in notas_filtradas 
                              if busqueda.lower() in n['titulo'].lower() 
                              or busqueda.lower() in n['contenido'].lower()]

        # Mostrar notas
        st.write(f"**{len(notas_filtradas)} nota(s) encontrada(s)**")

        for i, nota in enumerate(reversed(notas_filtradas)):
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.subheader(nota['titulo'])

                with col2:
                    st.caption(f"📁 {nota['categoria']}")

                with col3:
                    st.caption(f"📅 {nota['fecha']}")

                st.write(nota['contenido'])

                if st.button("🗑️ Eliminar", key=f"del_{i}"):
                    idx_real = st.session_state.notas.index(nota)
                    st.session_state.notas.pop(idx_real)
                    st.rerun()

    else:
        st.info("👈 No hay notas. Crea una usando el panel lateral")
```

* * *

Mejores Prácticas
-----------------

### 1. Estructura del Código

```python
    import streamlit as st

    # ✅ BUENO: Configuración al inicio
    st.set_page_config(page_title="Mi App", layout="wide")

    # ✅ BUENO: Funciones para lógica
    def procesar_datos(data):
        return data.upper()

    # ✅ BUENO: Inicialización de session state
    def init_session_state():
        if 'data' not in st.session_state:
            st.session_state.data = []

    # ✅ BUENO: Función principal
    def main():
        init_session_state()
        st.title("Mi Aplicación")
        # Lógica aquí

    if __name__ == "__main__":
        main()
```

### 2. Performance

```python
    # ✅ BUENO: Cachear datos costosos
    @st.cache_data
    def cargar_datos():
        # Operación costosa
        return pd.read_csv("datos.csv")

    # ✅ BUENO: Cachear recursos
    @st.cache_resource
    def init_modelo():
        return cargar_modelo()
```

### 3. UX/UI

```python
    # ✅ BUENO: Feedback visual
    with st.spinner("Cargando..."):
        time.sleep(2)
        st.success("Completado")

    # ✅ BUENO: Validación
    email = st.text_input("Email:")
    if email and "@" not in email:
        st.error("Email inválido")
```

* * *

Resumen
-------

Has aprendido:

1. **Conceptos fundamentales**: Modelo de ejecución, reactividad
2. **Widgets de entrada**: Texto, números, selección, fechas, archivos, botones
3. **Layout**: Columnas, sidebar, tabs, expanders, containers
4. **Elementos visuales**: Texto, imágenes, gráficos, tablas, multimedia
5. **Session state**: Persistencia de datos entre ejecuciones
6. **Formularios**: Agrupar widgets y controlar re-ejecuciones
