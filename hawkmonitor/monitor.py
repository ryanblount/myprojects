import requests
import random
import sys
import discord
import time
import re
import asyncio
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from discord.ext.commands import Bot
from discord.utils import get
from discord.ext import commands, tasks
from pytz import timezone
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, HardwareType
from fp.fp import FreeProxy

class stockStatus:

    user_agent_list = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36 Edg/90.0.818.39',
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        # 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    ]


    proxy_list = [
        "https://165.22.64.68:34961",
    ]

    STORES = {
        'BESTBUY0':[
            'https://www.bestbuy.com/site/apple-watch-series-6-gps-44mm-space-gray-aluminum-case-with-black-sport-band-space-gray/6215931.p?skuId=6215931',
            '.add-to-cart-button',
            'Add to Cart',
            'Apple Watch Series 6 (GPS) 44mm Space Gray Aluminum Case with Black Sport Band - Space Gray',
            '$379.99',
            'SKU: 6215931',
            'Model:M00H3LL/A',
            'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6215/6215931_sd.jpg;maxHeight=640;maxWidth=550',
        ],
        'BESTBUY1':[
            'https://www.bestbuy.com/site/sony-playstation-5-digital-edition-console/6430161.p?skuId=6430161',
            '.add-to-cart-button',
            'Add to Cart',
            'Sony - PlayStation 5 Digital Edition Console',
            '$399.99',
            'SKU: 6430161',
            'Model:3005719',
            'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6430/6430161_sd.jpg',
        ],
        'BESTBUY2':[
            'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149',
            '.add-to-cart-button',
            'Add to Cart',
            'Sony - PlayStation 5 Console',
            '$499.99',
            'SKU: 6426149',
            'Model: 3005718SKU',
            'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6426/6426149_sd.jpg;maxHeight=640;maxWidth=550',
        ],
        'BESTBUY3':[
            'https://www.bestbuy.com/site/combo/ps5-consoles/8f146095-0a5f-4993-b123-711a1d34745b',
            '.add-to-cart-button',
            'Add to Cart',
            'Package - Sony - PlayStation 5 Console and PlayStation 5 - DualSense Wireless Controller',
            '$569.98',
            'SKU: 6426149',
            'Model: 3005718',
            'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6426/6426149_sd.jpg;maxHeight=550;maxWidth=650',
        ],
        'BESTBUY4':[
            'https://www.bestbuy.com/site/combo/ps5-consoles/96be4c49-d98e-47c6-9a68-291c646d0e47',
            '.add-to-cart-button',
            'Add to Cart',
            'Package - Sony - PlayStation 5 Console and Marvel\'s Spider-Man: Miles Morales Standard Launch Edition',
            '$549.98',
            'SKU: 6426149',
            'Model: 3005718',
            'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6426/6426149_sd.jpg;maxHeight=550;maxWidth=650',
        ],
        'BESTBUY5':[
            'https://www.bestbuy.com/site/combo/ps5-consoles/c471fae2-1d2c-4870-ad3d-d39bffa39af2',
            '.add-to-cart-button',
            'Add to Cart',
            'Package - Sony - PlayStation 5 Console + 3 more items',
            '$679.96',
            'SKU: 6426149',
            'Model: 3005718',
            'https://i.imgur.com/rFx3DkH.png',
        ],
        'BESTBUY6':[
            'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440',
            '.add-to-cart-button',
            'Add to Cart',
            'NVIDIA GeForce RTX 3080 10GB GDDR6X PCI Express 4.0 Graphics Card - Titanium and Black',
            '$699.99',
            'SKU: 6429440',
            'Model: 9001G1332530000',
            'https://prnt.sc/11zcvsp',
        ],
        'BESTBUY7':[
            'https://www.bestbuy.com/site/nvidia-geforce-rtx-3070-8gb-gddr6-pci-express-4-0-graphics-card-dark-platinum-and-black/6429442.p?skuId=6429442',
            '.add-to-cart-button',
            'Add to Cart',
            'NVIDIA GeForce RTX 3070 8GB GDDR6 PCI Express 4.0 Graphics Card - Dark Platinum and Black',
            '$499.99',
            'SKU: 6429442',
            'Model: 9001G1422510000',
            'https://prnt.sc/11zczi1',
        ],
        'BESTBUY8':[
            'https://www.bestbuy.com/site/nvidia-geforce-rtx-3090-24gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429434.p?skuId=6429434',
            '.add-to-cart-button',
            'Add to Cart',
            'NVIDIA GeForce RTX 3090 24GB GDDR6X PCI Express 4.0 Graphics Card - Titanium and Black',
            '$1,499.99',
            'SKU: 6429434',
            'Model: 9001G1362510000',
            'https://prnt.sc/11zd364',
            
        ],
        'BESTBUY9':[
            'https://www.bestbuy.com/site/lego-creator-expert-flower-bouquet-10280/6434126.p?skuId=6434126',
            '.add-to-cart-button',
            'Add to Cart',
            'LEGO Creator Expert Flower Bouquet 10280',
            '$49.99',
            'SKU: 6434126',
            'Model: 6332921',
            'https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6434/6434126_rd.jpg',
            
        ],
        'WALMART1':[
            'https://www.walmart.com/ip/PlayStation-5-Console/363472942',
            'link',
            '^//schema.org/',
            'InStock',
            'Sony PlayStation 5 Video Game Console',
            '$499.99',
            '585799039',
            'https://i5.walmartimages.com/asr/fd596ed4-bf03-4ecb-a3b0-7a9c0067df83.bb8f535c7677cebdd4010741c6476d3a.png?odnWidth=undefined&odnHeight=undefined&odnBg=ffffff',
        ],
        'WALMART2':[
            'https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815',
            'link',
            '^//schema.org/',
            'InStock',
            'Sony PlayStation 5, Digital Edition',
            '$399.99',
            '590476772',
            'https://i5.walmartimages.com/asr/f62842fd-263f-46d4-8954-9fbe1a25d636.fefa1d11a99643573cf756f2ce835c05.png?odnWidth=undefined&odnHeight=undefined&odnBg=ffffff',
        ],
        'GAMESTOP1':[
            'https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html',
            'button',
            '\"availability\":\"Available\"',
            'PlayStation 5 (DIGITAL)',
            '$499.99',
            'https://media.gamestop.com/i/gamestop/11108140/PlayStation-5?$pdp$',
        ],
        'GAMESTOP2':[
            'https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5-digital-edition/11108141.html',
            'button',
            '\"availability\":\"Available\"',
            'PlayStation 5 Digital Edition',
            '$399.99',
            'https://media.gamestop.com/i/gamestop/11108141/PlayStation-5-Digital-Edition?$pdp$',
        ],
        'GAMESTOP3':[
            'https://www.gamestop.com/video-games/xbox-series-x/consoles/products/xbox-series-x/B224744V.html',
            'button',
            '\"availability\":\"Available\"',
            'Xbox Series X',
            '$499.99',
            'https://media.gamestop.com/i/gamestop/11108371/Xbox-Series-X?$pdp$'
        ],
        'TARGET1':[
            'https://www.target.com/p/playstation-5-console/-/A-81114595',
            '81114595',
            'IN_STOCK',
            'PlayStation 5 Console',
            '$499.99',
            'https://media.gamestop.com/i/gamestop/11108141/PlayStation-5-Digital-Edition?$pdp$'
        ],
        'TARGET2':[
            'https://www.target.com/p/playstation-5-digital-edition-console/-/A-81114596',
            '81114596',
            'IN_STOCK',
            'PlayStation 5 Digital Edition Console',
            '$399.99',
            'https://i5.walmartimages.com/asr/f62842fd-263f-46d4-8954-9fbe1a25d636.fefa1d11a99643573cf756f2ce835c05.png?odnWidth=undefined&odnHeight=undefined&odnBg=ffffff'
        ],
    }


    def getCarrier(self, url, selection):
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.MOBILE__PHONE]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
        proxyObject = FreeProxy(country_id="US", rand=True)
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent(),
                    'authority': 'www.bestbuy.com',
                    'sec-ch-ua': '^\\^Google',
                    'sec-ch-ua-mobile': '?0',
                    'accept-language': 'en-US,en;q=0.9',
        }
        proxies = {'Proxy' : proxyObject.get()}
        r = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(r.content,'html.parser')
        return soup.select(selection)
    
    def getWalmart(self, url, class_, hrefs):
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.MOBILE__PHONE]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
        proxyObject = FreeProxy(country_id="US", rand=True)
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent(),
                    'sec-ch-ua': '^\\^Google',
                    'sec-ch-ua-mobile': '?0',
                    'isExternal': 'false',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                    'accept-language': 'en-US,en;q=0.9',
        }
        proxies = {'Proxy' : proxyObject.get()}
        r = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(r.content,'html.parser')
        selection = str(soup.findAll(f'{class_}', href=re.compile(hrefs)))
        return selection

    def getGameStop(self, url, class_):
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.MOBILE__PHONE]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
        proxyObject = FreeProxy(country_id="US", rand=True)
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
        proxies = {'Proxy' : proxyObject.get()}
        r = requests.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(r.content,'html.parser')
        string = soup.findAll(f'{class_}', {"class":"btn-primary"})
        return string
    
    def getTarget(self, sku):
        software_names = [SoftwareName.CHROME.value]
        hardware_type = [HardwareType.MOBILE__PHONE]
        user_agent_rotator = UserAgent(software_names=software_names, hardware_type=hardware_type)
        proxyObject = FreeProxy(country_id="US", rand=True)
        headers = {'User-Agent': user_agent_rotator.get_random_user_agent()}
        proxies = {'Proxy' : proxyObject.get()}
        r = requests.get('https://www.target.com', headers=headers, proxies=proxies)
        key = r.cookies['visitorId']
        location = r.cookies['GuestLocation'].split('|')[0]
        store_id = requests.get('https://redsky.target.com/v3/stores/nearby/%s?key=%s&limit=1&within=100&unit=mile' %(location, key)).json()
        store_id = store_id[0]['locations'][0]['location_id']
        product_id = sku
        url = 'https://redsky.target.com/v3/pdp/tcin/%s' %product_id
        payload = {
                'pricing_store_id': store_id,
                'key': key,
        }
        jsonData = requests.get(url, params=payload).json()
        string = str(jsonData['product']['available_to_promise_network']['availability_status'])
        return string

    
    async def runCheck(self):
        channel = bot.get_channel(836274967896916028)
        message = await channel.fetch_message(channel.last_message_id)
        msgTimeStamp = timezone('US/Eastern').fromutc(message.created_at)
        curTime = timezone('US/Eastern').fromutc(datetime.utcnow())
        timeDiff = curTime - msgTimeStamp
        seconds = timeDiff.seconds
        sleep = 2.5
        checkTime = 180

        embedDict = {}
        for embed in message.embeds:
            embedDict = embed.to_dict()

        for key in self.STORES:
            if 'BESTBUY'in key:
                myResult = self.getCarrier(self.STORES[key][0],self.STORES[key][1])
                if self.STORES[key][2] in str(myResult):
                    sys.stdout.write("\u001b[32m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][3]}')
                    if seconds >= checkTime:
                        embed=discord.Embed(title=f"{self.STORES[key][3]}", url=f"{self.STORES[key][0]}", description="In stock.")
                        embed.set_thumbnail(url=f"{self.STORES[key][7]}")
                        embed.add_field(name=f"Price", value=f"{self.STORES[key][4]}", inline=True)
                        embed.add_field(name="Store", value="BestBuy.com", inline=True)
                        embed.set_author(name=f"{self.STORES[key][5]} | {self.STORES[key][6]}")
                        await channel.send(embed=embed)
                    else:
                        continue  
                else:
                    sys.stdout.write("\u001b[31m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][3]}')
                    #await asyncio.sleep(sleep)
            elif 'WALMART' in key:
                walmartResult = self.getWalmart(self.STORES[key][0],self.STORES[key][1],self.STORES[key][2])
                if self.STORES[key][3] in str(walmartResult):
                    sys.stdout.write("\u001b[32m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][4]}')
                    if seconds >= checkTime:
                        embed=discord.Embed(title=f"{self.STORES[key][4]}", url=f"{self.STORES[key][0]}", description="In stock.")
                        embed.set_thumbnail(url=f"{self.STORES[key][7]}")
                        embed.add_field(name=f"Price", value=f"{self.STORES[key][5]}", inline=True)
                        embed.add_field(name="Store", value="Walmart.com", inline=True)
                        embed.set_author(name=f"Product #{self.STORES[key][6]}")
                        await channel.send(embed=embed)
                    else:
                        continue      
                else:
                    sys.stdout.write("\u001b[31m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][4]}')
                    #await asyncio.sleep(sleep)
                    continue
            elif "GAMESTOP" in key:
                gameStopResult = self.getGameStop(self.STORES[key][0],self.STORES[key][1])
                if self.STORES[key][2] in str(gameStopResult):
                    sys.stdout.write("\u001b[32m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][3]}')
                    if seconds >= checkTime:
                        embed=discord.Embed(title=f"{self.STORES[key][3]}", url=f"{self.STORES[key][0]}", description="In stock.")
                        embed.set_thumbnail(url=f"{self.STORES[key][5]}")
                        embed.add_field(name=f"Price", value=f"{self.STORES[key][4]}", inline=True)
                        embed.add_field(name="Store", value="GameStop.com", inline=True)
                        await channel.send(embed=embed)
                    else:
                        continue  
                else:
                    sys.stdout.write("\u001b[31m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][3]}')
                    #await asyncio.sleep(sleep)
                    continue
            elif "TARGET" in key:
                targetResult = self.getTarget(self.STORES[key][1])
                if self.STORES[key][2] in str(targetResult):
                    sys.stdout.write("\u001b[32m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][3]}')
                    if seconds >= checkTime:
                        embed=discord.Embed(title=f"{self.STORES[key][3]}", url=f"{self.STORES[key][0]}", description="In stock.")
                        embed.set_thumbnail(url=f"{self.STORES[key][5]}")
                        embed.add_field(name=f"Price", value=f"{self.STORES[key][4]}", inline=True)
                        embed.add_field(name="Store", value="Target.com", inline=True)
                        await channel.send(embed=embed)
                    else:
                        continue  
                else:
                    sys.stdout.write("\u001b[31m")
                    print(f'[{datetime.now()}] :: {key}: {self.STORES[key][3]}')
                    #await asyncio.sleep(sleep)
                    continue
            else:
                break
                
        await self.runCheck()

bot = commands.Bot(command_prefix = "!")
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Scalping 😈"))
    #sys.setrecursionlimit(9999)
    print("Bot Online")
    await stockStatus().runCheck()

@bot.command()
async def ping(ctx):
    embed = discord.Embed(title=f'⌛ {round(bot.latency * 1000)} ms.', color=0xFF0000)
    await ctx.send(embed=embed)

bot.run("ODMzODkxNjM1MzEzMzc3Mjgy.YH48Gg.ds7K95F3zqcFnJPvlSVrjAilysI")
