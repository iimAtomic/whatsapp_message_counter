# Utiliser une image de base Python légère
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des dépendances et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source de l'application dans le conteneur
COPY . .

# Exposer le port sur lequel l'application Flask va écouter
EXPOSE 5000

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Commande pour démarrer l'application via Flask
CMD ["flask", "run"]
