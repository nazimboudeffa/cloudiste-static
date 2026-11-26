# Comparatif des fournisseurs GPU pour CloudistePAD

**Date de vérification : 24 novembre 2026**\
**Profil cible :** quelques heures par semaine, 1080p/60 FPS, budget de
0,10 à 0,30 €/h, préférence pour un fournisseur européen et une
facturation en euros.

> **Conclusion rapide :** aucun fournisseur vérifié dans cette
> comparaison ne coche avec certitude les quatre cases à la fois --- VM
> complète compatible CloudistePAD, GPU adapté au jeu, ports UDP
> Sunshine ouverts, et facturation en euros sous 0,30 €/h.\
> Le meilleur candidat économique à tester est **Vast.ai ou
> TensorDock**, sous réserve de sélectionner une vraie VM et de vérifier
> le réseau. Pour une facturation européenne en euros, **HOSTKEY**
> mérite une demande de devis, mais ses offres GPU GeForce publiées sont
> surtout mensuelles et certaines sont indiquées « Pre-Order ».

------------------------------------------------------------------------

## 1. Ce dont CloudistePAD a réellement besoin

CloudistePAD s'appuie sur Sunshine côté serveur et Moonlight côté
client. Ce n'est pas simplement une tâche d'inférence IA : il faut une
machine utilisable comme un PC de jeu distant.

### Conditions techniques à exiger

-   VM complète x86_64/amd64, pas seulement un conteneur managé.
-   Ubuntu 22.04 ou 24.04.
-   GPU NVIDIA avec pilote fonctionnel sur l'hôte.
-   `nvidia-smi` fonctionnel et NVIDIA Container Toolkit utilisable dans
    Docker.
-   Docker et Docker Compose.
-   Accès root ou sudo et SSH.
-   IPv4 publique, ou VPN privé correctement configuré.
-   Ports entrants TCP : `47984`, `47989`, `47990`, `48010`.
-   Ports entrants UDP : `47998`, `47999`, `48000`, `48002`.
-   Latence réseau faible et débit montant stable.
-   Stockage persistant si l'on veut conserver Steam, les jeux et les
    réglages entre les sessions.

**GPU recommandé pour 1080p60 :** une GeForce RTX 3060 ou mieux. Une RTX
3090 est largement suffisante, mais probablement excessive pour cet
objectif. La compatibilité du GPU et de son encodeur NVENC doit être
vérifiée sur l'offre exacte.

------------------------------------------------------------------------

## 2. Tableau comparatif

