import random
from django.core.management.base import BaseCommand
from comptes.models import Utilisateur
from donneurs.models import ProfilDonneur

class Command(BaseCommand):
    help = "Génère des utilisateurs fictifs pour les tests"

    def handle(self, *args, **options):
        NOMS = ["Issa", "Zando", "Detro", "Moussa", "Abdou", "Salif", "Oumar"]
        VILLES = ["Ouagadougou", "Bobo", "Koudougou", "Banfora"]
        GROUPES = ['A+', 'A-', 'B+', 'O+', 'O-', 'AB+']

        PASSWORD = "12345678op"
        NB_USERS = 30

        for i in range(NB_USERS):
            nom = random.choice(NOMS)
            prenom = f"Test{i}"
            email = f"{nom.lower()}{i}@test.com"

            if Utilisateur.objects.filter(email=email).exists():
                continue

            role = random.choice([
                Utilisateur.Role.DEMANDEUR,
                Utilisateur.Role.DONNEUR,
            ])

            user = Utilisateur.objects.create_user(
                email=email,
                password=PASSWORD,
                first_name=prenom,
                last_name=nom,
                ville=random.choice(VILLES),
                role=role,
            )

            # 👉 Si donneur → créer profil donneur
            if role == Utilisateur.Role.DONNEUR:
                ProfilDonneur.objects.create(
                    utilisateur=user,
                    groupe_sanguin=random.choice(GROUPES),
                    poids=random.randint(55, 90),
                    ville=user.ville,
                )

            self.stdout.write(
                self.style.SUCCESS(f"✔ {email} ({role})")
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\n🎉 {NB_USERS} utilisateurs générés "
                f"(mot de passe unique : {PASSWORD})"
            )
        )
