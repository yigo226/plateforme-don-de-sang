# Compatibilité DONNEUR ➜ RECEVEUR

COMPATIBILITE_SANG = {
    'O-': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
    'O+': ['O+', 'A+', 'B+', 'AB+'],
    'A-': ['A-', 'A+', 'AB-', 'AB+'],
    'A+': ['A+', 'AB+'],
    'B-': ['B-', 'B+', 'AB-', 'AB+'],
    'B+': ['B+', 'AB+'],
    'AB-': ['AB-', 'AB+'],
    'AB+': ['AB+'],
}

def donneur_peut_donner(groupe_donneur, groupe_receveur):
    """
    Retourne True si le donneur est compatible avec le receveur
    """
    return groupe_receveur in COMPATIBILITE_SANG.get(groupe_donneur, [])


def groupes_receveurs_compatibles(groupe_donneur):
    """
    Liste des groupes sanguins que ce donneur peut aider
    """
    return COMPATIBILITE_SANG.get(groupe_donneur, [])