Les prix ci-dessous sont des **repères publics relevés**, pas des devis
garantis. Les prix marketplace varient selon l'hôte, la région et la
disponibilité. Le coût total doit inclure CPU, RAM, disque, réseau,
taxes et éventuels frais de stockage.

  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  Fournisseur                                                     Type d'offre     GPU pertinents       Prix public Devise         Europe        Compatibilité CloudistePAD
                                                                                   repérés                indicatif                              
  --------------------------------------------------------------- ---------------- --------------- ---------------- -------------- ------------- --------------------------
  [Vast.ai](https://vast.ai/)                                     Marketplace de   Variable, selon Variable, offres USD            Selon hôte    **Candidat** : choisir une
                                                                  machines GPU     hôte ; parfois     à comparer en                              VM Ubuntu complète,
                                                                                   GeForce RTX               direct                              vérifier ports et
                                                                                                                                                 persistance

  [TensorDock](https://tensordock.com/)                           Marketplace / VM RTX 3090 et      RTX 3090 autour USD            Certaines     **Candidat** : vérifier
                                                                  GPU              autres selon    de 0,20 \$/h GPU                offres        VM, IP publique, UDP et
                                                                                   disponibilité           seul sur                européennes   stockage
                                                                                                     comparateurs ;                              
                                                                                                           total VM                              
                                                                                                          supérieur                              

  [HOSTKEY](https://hostkey.com/gpu-dedicated-servers/vds-gpu/)   VDS GPU /        RTX 3090, RTX           RTX 3090 EUR            Oui,          **Techniquement
                                                                  serveur virtuel  A5000, RTX 4090   affichée à 209                plusieurs     prometteur**, mais trop
                                                                                   selon catalogue   €/mois ; A5000                sites         cher pour quelques
                                                                                                       179 €/mois ;                européens     heures/semaine si facturé
                                                                                                   4090 299 €/mois,                selon offre   au mois ; vérifier
                                                                                                   certaines offres                              disponibilité et UDP
                                                                                                      « Pre-Order »                              

  [Scaleway](https://www.scaleway.com/en/gpu-instances/)          Cloud public GPU L4, L40S, H100      L4 autour de EUR            Paris,        VM cloud possible, mais
                                                                                   et autres               0,79 €/h                Varsovie      cher et GPU datacenter ;
                                                                                                                                   selon modèle  vérifier
                                                                                                                                                 affichage/virtualisation
                                                                                                                                                 et ports

  [OVHcloud](https://www.ovhcloud.com/)                           Cloud public GPU L4, L40S,           L4 autour de EUR            France et     VM possible, mais
                                                                                   A100/H100 selon         0,75 €/h                autres        largement hors budget ;
                                                                                   région                                          régions selon attention à la facturation
                                                                                                                                   gamme         des instances arrêtées

  [RunPod](https://www.runpod.io/)                                Pods GPU, cloud  RTX 3090 et            Variable, USD            Plusieurs     **À écarter pour ce
                                                                  GPU et           autres selon     généralement en                régions       déploiement précis tant
                                                                  serverless       région                       USD                européennes   que les contraintes UDP/VM
                                                                                                                                   selon offre   ne sont pas validées** ;
                                                                                                                                                 le README CloudistePAD
                                                                                                                                                 signale les
                                                                                                                                                 Pods/Serverless comme
                                                                                                                                                 incompatibles

  [Clore.ai](https://clore.ai/)                                   Marketplace de   Variable selon          Variable Généralement   Selon hôte    **À vérifier au cas par
                                                                  GPU              hôtes                            crypto / USD                 cas** : ne pas supposer
                                                                                                                    selon parcours               qu'une offre conteneurisée
                                                                                                                                                 fournit une VM complète et
                                                                                                                                                 les ports requis

  [VRAMfarm](https://vramfarm.com/)                               Location GPU     Variable selon            Tarifs EUR            Certaines     **Non adapté en l'état**
                                                                  avec             catalogue             variables,                machines      si l'offre sélectionnée
                                                                  environnements                       souvent à la                européennes   est un conteneur isolé
                                                                  et applications                            minute                              dont le disque est
                                                                  prêts à l'emploi                                                               supprimé à l'arrêt ; pas
                                                                                                                                                 l'équivalent d'une VM
                                                                                                                                                 persistante

  [Hetzner](https://www.hetzner.com/)                             Serveurs dédiés  RTX PRO         Environ 0,34 €/h EUR            Allemagne /   VM/serveur complet
                                                                  GPU              4000/6000 selon     pour RTX PRO                Finlande      possible, mais au-dessus
                                                                                   gamme           4000, avec frais                selon serveur du budget et matériel
                                                                                                     d'installation                              orienté workstation
                                                                                                       élevés selon                              
                                                                                                             modèle                              

  [Infomaniak](https://www.infomaniak.com/)                       Cloud GPU        L4, L40S, A100     Des offres L4 CHF/EUR selon  Suisse        **Piste à contacter** :
                                                                                   selon offre et           ont été facturation                  confirmer que l'offre est
                                                                                   disponibilité   signalées autour                              une VM complète, qu'elle
                                                                                                     de 0,25 €/h, à                              accepte Sunshine et que le
                                                                                                          confirmer                              prix final est bien en
                                                                                                        directement                              euros

  [SaladCloud](https://salad.com/)                                Calcul GPU       RTX 3080 Ti,             Environ USD            Selon         **Pas un choix sûr** pour
                                                                  distribué /      3090, 4080       0,20--0,27 \$/h                capacité      CloudistePAD sans preuve
                                                                  conteneurs       selon                    GPU sur                              d'une VM complète, d'une
                                                                                   disponibilité       comparateurs                              IP publique et des ports
                                                                                                                                                 UDP entrants

  [Paperspace](https://www.paperspace.com/)                       VM GPU           M4000, P4000,   0,45 à 1,38 \$/h USD            Amsterdam     **Repli pour un test** : vraie VM
                                                                  (Machines)       RTX4000, A4000, GPU seul, hors                  (AMS1)        persistante avec SSH, mais hors
                                                                                   A5000           stockage et IP                                budget ; ports UDP à confirmer

  [NovaPod](https://novapod.io/)                                  Marketplace GPU  RTX 3090, 4090, Prix « ask »     Crypto         Non précisé   **À vérifier** : seule l'option KVM
                                                                  (pods Docker ou  5090 repérées ; variables, facturés (USDT, USDC,                 root (IP publique, ports
                                                                  VM KVM root)     RTX 3060 non    à la seconde ;   ETH, SOL, BNB)               entrants ouverts selon le site)
                                                                                   vérifiée        RTX non relevés                               est pertinente ; paiement crypto
  -------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### Lecture du tableau

-   **Meilleures pistes à petit budget :** Vast.ai et TensorDock, parce
    que les marketplaces peuvent proposer des GeForce à prix compétitif.
-   **Meilleure piste de facturation en euros :** HOSTKEY pour des VDS
    GPU GeForce, mais les prix mensuels dépassent ton budget d'usage
    occasionnel. Infomaniak mérite une vérification directe, sans
    garantie de compatibilité gaming.
-   **Solutions cloud datacenter :** Scaleway et OVHcloud sont solides
    pour des VM GPU, mais leurs tarifs GPU relevés dépassent ton plafond
    de 0,30 €/h.
-   **Paperspace :** vraie VM persistante à Amsterdam, mais à partir de
    0,45 $/h pour le GPU seul, donc hors budget et en dollars.
-   **NovaPod :** marketplace à tarifs « live » facturés à la seconde,
    paiement uniquement en crypto. Seule son option VM KVM root est
    envisageable pour CloudistePAD.
-   **Offres conteneurisées :** elles ne sont pas interchangeables avec
    une VM gaming. Une image Docker avec GPU ne suffit pas à faire
    fonctionner un bureau complet, Steam, Sunshine et les connexions
    Moonlight.

------------------------------------------------------------------------

## 3. Analyse des candidats les plus pertinents

### A. Vast.ai --- meilleur potentiel de prix

**Pourquoi le considérer** - Marketplace où le prix et le matériel
varient selon les hôtes. - Possibilité de trouver des GPU GeForce
adaptés au jeu. - Le dépôt CloudistePAD recommande une VM Ubuntu, et non
une instance Docker seule.

**Risques** - Qualité, réseau et disponibilité dépendants de l'hôte. -
Ports publics parfois remappés ou limités ; le dépôt suggère Tailscale
comme contournement possible. - Tarification en dollars américains. -
Vérifier le coût total, y compris stockage et réseau. - Arrêter le
conteneur ne signifie pas nécessairement arrêter la facturation de la
VM.

**Verdict :** premier candidat à tester si le prix prime sur la
facturation en euros. Ne louer qu'après avoir vérifié les ports et la
nature exacte de l'instance.

### B. TensorDock --- candidat marketplace à comparer avec Vast.ai

**Pourquoi le considérer** - Déploiement de VM GPU et choix de
ressources. - Présence d'offres GeForce, notamment RTX 3090 selon
disponibilité. - Facturation au prorata annoncée par la plateforme.

**Risques** - Prix affichés en dollars. - L'offre disponible dépend du
fournisseur/hôte et de la région. - Vérifier que le modèle choisi donne
bien une VM complète, un accès SSH/root, une IP publique et des ports
UDP entrants. - Confirmer la persistance du disque et le coût lorsque la
machine est arrêtée.

**Verdict :** deuxième candidat à mettre en concurrence avec Vast.ai. Le
prix « GPU seul » n'est pas le prix final de la VM.

### C. HOSTKEY --- intéressant pour l'euro, moins pour ton rythme

Catalogue public relevé : - RTX 3090 24 Go : environ 209 €/mois. - RTX
A5000 24 Go : environ 179 €/mois. - RTX 4090 24 Go : environ 299
€/mois. - Plusieurs configurations sont indiquées « Pre-Order ».

Ces offres sont plus proches d'un serveur GPU permanent que d'une
location économique pour quelques heures par semaine. Vérifier si une
vraie option horaire est disponible pour le modèle souhaité. Attention :
selon les conditions horaires publiées, éteindre la machine ne met pas
forcément fin à la facturation ; la résiliation peut détruire le
serveur.

**Verdict :** pas mon choix pour un usage de quelques heures par semaine
au budget annoncé.

### D. Scaleway et OVHcloud --- fiables, mais hors budget

Les tarifs publics relevés pour les GPU L4 sont de l'ordre de 0,75 à
0,79 €/h, soit environ 2,5 fois ou plus ton plafond horaire. Ce sont des
GPU datacenter, pas nécessairement le meilleur choix pour un PC gaming
distant. Ils restent intéressants si tu privilégies un cloud européen
avec facturation en euros et acceptes un budget supérieur.

**Verdict :** écarter pour le budget actuel.

### E. Paperspace --- vraie VM GPU persistante, mais trop chère pour ton budget

Paperspace (désormais documenté dans l'écosystème DigitalOcean) mérite
d'être inclus car son produit **Machines** est bien une machine
virtuelle Linux ou Windows avec GPU, stockage persistant, possibilité
d'ajouter une IP publique et accès SSH. Ce n'est donc pas seulement une
offre de notebooks ou de conteneurs IA. Les régions Machines incluent
Amsterdam (AMS1), ce qui est intéressant depuis la France.
[Documentation
Machines](https://docs.digitalocean.com/products/paperspace/) ·
[Régions](https://github.com/Paperspace/CORE-API-Docs/blob/master/api-documentation/machines/README.md).

**Tarifs GPU horaires publiés** (prix en dollars, hors stockage et IP)
: - M4000 : **0,45 \$/h** - P4000 : **0,51 \$/h** - RTX4000 : **0,56
\$/h** - P5000 : **0,78 \$/h** - A4000 : **0,76 \$/h** - A5000 : **1,38
\$/h**

Même le modèle GPU le moins cher dépasse déjà ton plafond de 0,30 €/h
avant conversion, stockage et IP. Les GPU proposés sont par ailleurs des
cartes workstation/datacenter plutôt que les GeForce RTX 3060/3090 que
je privilégierais pour un PC gaming distant. La page tarifaire décrit
certains modèles comme adaptés aux applications 3D et au gaming, mais
cela ne garantit pas une expérience Sunshine/Moonlight optimisée.
[Tarifs
officiels](https://docs.digitalocean.com/products/paperspace/pricing/).

**Points positifs** - VM Linux complète et stockage persistant. - SSH et
possibilité d'ajouter une IP publique. - Datacenter d'Amsterdam, donc
potentiellement une latence correcte depuis la France. - La facturation
du calcul GPU s'arrête lorsque la machine est éteinte ; le stockage
attaché et l'IP publique continuent toutefois à être facturés. Pour
supprimer tous les frais, il faut détruire les ressources. [Règles de
facturation](https://docs.digitalocean.com/products/paperspace/pricing/)
· [Gestion des IP
publiques](https://docs.digitalocean.com/products/paperspace/machines/how-to/manage-public-ips/).

**Points de vigilance** - Le tarif minimal GPU publié est 0,45 \$/h :
hors budget. - Facturation en USD, pas en euros. - Les templates Windows
ont été dépréciés pour les nouveaux utilisateurs ; privilégier une VM
Linux et installer les composants nécessaires. [État des produits
Paperspace](https://docs.digitalocean.com/products/paperspace/). - Je
n'ai pas trouvé de confirmation officielle suffisante que les ports UDP
Sunshine requis soient ouverts sans restriction. Il faut demander
confirmation avant de commander. - La documentation présente les
Machines comme orientées HPC/IA ; ce n'est pas une offre commercialisée
spécifiquement comme PC gaming cloud.

**Verdict :** Paperspace est techniquement plus crédible que les
plateformes de conteneurs GPU, car il fournit une vraie VM persistante
avec région européenne. En revanche, il ne correspond pas à ton budget
ni à ta préférence de facturation en euros. Je le classerais comme
**solution de repli pour un test**, pas comme recommandation principale.

### F. NovaPod --- marketplace crypto, seule l'option KVM est envisageable

*Informations relevées sur le site officiel le 26 novembre 2026 ; je n'ai
pas pu en vérifier les affirmations de façon indépendante.*

NovaPod propose deux modes : des **pods Docker** (démarrage en moins de
15 s) et des **VM KVM root** avec disque NVMe persistant, IPv4 publique
dédiée et pare-feu configurable. Le site annonce Ubuntu 24.04, Debian 12
ou Windows Server GPU, et une facturation à la seconde. Une VM arrêtée
ne coûte que le stockage « en veille ». [Site
NovaPod](https://novapod.io/) · [Documentation](https://docs.novapod.io)

**Points positifs** - L'option KVM correspond au profil requis : VM
complète, root/SSH, IP publique, persistance du disque. - Facturation à
la seconde, sans minimum ni engagement. - Des GeForce (RTX 3090, 4090,
5090) sont citées parmi les GPU disponibles.

**Points de vigilance** - **Paiement uniquement en crypto** (USDT, USDC,
ETH, SOL, BNB) : pas de facturation en euros ni de facture avec TVA
classique, ce qui va à l'encontre de ta préférence. - Je n'ai pas relevé
de prix pour une GeForce adaptée (RTX 3060 ou équivalent) : les tarifs
sont des « asks » en direct, et les montants mis en avant concernent
surtout des GPU datacenter. - Aucune région européenne n'est indiquée
sur la page d'accueil. - Les pods Docker sont à écarter pour Sunshine
(redirection de ports dynamique, noyau partagé). - Les ports UDP
Sunshine ne sont pas explicitement confirmés : le site mentionne
seulement des « ports entrants ouverts » sur les KVM. - Le dépôt
CloudistePAD ne mentionne pas ce fournisseur.

**Verdict :** à tester uniquement si le paiement en crypto ne te gêne
pas et si une RTX 3060/3090 en KVM s'affiche sous 0,30 \$/h. À défaut,
il reste derrière Vast.ai et TensorDock.

### G. RunPod, Clore.ai, VRAMfarm et SaladCloud

Ces services peuvent être intéressants pour louer de la puissance GPU,
lancer des conteneurs ou exécuter des applications IA. Mais CloudistePAD
demande un environnement de PC distant avec accès réseau entrant et une
VM suffisamment complète. Il faut donc examiner le produit exact, et pas
seulement la présence d'un GPU NVIDIA.

**Verdict :** ne pas les retenir sans confirmation explicite d'une VM
complète, de l'accès réseau Sunshine et de la persistance.

------------------------------------------------------------------------

## 4. Configuration cible à demander

Pour du 1080p60 avec quelques heures de jeu par semaine :

  -----------------------------------------------------------------------
  Ressource               Minimum raisonnable     Cible conseillée
  ----------------------- ----------------------- -----------------------
  GPU                     RTX 3060 12 Go          RTX 3060 12 Go ou RTX
                                                  3090 si l'offre est
                                                  très économique

  CPU                     4 vCPU                  6 vCPU

  RAM                     8 Go                    16 Go

  Disque                  100 Go SSD              150--200 Go NVMe

  OS                      Ubuntu 22.04 amd64      Ubuntu 22.04/24.04
                                                  amd64

  Réseau                  IPv4 publique           IPv4 publique, faible
                                                  latence, UDP entrant

  Accès                   SSH                     Root/sudo + SSH

  Conteneurs              Docker                  Docker + Docker
                                                  Compose + NVIDIA
                                                  Container Toolkit
  -----------------------------------------------------------------------

**Important :** la RTX 3090 est un bon GPU gaming, mais elle consomme
davantage et peut coûter plus cher. Pour du 1080p60, une RTX 3060 ou une
carte de niveau similaire suffit généralement. Il vaut mieux payer pour
une bonne connexion réseau et un hôte stable que pour un GPU
surdimensionné.

------------------------------------------------------------------------

## 5. Budget correspondant à ton utilisation

Ton budget est de 0,10 à 0,30 €/h. Voici le coût de calcul pur, hors
stockage, taxes, réseau et éventuels frais fixes :

  Utilisation                     À 0,10 €/h   À 0,20 €/h   À 0,30 €/h
  ----------------------------- ------------ ------------ ------------
  4 h/semaine (\~17,3 h/mois)         1,73 €       3,46 €       5,19 €
  6 h/semaine (\~26 h/mois)           2,60 €       5,20 €       7,80 €
  8 h/semaine (\~34,7 h/mois)         3,47 €       6,94 €      10,41 €

À ce niveau d'utilisation, un abonnement mensuel de 179 à 299 € n'a pas
de sens économique. Il faut privilégier une location réellement facturée
à l'heure ou à la seconde, avec stockage persistant à coût raisonnable.

------------------------------------------------------------------------

## 6. Checklist avant de louer

Envoyer ces questions au fournisseur ou à l'hôte avant tout paiement :

1.  Est-ce une **VM complète** (et non un simple conteneur) avec Ubuntu
    22.04/24.04 amd64 ?
2.  Ai-je accès à SSH et root/sudo ?
3.  Le pilote NVIDIA est-il installé et `nvidia-smi` fonctionne-t-il ?
4.  Puis-je installer Docker Compose et NVIDIA Container Toolkit ?
5.  L'adresse IPv4 est-elle publique et dédiée à mon instance ?
6.  Les ports TCP `47984`, `47989`, `47990`, `48010` sont-ils
    accessibles depuis Internet ?
7.  Les ports UDP `47998`, `47999`, `48000`, `48002` sont-ils
    accessibles depuis Internet, sans filtrage ?
8.  Le disque système et les jeux Steam restent-ils conservés après
    arrêt/redémarrage ?
9.  Quel est le coût total avec 6 vCPU, 16 Go RAM, 150--200 Go NVMe et
    IPv4 ?
10. Quel est le coût exact lorsque la VM est arrêtée ? Le stockage et
    l'adresse IP restent-ils facturés ?
11. La facturation est-elle réellement en euros, avec facture et TVA
    adaptées à mon pays ?
12. Puis-je tester pendant une heure et résilier sans frais ni
    engagement ?

### Message prêt à envoyer au support

> Bonjour,
>
> Je souhaite louer une machine pour du cloud gaming avec CloudistePAD,
> Sunshine et Moonlight.
>
> Je cherche une VM complète Ubuntu 22.04/24.04 amd64, avec GPU NVIDIA
> (idéalement RTX 3060 12 Go ou équivalent), 6 vCPU, 16 Go de RAM,
> 150--200 Go NVMe, accès root/SSH et IPv4 publique.
>
> Pouvez-vous confirmer que je peux installer Docker Compose et NVIDIA
> Container Toolkit, et que les ports TCP 47984, 47989, 47990, 48010
> ainsi que UDP 47998, 47999, 48000 et 48002 sont accessibles depuis
> Internet ?
>
> Le disque et les jeux restent-ils persistants après arrêt de la VM ?
> Quel est le coût total horaire, stockage et IPv4 compris, et quelle
> facturation s'applique lorsque la VM est arrêtée ?
>
> Je privilégie une facturation en euros et une localisation en Europe.
>
> Merci.

------------------------------------------------------------------------

## 7. Sources et liens à vérifier

-   [CloudistePAD --- dépôt
    GitHub](https://github.com/nazimboudeffa/cloudiste-pad)
-   [Vast.ai --- marketplace](https://vast.ai/)
-   [Vast.ai --- guide de tarification
    GPU](https://vast.ai/article/how-much-does-it-cost-to-rent-a-gpu-in-the-cloud-live-pricing-guide)
-   [TensorDock --- déployer une VM
    GPU](https://console.tensordock.com/deploy)
-   [HOSTKEY --- VDS
    GPU](https://hostkey.com/gpu-dedicated-servers/vds-gpu/)
-   [Scaleway --- GPU
    Instances](https://www.scaleway.com/en/gpu-instances/)
-   [OVHcloud --- Public Cloud](https://www.ovhcloud.com/)
-   [RunPod](https://www.runpod.io/)
-   [Clore.ai](https://clore.ai/)
-   [VRAMfarm](https://vramfarm.com/)
-   [Hetzner](https://www.hetzner.com/)
-   [Infomaniak](https://www.infomaniak.com/)
-   [SaladCloud](https://salad.com/)
-   [Paperspace](https://www.paperspace.com/)
-   [NovaPod](https://novapod.io/) et sa
    [documentation](https://docs.novapod.io)
-   [Panorama des GPU cloud en Europe --- tarifs et
    régions](https://vramfarm.com/fr/blog/gpu-cloud-europe/)
-   [Comparatif de fournisseurs GPU
    cloud](https://vramfarm.com/en/compare/)
-   [GPU Radar --- offres GPU en
    Europe](https://www.gpuradar.eu/hosting)

**Note Paperspace :** les prix GPU cités proviennent du barème officiel
publié par Paperspace/DigitalOcean et sont en USD. La facturation GPU
s'arrête à l'extinction de la machine, mais stockage et IP restent
facturés tant qu'ils sont attachés.

**Note méthodologique :** les pages de comparaison et les catalogues
évoluent rapidement. Les prix sont des instantanés et certains
comparateurs ne donnent que le prix du GPU, pas celui de la machine
complète. Les points décisifs pour CloudistePAD --- VM complète, ports
UDP entrants, persistance et latence --- doivent être confirmés auprès
du fournisseur avant paiement.
