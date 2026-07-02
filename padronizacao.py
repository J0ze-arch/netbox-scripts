import os
from extras.scripts import Script, StringVar, BooleanVar
import paramiko


class MyScript(Script):
    class Meta(Script.Meta):
        name = 'Padronização'
        description = 'Padronizador de equipamentos BrasilNET'
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
        diretorioPdr = os.path.join(diretorio, 'scripts/pdr.txt')
        diretorioPdrV7 = os.path.join(diretorio, 'scripts/pdrv7.txt')

        ip = data['ip']
        usuario = data['usuario']
        senha = data.get('senha', '')
        porta = data['porta']
        versao = data['versao']

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(ip, username=usuario, password=senha, look_for_keys=False, port=int(porta))

        if versao == true:

            pdr = open(diretorioPdrV7)
            pdrLinha = pdr.readlines()

            for linha in pdrLinha:
                stdin, stdout, stderr = client.exec_command(linha)

            client.close()

            self.log_success("Equipamento padronizado com sucesso ✅!")

        else:

            pdr = open(diretorioPdr)
            pdrLinha = pdr.readlines()

            for linha in pdrLinha:
                stdin, stdout, stderr = client.exec_command(linha)

            client.close()

            self.log_success("Equipamento padronizado com sucesso ✅!")