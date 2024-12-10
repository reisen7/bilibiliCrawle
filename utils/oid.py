
import requests
import re



av = ''
bv = 'BV1kgi1Y8ELg'

cookie = 'buvid4=023081809-k0zyHiuRDURA%2F%2Bu6uUGBn9ZJh%2BUZroYQRlqvXttbKIFoVgjlvvDstw%3D%3D; buvid_fp_plain=undefined; header_theme_version=CLOSE; enable_web_push=DISABLE; DedeUserID=14211643; DedeUserID__ckMd5=896bac34e98270e4; LIVE_BUVID=AUTO7217028158647895; FEED_LIVE_VERSION=V8; buvid3=EBCD19BB-5F43-FA27-9E08-E7841D11831F72726infoc; b_nut=1723861672; _uuid=1B2A10745-10D82-3D25-B7E8-710B373AF513573813infoc; rpdid=0zbfvZWQjU|16Z4lxZ7a|2E|3w1SVjVJ; fingerprint=21dae7af1181bd34188ec789e2d7d75c; CURRENT_QUALITY=0; buvid_fp=21dae7af1181bd34188ec789e2d7d75c; PVID=3; home_feed_column=5; hit-dyn-v2=1; dy_spec_agreed=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzM4ODU5MTQsImlhdCI6MTczMzYyNjY1NCwicGx0IjotMX0.-TpHS1oQ29EYzWSf_slAT-jsYaBoZB3M_637TFrFLcI; bili_ticket_expires=1733885854; SESSDATA=1034f759%2C1749178715%2Ca2aad%2Ac1CjB-1L_IiUZkYXemBlhQoVB5lrjEGQv0N_RgiZ_DLplQ4Lt9XzBhzFWep3Rk6gCqGQwSVlV0YVFPbXgzUXNhT1dldWhGRVpPMU5jaDhzTVdDQ1QyLU56NDNIcnNnUVFOQ3VTQm1Xc1I3QlZwa2hlSzBIRTJtMC1SLXZRa3JlbmxDSV9oYXJvSTRRIIEC; bili_jct=b49d9fcd88fc86b822f7c9d4125530a3; sid=4k53eg99; bp_t_offset_14211643=1008410247531855872; b_lsid=FF812264_193A475A5F8; bsource=search_bing; browser_resolution=1912-954; CURRENT_FNVAL=4048'

headers = {
    'Cookie': cookie,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

def getOid():
    resp = requests.get("https://www.bilibili.com/video/"+bv,headers=headers)
    obj = re.compile(f'"aid":(?P<id>.*?),"bvid":"{bv}"')  # 在网页源代码里可以找到id，用正则获取到
    oid = obj.search(resp.text).group('id')
    # print('oid是' + oid)  # 在程序运行时告诉我们已经获取到了参数oid
    return oid


def getHeaders():
    return headers


def getCookie():
    return cookie

def getBv():
    return bv

if __name__ == '__main__':
    print(getOid('BV176i2YfE9L'))
