import random
from comptes.models import Utilisateur
from donneurs.models import ProfilDonneur

GROUPES = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
VILLES = ['Ouagadougou', 'Bobo', 'Koudougou', 'Banfora']
date_naissances = [
    '1990-05-14', '1985-11-23', '1992-03-10', '1988-07-22', '1995-12-05']
donneurs = Utilisateur.objects.filter(role=Utilisateur.Role.DONNEUR)

for user in donneurs:
    profil, created = ProfilDonneur.objects.get_or_create(
        utilisateur=user,
        defaults={
            'groupe_sanguin': random.choice(GROUPES),
            'date_naissance': random.choice(date_naissances),
            'poids': random.randint(55, 79),
        }
    )

    if created:
        print(f"✔ Profil donneur créé pour {user.email}")
    else:
        print(f"ℹ Profil déjà existant pour {user.email}")

print("✅ Tous les profils donneurs sont prêts")
