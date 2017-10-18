#!/usr/bin/python
# -*- coding: utf-8 -*-

from itty import *
import urllib2
import json
import multiprocessing
import time

def sendSparkGET(url):
    """
    This method is used for:
        -retrieving message text, when the webhook is triggered with a message
        -Getting the username of the person who posted the message if a command is recognized
    """
    request = urllib2.Request(url,
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+bearer)
    contents = urllib2.urlopen(request).read()
    print "RAN sendSparkGet"
    return contents
   
def sendSparkPOST(url, data):
    """
    This method is used for:
        -posting a message to the Spark room to confirm that a command was received and processed
    """
    request = urllib2.Request(url, json.dumps(data),
                            headers={"Accept" : "application/json",
                                     "Content-Type":"application/json"})
    request.add_header("Authorization", "Bearer "+HobbesBearer)
    contents = urllib2.urlopen(request).read()
    print "RAN sendSparkPost"
    return contents

def spammer():
	for i in range(15):
		sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "and they don't stop coming"})
		time.sleep(1)
	else:
		sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": "Way to go, you almost broke me."})

qtest = None

@post('/')
def index(request):
    print "index function ran"
    """
    When messages come in from the webhook, they are processed here.  The message text needs to be retrieved from Spark,
    using the sendSparkGet() function.  The message text is parsed.  If an expected command is found in the message,
    further actions are taken. i.e.
    """
    global webhook
    webhook = json.loads(request.body)
    print webhook['data']['id']
    result = sendSparkGET('https://api.ciscospark.com/v1/messages/{0}'.format(webhook['data']['id']))
    result = json.loads(result)
    msg = None
    markdown = None
    global qtest
    if webhook['data']['personEmail'] != bot_email:
        in_message = result.get('text', '').lower()
        in_message = in_message.replace(bot_name, '')
        if '/help' in in_message:
        	msg = "‘chuck’ or ‘chuckco’ - responds with 'praise be unto him'\n ’/not too’ or ‘not too’ or ‘jeans’\n 'help'\n ‘waste’ and ‘time’\n ’be humble’\n ’sit down’\n ‘fake news’\n ‘wrong’\n ‘cisco’\n ‘bug’\n ‘steam’ and ‘hams’\n ‘children’\n ‘fuck yea’ or ‘trashdove’ or ‘hell yea’\n ’good shit’\n ’understood’\n ‘allahu’\n ’well’ and ‘start coming’ or ‘starts coming’\n ’please clap’"
        elif 'cancer' in in_message:
        	msg = "WARNING: This message contains chemicals known to the State of California to cause cancer and birth defects or other reproductive harm."
        elif 'chuck' in in_message or "chuckco" in in_message:
            markdown = "#  𝓹𝓻𝓪𝓲𝓼𝓮 𝓫𝓮 𝓾𝓷𝓽𝓸 𝓱𝓲𝓶"
        elif '/not too' in in_message or 'not too' in in_message or 'jeans' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": Jeans})
        elif 'waste' in in_message and 'time' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": calvintime})
        elif 'be humble' in in_message:
        	msg = "Sit down"
        elif 'sit down' in in_message:
        	msg = "Be humble (lil bitch)"
        elif 'fake news' in in_message:
        	msg = "WRONG!"
        elif 'wrong' in in_message:
        	msg = "Fake news"
        elif 'cisco' in in_message and '.com' not in in_message:
        	msg = ".:|:.:|:. Chuck Co .:|:.:|:."
        elif 'bug' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": bryanBug})
        elif 'steam' in in_message and 'ham' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": steamedham})
        elif 'children' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": children})
        elif 'fuck yea' in in_message or 'trashdove' in in_message or 'hell yea' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": trashdove})
        elif 'good shit' in in_message:
        	markdown = "# 👌👀👌👀👌👀👌👀👌👀 good shit go౦ԁ sHit👌 thats ✔ some good👌👌shit right👌👌there👌👌👌 right✔there ✔✔if i do ƽaү so my self 💯 i say so 💯 thats what im talking about right there right there (chorus: ʳᶦᵍʰᵗ ᵗʰᵉʳᵉ) mMMMMᎷМ💯 👌👌 👌НO0ОଠOOOOOОଠଠOoooᵒᵒᵒᵒᵒᵒᵒᵒᵒ👌 👌👌 👌 💯 👌 👀 👀 👀 👌👌"
        elif 'understood' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": understood})
        elif 'allahu' in in_message and 'akbar' not in in_message:
        	msg = "akbar"
        elif 'well' in in_message and ('start coming' in in_message or 'starts coming' in in_message):
        	qtest = multiprocessing.Process(target=spammer)
        	qtest.start()
        	msg = "and they don't stop coming"
        elif 'please stop' == in_message:
        	qtest.terminate()
        	msg = " :( "
        elif 'please' in in_message and 'clap' in in_message:
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "files": jebpleaseclap})
        if msg != None:
            print msg
            sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "text": msg})
        if markdown != None:
        	print markdown
        	sendSparkPOST("https://api.ciscospark.com/v1/messages", {"roomId": webhook['data']['roomId'], "markdown": markdown})
    return "true"


