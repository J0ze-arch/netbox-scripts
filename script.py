from extras.scripts import Script, StringVar, IntegerVar
import paramiko
import os


class PadronizarEquipamento(Script):
    class Meta:
        name = "Padronização de Equipamento de Rede"
        description = "Aplica configurações padrão BrasilNET."
        commit_default = True

    ip_address = StringVar(
        description="Endereço IP",
        label="IP do Equipamento",
        required=True
    )

    port = IntegerVar(
        description="Porta de acesso (ex: 22 para SSH)",
        label="Porta de Acesso",
        default=22,
        required=True
    )

    username = StringVar(
        description="Usuário",
        label="Usuário",
        required=True
    )

    password = StringVar(
        description="Senha",
        label="Senha",
        required=True
    )

    def run(self, data, commit):

        diretorio = os.path.dirname(os.path.abspath(__file__))
        diretorioPdr = os.path.join(diretorio, 'scripts/pdr.txt')

        ip = data.get('ip_address')
        porta = data.get('port')
        usuario = data.get('username')
        senha = data.get('password')

        self.log_info("### 📋 Resumo da Solicitação")

        tabela_dados = (
            f"| Parâmetro | Valor Informado |\n"
            f"| :--- | :--- |\n"
            f"| **IP do Dispositivo** | `{ip}` |\n"
            f"| **Porta de Conexão** | `{porta}` |\n"
            f"| **Usuário Utilizado** | `{usuario}` |\n"
        )
        self.log_info(tabela_dados)
        self.log_info("---")  # Linha horizontal separadora

        # --- 2. LOGS DE EXECUÇÃO (Usando Emojis e Negritos) ---
        self.log_info(f"🔄 **Conectando...** Estabelecendo sessão SSH via porta `{porta}`...")

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ip, username=usuario, password=senha, look_for_keys=False, port=int(porta))

            pdr = open(diretorioPdr)
            pdrLinha = pdr.readlines()

            for linha in pdrLinha:
                stdin, stdout, stderr = client.exec_command(linha)

            client.close()

            return f"Processo de padronização concluído para o IP: {ip}"

        except Exception as e:
            # Em caso de erro, exibe o problema na tela
            self.log_failure(f"Ocorreu um erro durante a execução: {str(e)}")
