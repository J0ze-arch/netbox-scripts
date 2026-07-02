import os
from extras.scripts import Script, StringVar, BooleanVar
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


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

        # 1. Adicionando as flags +ct para evitar quebra de regex por cores
        usuario_mikrotik = f"{usuario}+ct"

        device = {
            'device_type': 'mikrotik_routeros',
            'host': ip,
            'username': usuario_mikrotik,
            'password': senha,
            'port': int(porta),
            'global_delay_factor': 2,  # Dá mais tempo para o equipamento processar os comandos
        }

        arquivo_script = diretorio_pdrv7 if versao else diretorio_pdr

        self.log_info(f"Iniciando tentativa de conexão com {ip} na porta {porta}...")

        try:
            net_connect = ConnectHandler(**device)
            self.log_success(f"Conexão SSH estabelecida com sucesso em {ip}!")

            self.log_info(f"Lendo e aplicando o script: {arquivo_script}")

            # Se o script alterar o hostname, o Netmiko perde o prompt.
            # Para evitar isso, lemos o arquivo e enviamos comando por comando,
            # avisando o Netmiko para ser menos rigoroso com o prompt de retorno.
            with open(arquivo_script, 'r') as f:
                comandos = f.readlines()

            # Remove quebras de linha e comandos vazios
            comandos_limpos = [cmd.strip() for cmd in comandos if cmd.strip()]

            # send_config_set é mais robusto para scripts que alteram o prompt
            output = net_connect.send_config_set(comandos_limpos, read_timeout=90)

            self.log_success("Comandos aplicados com sucesso!")
            self.log_info(f"Saída do terminal RouterOS:\n{output}")

            net_connect.disconnect()
            self.log_info("Sessão SSH encerrada.")

        except Exception as e:
            self.log_failure(f"Ocorreu um erro durante a execução: {str(e)}")