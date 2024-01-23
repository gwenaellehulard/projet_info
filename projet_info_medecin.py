import json
from datetime import datetime, timedelta

class Utilisateur:
    def __init__(self, nom_utilisateur, mot_de_passe):
        self.nom_utilisateur = nom_utilisateur
        self.mot_de_passe = mot_de_passe
        self.rendez_vous = []

class Medecin(Utilisateur):
    def __init__(self, nom_utilisateur, mot_de_passe):
        super().__init__(nom_utilisateur, mot_de_passe)
        self.horaires = {"matin": [], "apres_midi": []}

class RendezVous:
    def __init__(self, date, heure):
        self.date = date
        self.heure = heure

class SystemeRendezVous:
    def __init__(self):
        self.utilisateurs = []
        self.medecins = []
        self.rendez_vous = []

    def creer_utilisateur(self, nom_utilisateur, mot_de_passe):
        utilisateur = Utilisateur(nom_utilisateur, mot_de_passe)
        self.utilisateurs.append(utilisateur)
        return utilisateur

    def creer_medecin(self, nom_utilisateur, mot_de_passe):
        medecin = Medecin(nom_utilisateur, mot_de_passe)
        self.medecins.append(medecin)
        return medecin

    def authentifier(self, nom_utilisateur, mot_de_passe):
        for utilisateur in self.utilisateurs + self.medecins:
            if utilisateur.nom_utilisateur == nom_utilisateur and utilisateur.mot_de_passe == mot_de_passe:
                return utilisateur
        return None

    def afficher_rendez_vous_disponibles(self):
        for medecin in self.medecins:
            print(f"\nMedecin: {medecin.nom_utilisateur}")
            for horaire, creneaux in medecin.horaires.items():
                print(f"{horaire.capitalize()} Creneaux: {creneaux}")

    def prendre_rendez_vous(self, utilisateur, medecin, date, heure):
        rendez_vous = RendezVous(date, heure)
        utilisateur.rendez_vous.append(rendez_vous)
        medecin.horaires[heure].append(rendez_vous)
        self.rendez_vous.append(rendez_vous)

    def annuler_rendez_vous(self, utilisateur, rendez_vous):
        utilisateur.rendez_vous.remove(rendez_vous)
        for medecin in self.medecins:
            for horaire, creneaux in medecin.horaires.items():
                if rendez_vous in creneaux:
                    creneaux.remove(rendez_vous)
                    break
        self.rendez_vous.remove(rendez_vous)

    def afficher_rendez_vous_utilisateur(self, utilisateur):
        print(f"\nUtilisateur: {utilisateur.nom_utilisateur}")
        for rendez_vous in utilisateur.rendez_vous:
            print(f"Date: {rendez_vous.date}, Heure: {rendez_vous.heure}")

    def rechercher_rendez_vous_par_date(self, date):
        resultats = [rendez_vous for rendez_vous in self.rendez_vous if rendez_vous.date == date]
        if resultats:
            print(f"\nRendez-vous le {date}:")
            for rendez_vous in resultats:
                print(f"Medecin: {rendez_vous.medecin.nom_utilisateur}, Heure: {rendez_vous.heure}")
        else:
            print(f"Aucun rendez-vous disponible le {date}")

    def sauvegarder_donnees(self):
        donnees = {
            "utilisateurs": [(utilisateur.nom_utilisateur, utilisateur.mot_de_passe) for utilisateur in self.utilisateurs],
            "medecins": [(medecin.nom_utilisateur, medecin.mot_de_passe) for medecin in self.medecins],
            "rendez_vous": [(rendez_vous.date, rendez_vous.heure) for rendez_vous in self.rendez_vous],
        }

        with open("donnees.json", "w") as fichier:
            json.dump(donnees, fichier)

    def charger_donnees(self):
        try:
            with open("donnees.json", "r") as fichier:
                donnees = json.load(fichier)

            for nom_utilisateur, mot_de_passe in donnees["utilisateurs"]:
                self.creer_utilisateur(nom_utilisateur, mot_de_passe)

            for nom_utilisateur, mot_de_passe in donnees["medecins"]:
                self.creer_medecin(nom_utilisateur, mot_de_passe)

            for date, heure in donnees["rendez_vous"]:
                self.rendez_vous.append(RendezVous(date, heure))

        except FileNotFoundError:
            pass

# Exemple d'utilisation
systeme_rendez_vous = SystemeRendezVous()
systeme_rendez_vous.charger_donnees()

# Création d'un utilisateur et d'un médecin
utilisateur = systeme_rendez_vous.creer_utilisateur("claire de saint méloir", "TiramisuInTheSky")
medecin = systeme_rendez_vous.creer_medecin("Docteur Matmaz", "vélochouette")

# Affichage des rendez-vous disponibles
systeme_rendez_vous.afficher_rendez_vous_disponibles()

# Prise de rendez-vous
systeme_rendez_vous.prendre_rendez_vous(utilisateur, medecin, "2024-01-20", "matin")

# Affichage des rendez-vous de l'utilisateur
systeme_rendez_vous.afficher_rendez_vous_utilisateur(utilisateur)

# Annulation du rendez-vous
systeme_rendez_vous.annuler_rendez_vous(utilisateur, utilisateur.rendez_vous[0])

# Recherche des rendez-vous par date
systeme_rendez_vous.rechercher_rendez_vous_par_date("2024-01-20")

# Sauvegarde des données
systeme_rendez_vous.sauvegarder_donnees()
