# winrm_executor.py

import winrm

# --- Paramètres de connexion WinRM ---
# Remplacez ces valeurs par l'IP et les identifiants de votre machine Windows
WINRM_HOST = 'http://192.168.30.101:5985/wsman'
WINRM_USER = 'svc_logstash'  # L'utilisateur que vous avez créé
WINRM_PASS = '' # Le mot de passe de l'utilisateur

def execute_remote_command(host, user, password, command):
    """
    Établit une connexion WinRM et exécute une commande PowerShell.
    """
    try:
        # Création de la session WinRM
        # La connexion par défaut est non sécurisée (HTTP sur port 5985) pour les tests internes.
        # Utilisez HTTPS (port 5986) pour la production.
        session = winrm.Session(
            host,
            auth=(user, password),
            transport='ntlm' # NTLM est généralement utilisé dans les domaines Windows
        )

        print(f"Tentative d'exécution de la commande '{command}' sur {host}...")
        
        # Exécution de la commande
        result = session.run_cmd(command)

        # Affichage des résultats
        print("\n--- Résultat de la commande ---")
        print(f"Statut de sortie (Exit Code): {result.status_code}")
        print("\nSortie Standard (Stdout):")
        print(result.std_out.decode('utf-8'))
        print("\nErreur Standard (Stderr):")
        print(result.std_err.decode('utf-8'))
        print("------------------------------")

    except winrm.exceptions.WinRMError as e:
        print(f"Erreur de connexion/exécution WinRM : {e}")
        print("Veuillez vérifier : 1. WinRM est activé sur le serveur Windows. 2. Le pare-feu autorise le port 5985 (ou 5986). 3. Les identifiants sont corrects.")
    except Exception as e:
        print(f"Une erreur inattendue s'est produite : {e}")

if __name__ == "__main__":
    # Commande simple à exécuter
    target_command = 'hostname'
    
    # Exécuter la fonction
    execute_remote_command(WINRM_HOST, WINRM_USER, WINRM_PASS, target_command)
