from extras.scripts import Script, StringVar, IntegerVar
import paramiko


class MyScript(Script):
    class Meta(Script.Meta):
        name = 'Padronização'
        description = 'Padronizador de equipamentos'
        field_order = ['ip', 'usuario', 'senha', 'porta']

    ip = StringVar(
        label='IP',
        description='IP do equipamento',
    )

    usuario = StringVar(
        label='Usuario',
        description='Insira o usuário',
    )

    senha = StringVar(
        label='Senha',
        description='Senha do equipamento',
        required=False,
    )

    porta = StringVar(
        label='Porta',
        description='Porta de acesso SSH',
    )

    def run(self, data, commit):
        ip = data['ip']
        usuario = data['usuario']
        senha = data['senha']
        porta = data['porta']

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=usuario, password=senha, look_for_keys=False, port=int(porta))

        pdr = open('/opt/netbox/netbox/scripts/pdr.txt')
        pdrLinha = pdr.readlines()

        for linha in pdrLinha:
            stdin, stdout, stderr = client.exec_command(f'/{linha}')

        client.close()