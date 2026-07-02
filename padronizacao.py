import os
from extras.scripts import Script, StringVar, BooleanVar
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import time


class MyScript(Script):
    class Meta(Script.Meta):
        name = 'Padronização'
        description = 'Padronizador de equipamentos (Migração Netmiko)'
        field_order = ['ip', 'usuario', 'senha', 'porta', 'versao']

    ip = StringVar(
        label='IP',
        description='IP do equipamento',
    )

    usuario = StringVar(
        label='Usuário',
        description='Insira o usuário (ex: admin)',
    )

    senha = StringVar(
        label='Senha',
        description='Senha do equipamento',
        required=False,
    )

    porta = StringVar(
        label='Porta',
        description='Porta de acesso SSH',
        default='22'
    )

    versao = BooleanVar(
        label='RouterOS V7+',
        description='Marque se o equipamento estiver rodando RouterOS v7 ou superior'
    )

    def run(self, data, commit):

        diretorio = os.path.dirname(os.path.abspath(__file__))
        diretorio_pdr = os.path.join(diretorio, 'scripts/pdr.txt')
        diretorio_pdrv7 = os.path.join(diretorio, 'scripts/pdrv7.txt')

        ip = data['ip']
        usuario = data['usuario']
        senha = data.get('senha', '')
        porta = data['porta']
        versao = data['versao']

        usuario_mikrotik = f"{usuario}+ct"

        device = {
            'device_type': 'mikrotik_routeros',
            'host': ip,
            'username': usuario_mikrotik,
            'password': senha,
            'port': int(porta),
            'global_delay_factor': 4,
            'session_timeout': 60,
        }

        arquivo_script = diretorio_pdrv7 if versao else diretorio_pdr

        self.log_info(f"Iniciando tentativa de conexão com {ip} na porta {porta}...")

        try:
            net_connect = ConnectHandler(**device)

            tela_inicial = net_connect.read_channel()

            if "software license" in tela_inicial or "Enter" in tela_inicial:
                self.log_info("Equipamento de fábrica detectado. Passando pela licença...")
                net_connect.write_channel("n\n")
                time.sleep(1)

                # Envia o "Enter" caso ele peça especificamente
                net_connect.write_channel("\n")
                time.sleep(1)

                # Se for RouterOS v7, ele vai pedir senha nova. Podemos setar a mesma do formulário.
                tela_senha = net_connect.read_channel()
                if "new password" in tela_senha:
                    net_connect.write_channel(f"{senha}\n")
                    time.sleep(1)
                    net_connect.write_channel(f"{senha}\n")
                    time.sleep(1)

            self.log_success(f"Conexão estabelecida{ip}!")

            self.log_info(f"Padronizando...")

            with open(arquivo_script, 'r') as f:
                comandos = f.readlines()

            comandos_limpos = [cmd.strip() for cmd in comandos if cmd.strip()]

            output = net_connect.send_config_set(comandos_limpos, read_timeout=90, cmd_verify=False)

            self.log_success("Equipamento padronizado!")

            net_connect.disconnect()

        except Exception as e:
            self.log_failure(f"Ocorreu um erro durante a execução: {str(e)}")