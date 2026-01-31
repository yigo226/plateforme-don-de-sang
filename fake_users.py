
import random
from comptes.models import Utilisateur



# Création de faux utilisateurs pour les tests
# dans le shell Django
# exec(open('fake_users.py').read())


NOMS = ["Issa", "Zando", "Detro", "Moussa", "Abdou", "Salif", "Oumar"]
VILLES = ["Ouagadougou", "Bobo", "Koudougou", "Banfora"]
ROLES = [
    Utilisateur.Role.DEMANDEUR,
    Utilisateur.Role.DONNEUR,
]
for i in range(20):  # nombre d'utilisateurs
    nom = random.choice(NOMS)
    prenom = f"Test{i}"
    email = f"{nom.lower()}{i}@test.com"
    if Utilisateur.objects.filter(email=email).exists():
        continue
    user = Utilisateur.objects.create_user(
        email=email,
        password="12345678op",
        first_name=prenom,
        last_name=nom,
        ville=random.choice(VILLES),
        role=random.choice(ROLES),
    )
    print(" Utilisateur créé :", email)
    print(" All is finish.")