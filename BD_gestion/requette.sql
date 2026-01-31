USE don_sang_db;
DELETE FROM dons_don;

# Tous les comptes ( utilisateurs )
select * from comptes_utilisateur;
# Toute les prodils donneurs
SELECT * FROM donneurs_profildonneur;
# Tous les hopitaux
 select * from hopitaux_hopital;
#
select * from dons_don;

# Afficher des utilisateurs  ayant le groupes sanguin x
SELECT 
    d.id,
    d.date_don,
    d.volume_ml,
    d.valide,
    pd.groupe_sanguin,
    u.email,
    u.ville
FROM dons_don d
JOIN donneurs_profildonneur pd ON d.donneur_id = pd.id
JOIN comptes_utilisateur u ON pd.utilisateur_id = u.id
WHERE pd.groupe_sanguin = 'O-';

# Total de collecter par groupe sanguin
SELECT 
    pd.groupe_sanguin,
    COUNT(*) AS nombre_dons,
    SUM(d.volume_ml) AS volume_total
FROM dons_don d
JOIN donneurs_profildonneur pd ON d.donneur_id = pd.id
WHERE d.valide = 1
GROUP BY pd.groupe_sanguin;

# 
SELECT 
    u.id,
    u.last_name AS nom,
    u.first_name AS prenom,
    u.email,
    u.ville,
    pd.groupe_sanguin
FROM comptes_utilisateur u
INNER JOIN donneurs_profildonneur pd ON u.id = pd.utilisateur_id
WHERE pd.groupe_sanguin = 'B-';


