import requests
from fake_useragent import UserAgent

_cookie = "buvid4=4F41C8A4-A89C-5E80-B2AB-8C222E6A8C0160292-023081809-k0zyHiuRDURA%2F%2Bu6uUGBn9ZJh%2BUZroYQRlqvXttbKIFoVgjlvvDstw%3D%3D; buvid_fp_plain=undefined; header_theme_version=CLOSE; enable_web_push=DISABLE; DedeUserID=14211643; DedeUserID__ckMd5=896bac34e98270e4; LIVE_BUVID=AUTO7217028158647895; FEED_LIVE_VERSION=V8; buvid3=EBCD19BB-5F43-FA27-9E08-E7841D11831F72726infoc; b_nut=1723861672; _uuid=1B2A10745-10D82-3D25-B7E8-710B373AF513573813infoc; rpdid=0zbfvZWQjU|16Z4lxZ7a|2E|3w1SVjVJ; CURRENT_QUALITY=0; hit-dyn-v2=1; dy_spec_agreed=1; PVID=1; home_feed_column=5; browser_resolution=1528-738; SESSDATA=7cf0a90d%2C1749738645%2C22e42%2Ac1CjCB9RJzkAh9y62VJOA5hlPUbd3i4NL0whgZhSfccV8a-XPH0eGK-wXHgh0XKNV-C-ISVmhhQTBjSmxFVzc5ay0tajNwRE5CblItNFExUVpnRmpkRXo5dnZPbUxaU2xBYmlEVkk2ZlY4M0xTd0k0dFQyb25qcy0wbnRwd09tWU5nRnhPODQ2Wmt3IIEC; bili_jct=8319bc03969a1f1bb0dace6ba2824845; fingerprint=ab608923ba12e0161c35f30096c6d1c1; buvid_fp=ab608923ba12e0161c35f30096c6d1c1; bp_t_offset_14211643=1011045506320695296; b_lsid=A24210B27_193D4C3D156; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzQ3MDA2MjQsImlhdCI6MTczNDQ0MTM2NCwicGx0IjotMX0.yXq7edwOq7Bewt2R2BAxu_8rUKDGZIOkx0uBMXxPpNE; bili_ticket_expires=1734700564; CURRENT_FNVAL=2000; sid=gjnii2pd"

headers = {
    "Cookie": _cookie,
    "User-Agent": UserAgent().random,
}
resp_card = requests.get(
    f"https://api.bilibili.com/x/web-interface/card?mid=14211643",
    headers=headers,
)

data1 = resp_card.json()
print(data1)
data1 = data1["data"]["card"]
print(data1)
fans = data1["fans"]

print(fans)
