from extras.scripts import Script, StringVar, IntegerVar
import paramiko
import os


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

        comandos = [
    ':global idRB "T1_RT1";',
    ':global idRB2 "LEM_RT1";',
    ':global idRT [/system identity get name];',
    ':global vrPDR1 "1.4";',
    ':global PDR1 $vrPDR1;',
    ':global vrPDR2 "1.4";',
    ':global PDR2 $vrPDR2;',
    ':global vrPDR3 "1.1";',
    ':global PDR3 $vrPDR3;',
    ':global vrPDR4 "2.26";',
    ':global PDR4 $vrPDR4;',
    ':global vrPDR5 "1.1";',
    ':global PDR5 $vrPDR5;',
    ':if ([/user find where name="admin"]!="") do={/ip firewall layer7-protocol remove [find];};',
    ':if ([/ip firewall layer7-protocol find where name="PDR1" regexp=$vrPDR1]="") do={:global PDR1 "0"};',
    ':if ([/ip firewall layer7-protocol find where name="PDR2" regexp=$vrPDR2]="") do={:global PDR2 "0"};',
    ':if ([/ip firewall layer7-protocol find where name="PDR3" regexp=$vrPDR3]="") do={:global PDR3 "0"};',
    ':if ([/ip firewall layer7-protocol find where name="PDR4" regexp=$vrPDR4]="") do={:global PDR4 "0"};',
    ':if ([/ip firewall layer7-protocol find where name="PDR5" regexp=$vrPDR5]="") do={:global PDR5 "0"};',
    ':if ([/system identity get name]=$idRB) do={:global PDR3 $vrPDR3};',
    ':if ([/system identity get name]=$idRB) do={:global PDR2 $vrPDR2};',
    ':if ([/system identity get name]=$idRB2) do={:global PDR3 $vrPDR3};',
    ':if ([/system identity get name]=$idRB2) do={:global PDR2 $vrPDR2};',
    ':put "==========INICIANDO PADRONIZACAO==========";',
    ':if ($vrPDR1 = $PDR1) do={} else={/ip dns set allow-remote-requests=yes servers=138.219.193.2,138.219.193.6,208.67.220.220,8.8.8.8;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system clock set time-zone-name=America/Belem;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system ntp client set enabled=yes primary-ntp=200.160.0.8 secondary-ntp=200.189.40.8;};',
    ':if ($vrPDR1 = $PDR1) do={} else={:if ([/snmp community find where name=brnet_ro]="") do={ /snmp community add addresses=0.0.0.0/0 name=brnet_ro; };};',
    ':if ($vrPDR1 = $PDR1) do={} else={/snmp set contact=suporte@brasilnett.com.br enabled=yes location="BALSAS, MA" trap-community=brnet_ro trap-version=2;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/radius remove [/radius find where address=138.219.193.7];};',
    ':if ($vrPDR1 = $PDR1) do={} else={/radius add address=138.219.193.7 secret=6CGjsL5uBJ9j service=login; };',
    ':if ($vrPDR1 = $PDR1) do={} else={/user aaa set interim-update=5m use-radius=yes;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging action remove [ /system logging action find where name="REMOTO"];};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging action add name=REMOTO remote=10.1.161.11 remote-port=65014 target=remote;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging remove [/system logging find where action!=memory and action!=echo];};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging add action=REMOTO topics=info,!dhcp,!wireless,!ipsec,!pppoe;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging add action=REMOTO topics=system;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging add action=REMOTO topics=error;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging add action=REMOTO topics=critical;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/system logging add action=REMOTO topics=warning;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/ip firewall layer7-protocol remove [find name="PDR1"];};',
    ':if ($vrPDR1 = $PDR1) do={} else={/ip firewall layer7-protocol add name="PDR1" regexp=$vrPDR1;};',
    ':if ($vrPDR1 = $PDR1) do={} else={/log warning "PADRONIZANDO PDR1";};',
    ':if ($vrPDR1 = $PDR1) do={} else={:put "PADRONIZANDO PDR1";};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip service find where name="telnet" and address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22 and disabled=no]="") do { /ip service set telnet address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22 disabled=no; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip service find where name="ftp" and address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22]="") do { /ip service set ftp address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip service find where name="www" and address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22 and port=8280]="") do { /ip service set www address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22 port=8280; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip service find where name="ssh" and address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22 and port=8222]="") do { /ip service set ssh address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22 port=8222; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip service find where name="api" and address=138.219.193.8/32,45.230.238.2/32,187.85.56.242/32 and disabled=no]="") do { /ip service set api address=138.219.193.8/32,45.230.238.2/32,187.85.56.242/32 disabled=no; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip service find where name="winbox" and port=8200 and address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22]="") do { /ip service set winbox address=138.219.192.0/22,10.0.0.0/8,192.168.0.0/16,100.64.0.0/10,45.230.236.0/22,131.255.244.0/22,187.85.56.0/22 port=8200; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip service find where name="api-ssl" and disabled=yes]="") do { /ip service set api-ssl address=0.0.0.0/0 disabled=yes; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={/ip firewall address-list remove [/ip firewall address-list find where list=BrasilNET-Firewall and dynamic=no address!=172.16.0.0/14 and address!=10.0.0.0/8 and address!=192.168.0.0/16 and address!=100.64.0.0/10 and address!=138.219.192.0/22 and address!=159.148.147.0/24 and address!=200.160.0.8 and address!=200.189.40.8 and address!=45.230.236.0/22 and address!=131.255.244.0/22 and address!=187.85.56.0/22];};',
    ':if ($vrPDR2 = $PDR2) do={} else={/ip firewall address-list set [/ip firewall address-list find where list=BrasilNET-Firewall] disabled=no;};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=172.16.0.0/14 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=172.16.0.0/14 list=BrasilNET-Firewall ; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=10.0.0.0/8 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=10.0.0.0/8 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=192.168.0.0/16 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=192.168.0.0/16 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=100.64.0.0/10 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=100.64.0.0/10 list=BrasilNET-Firewall; }; };',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=138.219.192.0/22 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=138.219.192.0/22 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=159.148.147.0/24 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=159.148.147.0/24 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=200.160.0.8 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=200.160.0.8 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=200.189.40.8 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=200.189.40.8 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=45.230.236.0/22 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=45.230.236.0/22 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=131.255.244.0/22 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=131.255.244.0/22 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=187.85.56.0/22 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=187.85.56.0/22 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={:if ([/ip firewall address-list find where address=10.100.0.0/16 and list=BrasilNET-Firewall]="") do={ /ip firewall address-list add address=10.100.0.0/16 list=BrasilNET-Firewall; };};',
    ':if ($vrPDR2 = $PDR2) do={} else={/ip firewall address-list remove [/ip firewall address-list find where list=Firewall_Suporte and dynamic=no];};',
    ':if ($vrPDR2 = $PDR2) do={} else={/ip firewall address-list remove [/ip firewall address-list find where list=Acesso_Liberado_Firewall and dynamic=no];};',
    ':if ($vrPDR2 = $PDR2) do={} else={/ip firewall layer7-protocol remove [find name="PDR2"];};',
    ':if ($vrPDR2 = $PDR2) do={} else={/ip firewall layer7-protocol add name="PDR2" regexp=$vrPDR2;};',
    ':if ($vrPDR2 = $PDR2) do={} else={/log warning "PADRONIZANDO PDR2";};',
    ':if ($vrPDR2 = $PDR2) do={} else={:put "PADRONIZANDO PDR2";};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter remove [/ip firewall filter find where chain!=forward and comment!=BRNET-Netwatch and comment!=BRNET-Aceita_VPN and comment!=BRNET-Aceita_SNMP and disabled=yes];};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add action=accept chain=input comment=BRNET-Aceita_OSPF protocol=ospf;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add action=accept chain=output comment=BRNET-Aceita_OSPF protocol=ospf;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add action=accept chain=input comment=BRNET-Aceita_MPLS dst-port=646 protocol=tcp;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add action=accept chain=input comment=BRNET-Aceita_MPLS dst-port=646 protocol=udp;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add action=accept chain=input comment=BRNET-Firewall_Protecao_Router port=53 protocol=udp src-address-type=local;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add chain=input comment=BRNET-Firewall_Protecao_Router action=add-src-to-address-list address-list=key01 address-list-timeout=10s dst-port=2100 protocol=tcp;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add chain=input comment=BRNET-Firewall_Protecao_Router action=add-src-to-address-list address-list=key02 address-list-timeout=10s dst-port=6580 protocol=tcp src-address-list=key01;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add chain=input comment=BRNET-Firewall_Protecao_Router action=add-src-to-address-list address-list=BrasilNET-Firewall address-list-timeout=30m dst-port=8200 protocol=tcp src-address-list=key02;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add chain=input comment=BRNET-Firewall_Protecao_Router action=drop dst-port=8200 protocol=tcp src-address-list=!BrasilNET-Firewall;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add chain=input comment=BRNET-Firewall_Protecao_Router action=drop dst-port=161 protocol=udp src-address-list=!BrasilNET-Firewall;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add chain=input comment=BRNET-Firewall_Protecao_Router action=drop dst-port=1723 protocol=tcp src-address-list=!BrasilNET-Firewall;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall filter add chain=input comment=BRNET-Firewall_Protecao_Router action=drop protocol=!icmp src-address-list=!BrasilNET-Firewall;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall layer7-protocol remove [find name="PDR3"];};',
    ':if ($vrPDR3 = $PDR3) do={} else={/ip firewall layer7-protocol add name="PDR3" regexp=$vrPDR3;};',
    ':if ($vrPDR3 = $PDR3) do={} else={/log warning "PADRONIZANDO PDR3";};',
    ':if ($vrPDR3 = $PDR3) do={} else={:put "PADRONIZANDO PDR3";};',
    ':if ($vrPDR4 = $PDR4) do={} else={/user remove [find group=write name!=slc and name!=SB and name!=cbe and name!=radiocom and name!=fabio and name!=laranjeiras.agricola and name!=teatino and name!=norton and name!=zaltron and name!=montani and name!=peteck and name!=acesso];};',
    ':if ($vrPDR4 = $PDR4) do={} else={/user remove [find group=read];};',
    ':if ($vrPDR4 = $PDR4) do={} else={/user remove [find name="rafael.servian"];};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="ZABBIX"]="") do={ /user add name=ZABBIX group=full;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="ZABBIX"]!="") do={/user set [find name="ZABBIX"] password=ax2742q8 address="";};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="BRNETSAC"]="") do={ /user add name=BRNETSAC group=write;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="BRNETSAC"]!="") do={/user set [find name="BRNETSAC"] password=367ntd61;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="BRNETCGR"]="") do={ /user add name=BRNETCGR group=write;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="BRNETCGR"]!="") do={/user set [find name="BRNETCGR"] password=guz2mlhg;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="BRNETSUP"]="") do={ /user add name=BRNETSUP group=read;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="BRNETSUP"]!="") do={/user set [find name="BRNETSUP"] password=5v2em25l;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="william.batista"]!="") do={ /user remove [find name=william.batista];};} else={:if ([/user find where name="william.batista"]="") do={ /user add name=william.batista group=write;};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="william.batista"]!="") do={/user set [find name="william.batista"] password=918270;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="tiago.guida"]!="") do={ /user remove [find name=tiago.guida];};} else={:if ([/user find where name="tiago.guida"]="") do={ /user add name=tiago.guida group=write;};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="tiago.guida"]!="") do={/user set [find name="tiago.guida"] password=tiago17;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="ramon.cunha"]!="") do={ /user remove [find name=ramon.cunha];};} else={:if ([/user find where name="ramon.cunha"]="") do={ /user add name=ramon.cunha group=write;};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="ramon.cunha"]!="") do={/user set [find name="ramon.cunha"] password=ramon1795;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="daniel.brandao"]!="") do={ /user remove [find name=daniel.brandao];};} else={:if ([/user find where name="daniel.brandao"]="") do={ /user add name=daniel.brandao group=write;};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="daniel.brandao"]!="") do={/user set [find name="daniel.brandao"] password=barros131619;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="jeremias.alves"]!="") do={ /user remove [find name=jeremias.alves];};} else={:if ([/user find where name="jeremias.alves"]="") do={ /user add name=jeremias.alves group=write;};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="jeremias.alves"]!="") do={/user set [find name="jeremias.alves"] password=251401;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="mateus.santos"]!="") do={ /user remove [find name=mateus.santos];};} else={:if ([/user find where name="mateus.santos"]="") do={ /user add name=mateus.santos group=write;};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="mateus.santos"]!="") do={/user set [find name="mateus.santos"] password=030465;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="jailton.bastos"]!="") do={ /user remove [find name=jailton.bastos];};} else={:if ([/user find where name="jailton.bastos"]="") do={ /user add name=jailton.bastos group=write;};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="jailton.bastos"]!="") do={/user set [find name="jailton.bastos"] password=brasilnet;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="admin"]!="") do={ /user remove [find name=admin];};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="ixc"]="") do={ /user add name=ixc group=full;};} else={:if ([/user find where name="ixc"]!="") do={ /user remove [find name=ixc];};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ($idRT ~ "_RT") do={:if ([/user find where name="ixcsoft"]="") do={ /user add name=ixcsoft group=full;};} else={:if ([/user find where name="ixcsoft"]!="") do={ /user remove [find name=ixcsoft];};};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="ixc"]!="") do={/user set [find name="ixc"] password=ixcsoft address=138.219.193.8/32,45.230.238.2/32;};};',
    ':if ($vrPDR4 = $PDR4) do={} else={:if ([/user find where name="ixcsoft"]!="") do={/user set [find name="ixcsoft"] password=Ma@2016@2BR address=138.219.193.8/32,45.230.238.2/32;};};',
    ':if ([/system identity get name]=$idRB) do={/user set [find group=write name!="BRNETCGR"] group=read};',
    ':if ($vrPDR4 = $PDR4) do={} else={/ip firewall layer7-protocol remove [find name="PDR4"];};',
    ':if ($vrPDR4 = $PDR4) do={} else={/ip firewall layer7-protocol add name="PDR4" regexp=$vrPDR4;};',
    ':if ($vrPDR4 = $PDR4) do={} else={/log warning "PADRONIZANDO PDR4";};',
    ':if ($vrPDR4 = $PDR4) do={} else={:put "PADRONIZANDO PDR4";};',
    ':if ($vrPDR5 = $PDR5) do={} else={/system scheduler remove [f];};',
    ':if ($vrPDR5 = $PDR5) do={} else={/system scheduler add interval=1d name=BrasilNET-INT on-event=BrasilNET-INT start-time=01:00:00;};',
    ':if ($vrPDR5 = $PDR5) do={} else={/system script remove [f];};',
    ':if ($vrPDR5 = $PDR5) do={} else={:if ([/system script find where name="BrasilNET-INT"]="") do={ /system script add name=BrasilNET-INT source=":global identity [/system identity get name]; :foreach i in=[/interface wireless find] do={:local radioname [/interface wireless get $i radio-name]; :if ($radioname != $identity) do={/interface wireless set $i radio-name=$identity;}}";};};',
    ':if ($vrPDR5 = $PDR5) do={} else={/ip firewall layer7-protocol remove [find name="PDR5"];};',
    ':if ($vrPDR5 = $PDR5) do={} else={/ip firewall layer7-protocol add name="PDR5" regexp=$vrPDR5;};',
    ':if ($vrPDR5 = $PDR5) do={} else={/log warning "PADRONIZANDO PDR5";};',
    ':if ($vrPDR5 = $PDR5) do={} else={:put "PADRONIZANDO PDR5";};',
    '/user group set write policy=ssh;',
    '/ip firewall service-port disable sip;',
    '/tool romon set enabled=no;',
    ':if ($idRT ~ "_PTP") do={/ip firewall filter remove [/ip firewall filter find where chain!=forward and comment!=BRNET-Netwatch and comment!=BRNET-Aceita_VPN and comment!=BRNET-Aceita_SNMP];};',
    ':if ($idRT ~ "_PTP") do={/ip firewall address-list remove [/ip firewall address-list find where list=BrasilNET-Firewall and dynamic=no];};',
    ':if ($idRT ~ "_AP") do={/ip firewall filter remove [/ip firewall filter find where chain!=forward and comment!=BRNET-Netwatch and comment!=BRNET-Aceita_VPN and comment!=BRNET-Aceita_SNMP];};',
    ':if ($idRT ~ "_AP") do={/ip firewall address-list remove [/ip firewall address-list find where list=BrasilNET-Firewall and dynamic=no];};',
    ':put "==========PADRONIZACAO CONCLUIDA==========";',
    '/ip firewall layer7-protocol remove [find name!="PDR1" and name!="PDR2" and name!="PDR3" and name!="PDR4" and name!="PDR5"];'
]

        for linha in comandos:
            stdin, stdout, stderr = client.exec_command(f'/{linha}')

        client.close()
