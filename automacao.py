#DISCORD
import discord
from discord.ext import commands
from discord.ext import tasks
import os
from dotenv import load_dotenv

#MINECRAFT
from mcstatus import JavaServer
import requests

# Variáveis
server_name="" # Para o Embed - Precisa ser um valor verdadeiro
minecraft_server_ip = ""
minecraft_server_porta = ""

prefix="!" # Não pode conter aspas
id_canal = 00000000000000 # Canal para enviar a mensagem ao ligar o Bot
tempo_de_atualizacao_em_segundos = 00 # Apenas número(s)

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} logado com sucesso!')
    print(f'https://api.mcsrvstat.us/2/{minecraft_server_ip}')
    print(minecraft_server_ip +":"+ minecraft_server_porta)

    ###########################################################
    #Loop#
    ###########################################################
    
    # Canal para mandar a mensagem [Não altere]
    channel = bot.get_channel(id_canal)

    @tasks.loop(seconds=tempo_de_atualizacao_em_segundos)
    async def Loop():
        # Encontrar o Servidor (API) [Não altere]
        response = requests.get(f'https://api.mcsrvstat.us/2/{minecraft_server_ip}').json()
        server_status = response['online']

        # Configurações de quando o Server está ligado
        if server_status == True:
            server_status = '🟢 Ligado'

            # Cor do embed quando servidor está ligado
            color_embed = discord.Color.blue()

            # Leitura da Versão do Minecraft
            version = response["version"]

            # Ping - usei uma API, é possível que não de o Ping exato, se possível substitua
            server = JavaServer.lookup(minecraft_server_ip +":"+ minecraft_server_porta)
            latency = server.ping()

            players_status = response['players']
            if players_status['online'] == 0:
                players_online_message = '0'
            if players_status['online'] == 1:
                players_online_message = '1'
            if players_status['online'] > 1:
                maisqueum = players_status['online']
                players_online_message = f"{maisqueum}"

        # Configurações de quando o Server está desligado
        if server_status == False:
            server_status = '❌ Desligado'
            color_embed = discord.Color.red() # Cor do embed quando servidor está desligado

            players_online_message = "0" # Quando ele não encontra o Servidor Ativo ele vai setar a quantidade de Players em zero [Não altere]

            version = "Indefinida" # Quando ele não encontra o Servidor Ativo ele vai setar a versão em "Indefinido" [Altere apenas a String] 

        
        # Embed - Você pode customizar o Embed da forma que quiser, deixarei uma lista abaixo das váriaveis pra facilitar:

        # {minecraft_server_ip} - IP do Servidor
        # {version} - Versão do Servidor
        # {players_online_message} - Quantidade de Players Conectados
        # {server_status} - Verifica se o Server está desligado ou Ligado
        # {str(latency)[:6]} - Verifica o Ping do Servidor | Para determinar o Ping exato recomendo fazer RCON |

        embed = discord.Embed(title=f"{server_name}", description="Informações do Servidor:", color=color_embed)
        embed.add_field(name="`🏠` IP do Servidor:", value=f"{minecraft_server_ip}", inline=False)
        embed.add_field(name="`📌` Versão", value=f"{version}")
        embed.add_field(name="`👤` Pessoas Ativas:", value=f"{players_online_message}", inline=False)
        embed.add_field(name="`🔌` Status do Servidor", value=f"{server_status}", inline=False)
        embed.add_field(name="`📡` Ping", value=f"{str(latency)[:6]}ms", inline=False)

        await channel.purge(limit=1)
        await channel.send(embed=embed)

    Loop.start()

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(DISCORD_TOKEN)