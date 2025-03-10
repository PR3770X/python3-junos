import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time



# Configurações
router_ip = "IP_DO_ROTEADOR"
router_user = "SEU_USUARIO"
router_password = "SENHA_DO_USUARIO"
root_password = "12345678"
email_from = "seu_email@exemplo.com"
email_to = ["destinatario1@dominio.com", "destinatario2@dominio.com", "destinatario3@dominio.com"]  # Lista de destinatários
email_password = "SENHA_DO_EMAIL"
smtp_server = "smtp.exemplo.com"
smtp_port = 587

# Função para enviar e-mail
def enviar_email(assunto, mensagem):
    print("[DEBUG] Preparando para enviar e-mail...")
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = email_from
    msg["To"] = email_to

    try:
        print(f"[DEBUG] Conectando ao servidor SMTP: {smtp_server}:{smtp_port}...")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            print("[DEBUG] Iniciando TLS...")
            server.starttls()
            print("[DEBUG] Realizando login no servidor SMTP...")
            server.login(email_from, email_password)
            print("[DEBUG] Enviando e-mail...")
            server.sendmail(email_from, email_to, msg.as_string())
        print("[DEBUG] E-mail enviado com sucesso!")
    except smtplib.SMTPConnectError as e:
        print(f"[ERRO] Falha ao conectar ao servidor SMTP: {e}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERRO] Falha de autenticação no servidor SMTP: {e}")
    except Exception as e:
        print(f"[ERRO] Erro ao enviar e-mail: {e}")

# Funcao para enviar e-mail
def enviar_email(assunto, mensagem):
    print("[DEBUG] Preparando para enviar e-mail...")
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = email_from
    msg["To"] = ", ".join(email_to)  # Concatena os e-mails com virgula

    try:
        print(f"[DEBUG] Conectando ao servidor SMTP: {smtp_server}:{smtp_port}...")
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            #print("[DEBUG] Iniciando TLS...")
            #server.starttls()
            print("[DEBUG] Realizando login no servidor SMTP...")
            server.login(email_from, email_password)
            print("[DEBUG] Enviando e-mail...")
            server.sendmail(email_from, email_to, msg.as_string())
        print("[DEBUG] E-mail enviado com sucesso!")
    except smtplib.SMTPConnectError as e:
        print(f"[ERRO] Falha ao conectar ao servidor SMTP: {e}")
    except smtplib.SMTPAuthenticationError as e:
        print(f"[ERRO] Falha de autenticacao servidor SMTP: {e}")
    except Exception as e:
        print(f"[ERRO] Erro ao enviar e-mail: {e}")

# Conexao SSH
try:
    print("[DEBUG] Iniciando conexao SSH com o roteador...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print(f"[DEBUG] Conectando ao roteador {router_ip} como usuario {router_user}...")
    ssh.connect(router_ip, username=router_user, password=router_password)
    print("[DEBUG] Conexao SSH estabelecida com sucesso!")

    print("[DEBUG] Abrindo canal SSH...")
    channel = ssh.invoke_shell()
    print("[DEBUG] Executando comando 'start shell user root'...")
    channel.send("start shell user root\n")
    time.sleep(1)  # Aguarda o roteador processar o comando
    print("[DEBUG] Inserindo senha do root...")
    channel.send(f"{root_password}\n")
    time.sleep(1)
    print("[DEBUG] Executando comando 'sh /root/bbe-smgd.sh'...")
    channel.send("sh /root/bbe-smgd.sh\n")
    time.sleep(5)  # Aguarda a execucao do script
    print("[DEBUG] Saindo do shell...")
    channel.send("exit\n")
    time.sleep(1)
    channel.send("exit\n")
    time.sleep(1)

    print("[DEBUG] Fechando conexao SSH...")
    ssh.close()
    print("[DEBUG] Conexao SSH fechada.")

    # Envia e-mail de confirmação
    print("[DEBUG] Preparando para enviar e-mail de confirmacao...")
    enviar_email(
        "Relatorio de Execucao",
        f"O comando kill foi executado com sucesso no roteador {router_ip}."
    )

except paramiko.AuthenticationException:
    print("[ERRO] Falha na autenticacao SSH. Verifique o usuario e senha.")
except paramiko.SSHException as e:
    print(f"[ERRO] Erro na conexao SSH: {e}")
except Exception as e:
    print(f"[ERRO] Erro durante a execucao: {e}")
