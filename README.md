# carpool-app

## SPECS:
La société Nextech souhaite réaliser une plateforme de covoiturage pour ses étudiants. Le besoin se découpe donc en 4 parties distinctes pour la même application, le tout s’articulant autour d’une base de données commune.

### Application Covoit FrontOffice - Client Léger
* Les étudiants peuvent se connecter (pas s’inscrire) sur la plateforme web avec leurs identifiants
* La connexion doit pouvoir être maintenue si il revient plus tard
* Ils peuvent renseigner leur véhicule et le nombre de place disponibles
* Créer des trajets entre deux points et les rendres récurrents (avec une temporalité hebdomadaire au choix)
* Visualiser les trajets existants avec la possibilité de les filtrer par lieu de départ et/ou d'arrivée, les trajets complets n’apparaîtront que si un filtre spécifique est coché.
* S’inscrire sur un trajet de façon ponctuelle ou récurrente
* Avoir un historique des trajets sur lesquels ils sont inscrits pour révoquer cette inscription
* Envoyer un message et communiquer entre eux (conducteur / passager)
* Modifier leur mot de passe et leurs informations

### Application Covoit BackOffice - Client Léger
* Les administrateurs/modérateurs disposent d’un compte sur le site web pour se connecter au backoffice de façon sécurisée
* La connexion doit pouvoir être maintenue si il revient plus tard
* Ils peuvent consulter tous les trajets proposés et les historiques
* Ils peuvent supprimer des trajets existants ou des inscriptions de passager

### Application Covoit BackOffice - Client Lourd
* Les administrateurs disposent des mêmes accès pour se connecter via le client lourd
* Le client lourd ne doit pas être accessible aux modérateurs
* La connexion doit pouvoir être maintenue si il revient plus tard
* Les administrateurs peuvent visualiser la liste des étudiants inscrits et pouvoir les modifiers, les supprimer (par lot) ou désactiver les comptes
* Il doit être possible d'ajouter manuellement un utilisateur
* Il doit être possible d’importer un fichier .csv pour créer automatiquement les comptes utilisateur
* A chaque création d’un compte utilisateur un mot de passe sécurisé est généré par le système et envoyer par mail à l’étudiant Application Covoit FrontOffice - Mobile
* Une application mobile doit être développé et proposer des fonctionnalités allégé par rapport au client léger, on attend uniquement la possibilité de réserver / annuler un trajet avec les mêmes filtres que sur le client léger

### Application Covoit Base de donnée
* Une base de données commune aux 4 applications doit être implémenter, l’analyse doit être réalisée en amont. Il est demandé que la base de données possède au minimum 1 trigger et une procédure/fonction stockées (de votre choix).
* Le stockage des mots de passe doit être sécurisé
* Les données personnel doivent être chiffré dans la base
Il doit exister une table d’historique permettant de savoir quel administrateur et quand a procédé à des modification / consultation / suppression des données personnel d’un étudiant

