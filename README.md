# capstone-statistikkur
## Was macht welche Datei? 
1. GUI.py -> öffnet das User Interface um den full DL durchzuführen
2. api_test.py -> testet die webinargeek API interaktion
3. .gitignore -> enthält informationen welche Dateien bei einem GIT push ignoriert werden sollen
4. connection_test.py -> testet die connection zur azure datenbank
5. full_dl_master.py -> herzszück um den full dl von webinargeek durchzuführen
6. sql_functions.py -> Funktionssammlung
7. t_testing.ipynb -> Notebook mit dem wir die T-tests durchgeführt haben, kann für weiteren und späteren Gebrauch umfunktioniert werden
8. wix_orders.ipynb -> lädt alle ORders vom Wixshop und speichert sie als CSV
9. wix_side_id.ipynb -> lädt alle side ids die du besitzt, wird gebraucht fpr andere WIX api calls
10. (auf Git hub nicht zu sehen) .env -> enthält alle credentials und API keys

## Wie verknüpfe ich dieses REPO mit meinem PC? 
Einen SSH Schlüssel habe ich dir schon erstellt. 
1. Packe alle bereits existierenden Daten und Dateien in einen Backup Ordner
2. Erstelle eine neue directory mit der du dieses repository verknüpfen möchtest.
3. Kopiere den SSH link der Repo. Siehe Screenshot:
![](pictures/copy_ssh_link.png)
4. Öffne Terminal und cd in die erstellte directory
5. run: git clone DEIN_SSH_LINK
6. nun solltest du alle Dateien von github auf deinem PC haben

## Welche Apis lohnen sich zu callen? 
1. Orders -> alle käufe, preise, produkte, refunds aller Kunden
2. 