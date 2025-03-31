import socket
import threading
import requests

# Configuration
MINECRAFT_SERVER = ("fbft.fr", 25565)  # IP du serveur
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1356315376383692881/Glh1WLEZFs_4u4QsN7jONJDdKKzWsmDk0bB0AfU2A-Zjd5vJ_ftyD2iDS0CCWWYqwheX"  # Remplace par ton Webhook Discord
PROXY_HOST = "0.0.0.0"  # Proxy ouvert à tous
PROXY_PORT = 25566  # Port du proxy

def forward_data(source, destination):
    """Transfère les données entre le client et le serveur."""
    while True:
        data = source.recv(4096)
        if not data:
            break
        destination.sendall(data)

        # Vérification si c'est un message de chat
        if b'\x02' in data:  # Vérification basique du format des messages
            try:
                message = data.decode('utf-8', errors='ignore')
                if "chat" in message.lower():
                    send_to_discord(message)
            except:
                pass

def send_to_discord(message):
    """Envoie le message sur Discord via Webhook."""
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK, json=data)

def handle_client(client_socket):
    """Gère une connexion au proxy."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(MINECRAFT_SERVER)
    
    client_thread = threading.Thread(target=forward_data, args=(client_socket, server_socket))
    server_thread = threading.Thread(target=forward_data, args=(server_socket, client_socket))
    
    client_thread.start()
    server_thread.start()
    
    client_thread.join()
    server_thread.join()

def start_proxy():
    """Démarre le proxy."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((PROXY_HOST, PROXY_PORT))
    server.listen(5)
    print(f"Proxy en écoute sur {PROXY_HOST}:{PROXY_PORT}...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connexion de {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_proxy()