####CHANGE THESE VALUES#####
jebpleaseclap = "https://media.giphy.com/media/l0NwPo3VHujpJDI4w/giphy.gif"
trashdove = "http://i.imgur.com/50wBJit.gif"
understood = "https://lh3.googleusercontent.com/hJlIRL8tQD9lG-x82xY3E5VW7hTEWd63MGnuSRASTdxSld3wzk3tGK_6BPp-F6U5z0HASxxCPKUNmoGnnTcBGTlVQ9nPIwDB5R4XQfIKna43SE8ac_C4_lZK3qedzTyxNDE0vPsyBGQvSPmiodb7ExScPJVp23PCe-UyRc3ZmVQtTVTLtcVFceINjw4w3Y3ydpoystUljD-6CJECx8ez2wkU1L0i2eDJZhlG256VmAO09nYO5WaRg3hft_6rk-lFkg45RJmWTfbwUMN5k4hb7S6gTkzlf59Xj1ZXStjqd-fOVLjyb1yRhoSEwtDz0vus0FDaMymED8mbnJ51QFJZ5H58caOTnuDD0H0BkltdHU_xupvwcg-ZwzyUpvAwP_YqGLwA19ziOeVsKda4qXAiYndzsX-WPAAIVdmhr9X8Xvhz4Oo8r7FoH5c-0ThONMkJMmwhS2_sWdpdG6QCvQS5U1tYkOKlo8hXKi_mLKJUBtYQqQLJ4F9GaAlOw8FBiHKyTGv0lsdUEb8OzB5pfK0qfq1yarNWKEw7Puhl6GPDx9ZKcZSH99abgWnqvpTgmjZGjITRL0R_ZVr49veilDH2viLsKFQ6yy79zdn6GyG8CdEx_bpDEFcGTGl-g0ijSxdGC0LO0aEAK0_ThfZcPjws96_01A9jEAJZ8c4bvd6BK-M=w1200-h675-no"
children = "https://lh3.googleusercontent.com/dNs-YgduU2QBAgI8bI-NTHxdb76IjQgTMAurbA5kJj3crlkvDupSzc8tk8Z-_ci5BfdEjVaGVbuvMTMyLhaPIAh0PyWdYLsP06ZOsbV0rWdJ6bHOEo59jZSshheXBde6ZbzP_QDimKa7Rvbd_KTdh7olqLsDWE0WNO5egk5wmNLKb9uErhYn8whRR2sJzDUp8cjtCZPcw7CtjUBnu0tsTq0WbmbDCqU_VkJID0qLbiLtunQ46dHy9ZnhaKm8ftEJaKSsc6uF9YZuY9OjvLb0ZnN52niAywOFR6HbuqQRCEyQFY2QQ1WEyW1e_OHjD8WsNx1tr90hMyyJBa1pgY-ihkK-AC-18dgWqWsBUZwnVAUXCGVAlkfFyhUBHJZcH5pcH5YN_-oZy0TETnYDM80mIJPIPiBhsYurGZgvs3LyUyvSXn3LRulr5tKO0K_Pn8G1FQ_bKAV1A6DE5ovVwjgV-qY9oDHju78_t2Sx8i1FHpmyZkzDVwvuORoXYSOqdCz0g6WCAgjpnPGOAhrW_ZXEM7-X-8l2-7vsrZZxeV4T3AAZp3aJDuvmDsrPb0LxutJNuEk5X9L2jVE0XxOlKQbSYYaLe8RYBCTJbw57P0XOx7ykqWqr9QDhQYu8Uokiax8Mt9c9rowD8N7qleHpNEOTOILfv6BqundAZKkG_3w54Gs=w106-h100-no"
steamedham = "https://lh3.googleusercontent.com/Ny4Icxd61yz42TXlWEdnEsVwUfs03bWSFQS_GSsl2t-SYldp5ITlFeNW7n1NdhW8ELniUwp04VbWeTIOOFvnv0_vH7gWVoD8wAZhc2hh5YiIoK9L1avYR1geOI1JG2L09DfX7mDZh4UYyGSHxywxJcUCPl8t5XxhDoJnaQEasQpKgS-sAcvy_nFM6RYkUciHrlJ2URfq1RQmu5r7COFDQGARsjO6wgmxnYrM5t-C9O-3QFyLV3i5ukuTSM1nfgNSJfIzP2hfeto2uBy4Nx78msIfY6ZOaKJDVbIV0mJ2FgGW_3np1sM2vFmVbmM_4Qzh75dZCld9nrcTUygzm0mrWJmeYnV3uJi7PhQ2W6C4U-K3csdzLkWRC8lpftkTSPgTGbTUGGbVrA-u53ah-mgJ8jWbfR6MTSQ3WHyD6UGSDQkUXM9Dq1GAgz1tf3rd50giTWr7eMo9pZUQvAA22nlM8lcnmaiehzSn2BugHsxZP7yfVqMWeCBlrt3L59PXXpvo2MQTKeh92iZS4C9SVNIoYzodM7NIaaP0hON1pRza4gNwwT6PK-Bwyef2znq0Q6twF8PT4M599Mfd5HWsIDROQyiM7oVx6rpOCOJrroSl-vFfab47lFwXJfkC6-Bxffokp2osqZLFjWJ5sUyx_veNhRTH4MVjCgw-M6v3wtHQJfk=w261-h141-no"
calvintime = "http://i3.kym-cdn.com/photos/images/original/000/897/738/706.png"
Jeans = "https://lh3.googleusercontent.com/SEKZgteoZn6-_fNJLWET5gPybQOKdOkdJG4pvUq2umoTL8oLBBIzUMASm9MPMEeaPMGqURkNeZOc028FeiAU5fEivXST_64r0KoJKyDWYP4b4kWkR4MhXSvYq1lHNkP5g9AQb6DunyHCHGI0e1dts8mbtdgPV_KOBzi5ExAepzm7JHPALlOM054E6RNXXxziMiQQu0TbeUo2O4Nw29XWTfiEiFPcV3x67f0wTRFsmCWPdb7lucczI7aOZfCyZ49-A1fBOnLHG5GPKhebrZjULsYH3Ju5i9FHKIOSqoZ7f0i11jePcC_R7AKHYewC2BJWUTrRGevn8fh07vhhl9F_0JQlF2qoGHB2RGzwJdXWq8JwgGCu8RkiQnUXecuhO4KjjtzAfWa0fV22kD7ojT4YEIyEI6wE7e7Q9rTR6TY58Q_Zozkc5n6S8m8_RQ3NmQxuySPSXu9vp7KzmUJ3Pc12Exqnq-U9ELfUoPyH676pPm8qXM3N_jOswtPxNwz2nFK9GK6pbhsJmOZ3DLSbiioBjvbKtE7rh_n1Vs3yFkQDKhK1iPnNf5RrT96UjrXsYG163l8DbFhZjaltOcBPxWZ8do0aTmfmgiVJ2fatuFP6xx5Nlw-VDjZNHxPI9u2hXLgcDa4PhRHBcaNG43cNHa34ocy2Tr240ItCmmD9VMVGJn8=w478-h592-no"
Jonathan = "https://lh3.googleusercontent.com/BZa-vEfXiCPh1y02kPEQo6U1YbkoaEkmybpnP_u0b35kLtmHHI9lcq-VUn_sUbL50nBjzq9r2Z_nFJIHwubQtuLd9Sd4O3E8cb4cM5HzOd8DfJzIjbapaC6xZ2kKbeD06jymUqk=w315-h420-no"
bryanBug = "https://lh3.googleusercontent.com/xScm_RRPDSzEkPrwymbufoMAzdbineiebFfAyAHParC2KpzntnrP41s8Gjs69GfWkgCaldnMm9TW6LxonYEbG77Duehy_8VjtazihtpAmdKLkm4euKg5v4-5OpbslYV1wMS2gJo=w287-h375-no"
bot_email = "hobbes@sparkbot.io"
bot_name = "Hobbes"
bearer = "****"
HobbesBearer = "****"
run_itty(server='wsgiref', host='0.0.0.0', port=8080)
