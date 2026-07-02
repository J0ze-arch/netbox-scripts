import os
import io
from extras.scripts import Script, StringVar, BooleanVar
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
from netmiko import redispatch
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
            'device_type': 'terminal_server',
            'host': ip,
            'username': usuario_mikrotik,
            'password': senha,
            'port': int(porta),
        }

        arquivo_script = diretorio_pdrv7 if versao else diretorio_pdr

        self.log_info(f"Iniciando tentativa de conexão com {ip} na porta {porta}...")

        try:
            # 1. Conecta sem fazer verificações chatas de Regex
            net_connect = ConnectHandler(**device)
            self.log_info("Conexão bruta estabelecida. Executando sua ideia (Ctrl+C)...")

            import time

            net_connect.write_channel('\x03')
            time.sleep(1)

            net_connect.write_channel('\n\n')
            time.sleep(1)

            redispatch(net_connect, device_type='mikrotik_routeros')
            self.log_info("Conexão convertida para MikroTik. Iniciando script...")

            with open(arquivo_script, 'r') as f:
                comandos_limpos = [linha.replace('\n', '').strip() for linha in f.readlines() if
                                   linha.replace('\n', '').strip()]

            output = net_connect.send_config_set(comandos_limpos, read_timeout=90, cmd_verify=False)

            self.log_success("Comandos aplicados com sucesso!")
            self.log_info(f"Saída do RouterOS:\n{output}")

            net_connect.disconnect()

        except Exception as e:
            self.log_failure(f"Erro inesperado durante a execução: {str(e)}")