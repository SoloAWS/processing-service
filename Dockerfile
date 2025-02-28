# Usa una imagen base de Python
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los requisitos e instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente
COPY . .

# Expone el puerto (Cloud Run usa el puerto 8080 por defecto)
EXPOSE 8080

# Comando para iniciar la aplicación
CMD ["uvicorn", "src.processing_service.main:app", "--host", "0.0.0.0", "--port", "8080"]