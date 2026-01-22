import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import urllib.parse
import urllib.request
import sys
import os
import base64
import json
import threading
import yaml      # 需安装 PyYAML

# ================= 资源路径工具 =================
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================= 规则列表 =================
ADVANCED_RULES = [
    "DOMAIN-SUFFIX,services.googleapis.cn,🚀 节点选择",
    "DOMAIN-SUFFIX,xn--ngstr-lra8j.com,🚀 节点选择",
    "DOMAIN,safebrowsing.urlsec.qq.com,DIRECT",
    "DOMAIN,safebrowsing.googleapis.com,DIRECT",
    "DOMAIN,developer.apple.com,🚀 节点选择",
    "DOMAIN-SUFFIX,digicert.com,🚀 节点选择",
    "DOMAIN,ocsp.apple.com,🚀 节点选择",
    "DOMAIN,ocsp.comodoca.com,🚀 节点选择",
    "DOMAIN,ocsp.usertrust.com,🚀 节点选择",
    "DOMAIN,ocsp.sectigo.com,🚀 节点选择",
    "DOMAIN,ocsp.verisign.net,🚀 节点选择",
    "DOMAIN-SUFFIX,apple-dns.net,🚀 节点选择",
    "DOMAIN,testflight.apple.com,🚀 节点选择",
    "DOMAIN,sandbox.itunes.apple.com,🚀 节点选择",
    "DOMAIN,itunes.apple.com,🚀 节点选择",
    "DOMAIN-SUFFIX,apps.apple.com,🚀 节点选择",
    "DOMAIN-SUFFIX,blobstore.apple.com,🚀 节点选择",
    "DOMAIN,cvws.icloud-content.com,🚀 节点选择",
    "DOMAIN-SUFFIX,mzstatic.com,DIRECT",
    "DOMAIN-SUFFIX,itunes.apple.com,DIRECT",
    "DOMAIN-SUFFIX,icloud.com,DIRECT",
    "DOMAIN-SUFFIX,icloud-content.com,DIRECT",
    "DOMAIN-SUFFIX,me.com,DIRECT",
    "DOMAIN-SUFFIX,aaplimg.com,DIRECT",
    "DOMAIN-SUFFIX,cdn20.com,DIRECT",
    "DOMAIN-SUFFIX,cdn-apple.com,DIRECT",
    "DOMAIN-SUFFIX,akadns.net,DIRECT",
    "DOMAIN-SUFFIX,akamaiedge.net,DIRECT",
    "DOMAIN-SUFFIX,edgekey.net,DIRECT",
    "DOMAIN-SUFFIX,mwcloudcdn.com,DIRECT",
    "DOMAIN-SUFFIX,mwcname.com,DIRECT",
    "DOMAIN-SUFFIX,apple.com,DIRECT",
    "DOMAIN-SUFFIX,apple-cloudkit.com,DIRECT",
    "DOMAIN-SUFFIX,apple-mapkit.com,DIRECT",
    "DOMAIN-SUFFIX,126.com,DIRECT",
    "DOMAIN-SUFFIX,126.net,DIRECT",
    "DOMAIN-SUFFIX,127.net,DIRECT",
    "DOMAIN-SUFFIX,163.com,DIRECT",
    "DOMAIN-SUFFIX,360buyimg.com,DIRECT",
    "DOMAIN-SUFFIX,36kr.com,DIRECT",
    "DOMAIN-SUFFIX,acfun.tv,DIRECT",
    "DOMAIN-SUFFIX,air-matters.com,DIRECT",
    "DOMAIN-SUFFIX,aixifan.com,DIRECT",
    "DOMAIN-KEYWORD,alicdn,DIRECT",
    "DOMAIN-KEYWORD,alipay,DIRECT",
    "DOMAIN-KEYWORD,taobao,DIRECT",
    "DOMAIN-SUFFIX,amap.com,DIRECT",
    "DOMAIN-SUFFIX,autonavi.com,DIRECT",
    "DOMAIN-KEYWORD,baidu,DIRECT",
    "DOMAIN-SUFFIX,bdimg.com,DIRECT",
    "DOMAIN-SUFFIX,bdstatic.com,DIRECT",
    "DOMAIN-SUFFIX,bilibili.com,DIRECT",
    "DOMAIN-SUFFIX,bilivideo.com,DIRECT",
    "DOMAIN-SUFFIX,caiyunapp.com,DIRECT",
    "DOMAIN-SUFFIX,clouddn.com,DIRECT",
    "DOMAIN-SUFFIX,cnbeta.com,DIRECT",
    "DOMAIN-SUFFIX,cnbetacdn.com,DIRECT",
    "DOMAIN-SUFFIX,cootekservice.com,DIRECT",
    "DOMAIN-SUFFIX,csdn.net,DIRECT",
    "DOMAIN-SUFFIX,ctrip.com,DIRECT",
    "DOMAIN-SUFFIX,dgtle.com,DIRECT",
    "DOMAIN-SUFFIX,dianping.com,DIRECT",
    "DOMAIN-SUFFIX,douban.com,DIRECT",
    "DOMAIN-SUFFIX,doubanio.com,DIRECT",
    "DOMAIN-SUFFIX,duokan.com,DIRECT",
    "DOMAIN-SUFFIX,easou.com,DIRECT",
    "DOMAIN-SUFFIX,ele.me,DIRECT",
    "DOMAIN-SUFFIX,feng.com,DIRECT",
    "DOMAIN-SUFFIX,fir.im,DIRECT",
    "DOMAIN-SUFFIX,frdic.com,DIRECT",
    "DOMAIN-SUFFIX,g-cores.com,DIRECT",
    "DOMAIN-SUFFIX,godic.net,DIRECT",
    "DOMAIN-SUFFIX,gtimg.com,DIRECT",
    "DOMAIN,cdn.hockeyapp.net,DIRECT",
    "DOMAIN-SUFFIX,hongxiu.com,DIRECT",
    "DOMAIN-SUFFIX,hxcdn.net,DIRECT",
    "DOMAIN-SUFFIX,iciba.com,DIRECT",
    "DOMAIN-SUFFIX,ifeng.com,DIRECT",
    "DOMAIN-SUFFIX,ifengimg.com,DIRECT",
    "DOMAIN-SUFFIX,ipip.net,DIRECT",
    "DOMAIN-SUFFIX,iqiyi.com,DIRECT",
    "DOMAIN-SUFFIX,jd.com,DIRECT",
    "DOMAIN-SUFFIX,jianshu.com,DIRECT",
    "DOMAIN-SUFFIX,knewone.com,DIRECT",
    "DOMAIN-SUFFIX,le.com,DIRECT",
    "DOMAIN-SUFFIX,lecloud.com,DIRECT",
    "DOMAIN-SUFFIX,lemicp.com,DIRECT",
    "DOMAIN-SUFFIX,licdn.com,DIRECT",
    "DOMAIN-SUFFIX,luoo.net,DIRECT",
    "DOMAIN-SUFFIX,meituan.com,DIRECT",
    "DOMAIN-SUFFIX,meituan.net,DIRECT",
    "DOMAIN-SUFFIX,mi.com,DIRECT",
    "DOMAIN-SUFFIX,miaopai.com,DIRECT",
    "DOMAIN-SUFFIX,microsoft.com,DIRECT",
    "DOMAIN-SUFFIX,microsoftonline.com,DIRECT",
    "DOMAIN-SUFFIX,miui.com,DIRECT",
    "DOMAIN-SUFFIX,miwifi.com,DIRECT",
    "DOMAIN-SUFFIX,mob.com,DIRECT",
    "DOMAIN-SUFFIX,netease.com,DIRECT",
    "DOMAIN-SUFFIX,office.com,DIRECT",
    "DOMAIN-SUFFIX,office365.com,DIRECT",
    "DOMAIN-KEYWORD,officecdn,DIRECT",
    "DOMAIN-SUFFIX,oschina.net,DIRECT",
    "DOMAIN-SUFFIX,ppsimg.com,DIRECT",
    "DOMAIN-SUFFIX,pstatp.com,DIRECT",
    "DOMAIN-SUFFIX,qcloud.com,DIRECT",
    "DOMAIN-SUFFIX,qdaily.com,DIRECT",
    "DOMAIN-SUFFIX,qdmm.com,DIRECT",
    "DOMAIN-SUFFIX,qhimg.com,DIRECT",
    "DOMAIN-SUFFIX,qhres.com,DIRECT",
    "DOMAIN-SUFFIX,qidian.com,DIRECT",
    "DOMAIN-SUFFIX,qihucdn.com,DIRECT",
    "DOMAIN-SUFFIX,qiniu.com,DIRECT",
    "DOMAIN-SUFFIX,qiniucdn.com,DIRECT",
    "DOMAIN-SUFFIX,qiyipic.com,DIRECT",
    "DOMAIN-SUFFIX,qq.com,DIRECT",
    "DOMAIN-SUFFIX,qqurl.com,DIRECT",
    "DOMAIN-SUFFIX,rarbg.to,DIRECT",
    "DOMAIN-SUFFIX,ruguoapp.com,DIRECT",
    "DOMAIN-SUFFIX,segmentfault.com,DIRECT",
    "DOMAIN-SUFFIX,sinaapp.com,DIRECT",
    "DOMAIN-SUFFIX,smzdm.com,DIRECT",
    "DOMAIN-SUFFIX,snapdrop.net,DIRECT",
    "DOMAIN-SUFFIX,sogou.com,DIRECT",
    "DOMAIN-SUFFIX,sogoucdn.com,DIRECT",
    "DOMAIN-SUFFIX,sohu.com,DIRECT",
    "DOMAIN-SUFFIX,soku.com,DIRECT",
    "DOMAIN-SUFFIX,speedtest.net,DIRECT",
    "DOMAIN-SUFFIX,sspai.com,DIRECT",
    "DOMAIN-SUFFIX,suning.com,DIRECT",
    "DOMAIN-SUFFIX,taobao.com,DIRECT",
    "DOMAIN-SUFFIX,tencent.com,DIRECT",
    "DOMAIN-SUFFIX,tenpay.com,DIRECT",
    "DOMAIN-SUFFIX,tianyancha.com,DIRECT",
    "DOMAIN-SUFFIX,tmall.com,DIRECT",
    "DOMAIN-SUFFIX,tudou.com,DIRECT",
    "DOMAIN-SUFFIX,umetrip.com,DIRECT",
    "DOMAIN-SUFFIX,upaiyun.com,DIRECT",
    "DOMAIN-SUFFIX,upyun.com,DIRECT",
    "DOMAIN-SUFFIX,veryzhun.com,DIRECT",
    "DOMAIN-SUFFIX,weather.com,DIRECT",
    "DOMAIN-SUFFIX,weibo.com,DIRECT",
    "DOMAIN-SUFFIX,xiami.com,DIRECT",
    "DOMAIN-SUFFIX,xiami.net,DIRECT",
    "DOMAIN-SUFFIX,xiaomicp.com,DIRECT",
    "DOMAIN-SUFFIX,ximalaya.com,DIRECT",
    "DOMAIN-SUFFIX,xmcdn.com,DIRECT",
    "DOMAIN-SUFFIX,xunlei.com,DIRECT",
    "DOMAIN-SUFFIX,yhd.com,DIRECT",
    "DOMAIN-SUFFIX,yihaodianimg.com,DIRECT",
    "DOMAIN-SUFFIX,yinxiang.com,DIRECT",
    "DOMAIN-SUFFIX,ykimg.com,DIRECT",
    "DOMAIN-SUFFIX,youdao.com,DIRECT",
    "DOMAIN-SUFFIX,youku.com,DIRECT",
    "DOMAIN-SUFFIX,zealer.com,DIRECT",
    "DOMAIN-SUFFIX,zhihu.com,DIRECT",
    "DOMAIN-SUFFIX,zhimg.com,DIRECT",
    "DOMAIN-SUFFIX,zimuzu.tv,DIRECT",
    "DOMAIN-SUFFIX,zoho.com,DIRECT",
    "DOMAIN-KEYWORD,amazon,🚀 节点选择",
    "DOMAIN-KEYWORD,google,🚀 节点选择",
    "DOMAIN-KEYWORD,gmail,🚀 节点选择",
    "DOMAIN-KEYWORD,youtube,🚀 节点选择",
    "DOMAIN-KEYWORD,facebook,🚀 节点选择",
    "DOMAIN-SUFFIX,fb.me,🚀 节点选择",
    "DOMAIN-SUFFIX,fbcdn.net,🚀 节点选择",
    "DOMAIN-KEYWORD,twitter,🚀 节点选择",
    "DOMAIN-KEYWORD,instagram,🚀 节点选择",
    "DOMAIN-KEYWORD,dropbox,🚀 节点选择",
    "DOMAIN-SUFFIX,twimg.com,🚀 节点选择",
    "DOMAIN-KEYWORD,blogspot,🚀 节点选择",
    "DOMAIN-SUFFIX,youtu.be,🚀 节点选择",
    "DOMAIN-KEYWORD,whatsapp,🚀 节点选择",
    "DOMAIN-KEYWORD,admarvel,REJECT",
    "DOMAIN-KEYWORD,admaster,REJECT",
    "DOMAIN-KEYWORD,adsage,REJECT",
    "DOMAIN-KEYWORD,adsmogo,REJECT",
    "DOMAIN-KEYWORD,adsrvmedia,REJECT",
    "DOMAIN-KEYWORD,adwords,REJECT",
    "DOMAIN-KEYWORD,adservice,REJECT",
    "DOMAIN-SUFFIX,appsflyer.com,REJECT",
    "DOMAIN-KEYWORD,domob,REJECT",
    "DOMAIN-SUFFIX,doubleclick.net,REJECT",
    "DOMAIN-KEYWORD,duomeng,REJECT",
    "DOMAIN-KEYWORD,dwtrack,REJECT",
    "DOMAIN-KEYWORD,guanggao,REJECT",
    "DOMAIN-KEYWORD,lianmeng,REJECT",
    "DOMAIN-SUFFIX,mmstat.com,REJECT",
    "DOMAIN-KEYWORD,mopub,REJECT",
    "DOMAIN-KEYWORD,omgmta,REJECT",
    "DOMAIN-KEYWORD,openx,REJECT",
    "DOMAIN-KEYWORD,partnerad,REJECT",
    "DOMAIN-KEYWORD,pingfore,REJECT",
    "DOMAIN-KEYWORD,supersonicads,REJECT",
    "DOMAIN-KEYWORD,uedas,REJECT",
    "DOMAIN-KEYWORD,umeng,REJECT",
    "DOMAIN-KEYWORD,usage,REJECT",
    "DOMAIN-SUFFIX,vungle.com,REJECT",
    "DOMAIN-KEYWORD,wlmonitor,REJECT",
    "DOMAIN-KEYWORD,zjtoolbar,REJECT",
    "DOMAIN-SUFFIX,9to5mac.com,🚀 节点选择",
    "DOMAIN-SUFFIX,abpchina.org,🚀 节点选择",
    "DOMAIN-SUFFIX,adblockplus.org,🚀 节点选择",
    "DOMAIN-SUFFIX,adobe.com,🚀 节点选择",
    "DOMAIN-SUFFIX,akamaized.net,🚀 节点选择",
    "DOMAIN-SUFFIX,alfredapp.com,🚀 节点选择",
    "DOMAIN-SUFFIX,amplitude.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ampproject.org,🚀 节点选择",
    "DOMAIN-SUFFIX,android.com,🚀 节点选择",
    "DOMAIN-SUFFIX,angularjs.org,🚀 节点选择",
    "DOMAIN-SUFFIX,aolcdn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,apkpure.com,🚀 节点选择",
    "DOMAIN-SUFFIX,appledaily.com,🚀 节点选择",
    "DOMAIN-SUFFIX,appshopper.com,🚀 节点选择",
    "DOMAIN-SUFFIX,appspot.com,🚀 节点选择",
    "DOMAIN-SUFFIX,arcgis.com,🚀 节点选择",
    "DOMAIN-SUFFIX,archive.org,🚀 节点选择",
    "DOMAIN-SUFFIX,armorgames.com,🚀 节点选择",
    "DOMAIN-SUFFIX,aspnetcdn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,att.com,🚀 节点选择",
    "DOMAIN-SUFFIX,awsstatic.com,🚀 节点选择",
    "DOMAIN-SUFFIX,azureedge.net,🚀 节点选择",
    "DOMAIN-SUFFIX,azurewebsites.net,🚀 节点选择",
    "DOMAIN-SUFFIX,bintray.com,🚀 节点选择",
    "DOMAIN-SUFFIX,bit.com,🚀 节点选择",
    "DOMAIN-SUFFIX,bit.ly,🚀 节点选择",
    "DOMAIN-SUFFIX,bitbucket.org,🚀 节点选择",
    "DOMAIN-SUFFIX,bjango.com,🚀 节点选择",
    "DOMAIN-SUFFIX,bkrtx.com,🚀 节点选择",
    "DOMAIN-SUFFIX,blog.com,🚀 节点选择",
    "DOMAIN-SUFFIX,blogcdn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,blogger.com,🚀 节点选择",
    "DOMAIN-SUFFIX,blogsmithmedia.com,🚀 节点选择",
    "DOMAIN-SUFFIX,blogspot.com,🚀 节点选择",
    "DOMAIN-SUFFIX,blogspot.hk,🚀 节点选择",
    "DOMAIN-SUFFIX,bloomberg.com,🚀 节点选择",
    "DOMAIN-SUFFIX,box.com,🚀 节点选择",
    "DOMAIN-SUFFIX,box.net,🚀 节点选择",
    "DOMAIN-SUFFIX,cachefly.net,🚀 节点选择",
    "DOMAIN-SUFFIX,chromium.org,🚀 节点选择",
    "DOMAIN-SUFFIX,cl.ly,🚀 节点选择",
    "DOMAIN-SUFFIX,cloudflare.com,🚀 节点选择",
    "DOMAIN-SUFFIX,cloudfront.net,🚀 节点选择",
    "DOMAIN-SUFFIX,cloudmagic.com,🚀 节点选择",
    "DOMAIN-SUFFIX,cmail19.com,🚀 节点选择",
    "DOMAIN-SUFFIX,cnet.com,🚀 节点选择",
    "DOMAIN-SUFFIX,cocoapods.org,🚀 节点选择",
    "DOMAIN-SUFFIX,comodoca.com,🚀 节点选择",
    "DOMAIN-SUFFIX,crashlytics.com,🚀 节点选择",
    "DOMAIN-SUFFIX,culturedcode.com,🚀 节点选择",
    "DOMAIN-SUFFIX,d.pr,🚀 节点选择",
    "DOMAIN-SUFFIX,danilo.to,🚀 节点选择",
    "DOMAIN-SUFFIX,dayone.me,🚀 节点选择",
    "DOMAIN-SUFFIX,db.tt,🚀 节点选择",
    "DOMAIN-SUFFIX,deskconnect.com,🚀 节点选择",
    "DOMAIN-SUFFIX,disq.us,🚀 节点选择",
    "DOMAIN-SUFFIX,disqus.com,🚀 节点选择",
    "DOMAIN-SUFFIX,disquscdn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,dnsimple.com,🚀 节点选择",
    "DOMAIN-SUFFIX,docker.com,🚀 节点选择",
    "DOMAIN-SUFFIX,dribbble.com,🚀 节点选择",
    "DOMAIN-SUFFIX,droplr.com,🚀 节点选择",
    "DOMAIN-SUFFIX,duckduckgo.com,🚀 节点选择",
    "DOMAIN-SUFFIX,dueapp.com,🚀 节点选择",
    "DOMAIN-SUFFIX,dytt8.net,🚀 节点选择",
    "DOMAIN-SUFFIX,edgecastcdn.net,🚀 节点选择",
    "DOMAIN-SUFFIX,edgekey.net,🚀 节点选择",
    "DOMAIN-SUFFIX,edgesuite.net,🚀 节点选择",
    "DOMAIN-SUFFIX,engadget.com,🚀 节点选择",
    "DOMAIN-SUFFIX,entrust.net,🚀 节点选择",
    "DOMAIN-SUFFIX,eurekavpt.com,🚀 节点选择",
    "DOMAIN-SUFFIX,evernote.com,🚀 节点选择",
    "DOMAIN-SUFFIX,fabric.io,🚀 节点选择",
    "DOMAIN-SUFFIX,fast.com,🚀 节点选择",
    "DOMAIN-SUFFIX,fastly.net,🚀 节点选择",
    "DOMAIN-SUFFIX,fc2.com,🚀 节点选择",
    "DOMAIN-SUFFIX,feedburner.com,🚀 节点选择",
    "DOMAIN-SUFFIX,feedly.com,🚀 节点选择",
    "DOMAIN-SUFFIX,feedsportal.com,🚀 节点选择",
    "DOMAIN-SUFFIX,fiftythree.com,🚀 节点选择",
    "DOMAIN-SUFFIX,firebaseio.com,🚀 节点选择",
    "DOMAIN-SUFFIX,flexibits.com,🚀 节点选择",
    "DOMAIN-SUFFIX,flickr.com,🚀 节点选择",
    "DOMAIN-SUFFIX,flipboard.com,🚀 节点选择",
    "DOMAIN-SUFFIX,g.co,🚀 节点选择",
    "DOMAIN-SUFFIX,gabia.net,🚀 节点选择",
    "DOMAIN-SUFFIX,geni.us,🚀 节点选择",
    "DOMAIN-SUFFIX,gfx.ms,🚀 节点选择",
    "DOMAIN-SUFFIX,ggpht.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ghostnoteapp.com,🚀 节点选择",
    "DOMAIN-SUFFIX,git.io,🚀 节点选择",
    "DOMAIN-KEYWORD,github,🚀 节点选择",
    "DOMAIN-SUFFIX,globalsign.com,🚀 节点选择",
    "DOMAIN-SUFFIX,gmodules.com,🚀 节点选择",
    "DOMAIN-SUFFIX,godaddy.com,🚀 节点选择",
    "DOMAIN-SUFFIX,golang.org,🚀 节点选择",
    "DOMAIN-SUFFIX,gongm.in,🚀 节点选择",
    "DOMAIN-SUFFIX,goo.gl,🚀 节点选择",
    "DOMAIN-SUFFIX,goodreaders.com,🚀 节点选择",
    "DOMAIN-SUFFIX,goodreads.com,🚀 节点选择",
    "DOMAIN-SUFFIX,gravatar.com,🚀 节点选择",
    "DOMAIN-SUFFIX,gstatic.com,🚀 节点选择",
    "DOMAIN-SUFFIX,gvt0.com,🚀 节点选择",
    "DOMAIN-SUFFIX,hockeyapp.net,🚀 节点选择",
    "DOMAIN-SUFFIX,hotmail.com,🚀 节点选择",
    "DOMAIN-SUFFIX,icons8.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ifixit.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ift.tt,🚀 节点选择",
    "DOMAIN-SUFFIX,ifttt.com,🚀 节点选择",
    "DOMAIN-SUFFIX,iherb.com,🚀 节点选择",
    "DOMAIN-SUFFIX,imageshack.us,🚀 节点选择",
    "DOMAIN-SUFFIX,img.ly,🚀 节点选择",
    "DOMAIN-SUFFIX,imgur.com,🚀 节点选择",
    "DOMAIN-SUFFIX,imore.com,🚀 节点选择",
    "DOMAIN-SUFFIX,instapaper.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ipn.li,🚀 节点选择",
    "DOMAIN-SUFFIX,is.gd,🚀 节点选择",
    "DOMAIN-SUFFIX,issuu.com,🚀 节点选择",
    "DOMAIN-SUFFIX,itgonglun.com,🚀 节点选择",
    "DOMAIN-SUFFIX,itun.es,🚀 节点选择",
    "DOMAIN-SUFFIX,ixquick.com,🚀 节点选择",
    "DOMAIN-SUFFIX,j.mp,🚀 节点选择",
    "DOMAIN-SUFFIX,js.revsci.net,🚀 节点选择",
    "DOMAIN-SUFFIX,jshint.com,🚀 节点选择",
    "DOMAIN-SUFFIX,jtvnw.net,🚀 节点选择",
    "DOMAIN-SUFFIX,justgetflux.com,🚀 节点选择",
    "DOMAIN-SUFFIX,kat.cr,🚀 节点选择",
    "DOMAIN-SUFFIX,klip.me,🚀 节点选择",
    "DOMAIN-SUFFIX,libsyn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,linkedin.com,🚀 节点选择",
    "DOMAIN-SUFFIX,line-apps.com,🚀 节点选择",
    "DOMAIN-SUFFIX,linode.com,🚀 节点选择",
    "DOMAIN-SUFFIX,lithium.com,🚀 节点选择",
    "DOMAIN-SUFFIX,littlehj.com,🚀 节点选择",
    "DOMAIN-SUFFIX,live.com,🚀 节点选择",
    "DOMAIN-SUFFIX,live.net,🚀 节点选择",
    "DOMAIN-SUFFIX,livefilestore.com,🚀 节点选择",
    "DOMAIN-SUFFIX,llnwd.net,🚀 节点选择",
    "DOMAIN-SUFFIX,macid.co,🚀 节点选择",
    "DOMAIN-SUFFIX,macromedia.com,🚀 节点选择",
    "DOMAIN-SUFFIX,macrumors.com,🚀 节点选择",
    "DOMAIN-SUFFIX,mashable.com,🚀 节点选择",
    "DOMAIN-SUFFIX,mathjax.org,🚀 节点选择",
    "DOMAIN-SUFFIX,medium.com,🚀 节点选择",
    "DOMAIN-SUFFIX,mega.co.nz,🚀 节点选择",
    "DOMAIN-SUFFIX,mega.nz,🚀 节点选择",
    "DOMAIN-SUFFIX,megaupload.com,🚀 节点选择",
    "DOMAIN-SUFFIX,microsofttranslator.com,🚀 节点选择",
    "DOMAIN-SUFFIX,mindnode.com,🚀 节点选择",
    "DOMAIN-SUFFIX,mobile01.com,🚀 节点选择",
    "DOMAIN-SUFFIX,modmyi.com,🚀 节点选择",
    "DOMAIN-SUFFIX,msedge.net,🚀 节点选择",
    "DOMAIN-SUFFIX,myfontastic.com,🚀 节点选择",
    "DOMAIN-SUFFIX,name.com,🚀 节点选择",
    "DOMAIN-SUFFIX,nextmedia.com,🚀 节点选择",
    "DOMAIN-SUFFIX,nsstatic.net,🚀 节点选择",
    "DOMAIN-SUFFIX,nssurge.com,🚀 节点选择",
    "DOMAIN-SUFFIX,nyt.com,🚀 节点选择",
    "DOMAIN-SUFFIX,nytimes.com,🚀 节点选择",
    "DOMAIN-SUFFIX,omnigroup.com,🚀 节点选择",
    "DOMAIN-SUFFIX,onedrive.com,🚀 节点选择",
    "DOMAIN-SUFFIX,onenote.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ooyala.com,🚀 节点选择",
    "DOMAIN-SUFFIX,openvpn.net,🚀 节点选择",
    "DOMAIN-SUFFIX,openwrt.org,🚀 节点选择",
    "DOMAIN-SUFFIX,orkut.com,🚀 节点选择",
    "DOMAIN-SUFFIX,osxdaily.com,🚀 节点选择",
    "DOMAIN-SUFFIX,outlook.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ow.ly,🚀 节点选择",
    "DOMAIN-SUFFIX,paddleapi.com,🚀 节点选择",
    "DOMAIN-SUFFIX,parallels.com,🚀 节点选择",
    "DOMAIN-SUFFIX,parse.com,🚀 节点选择",
    "DOMAIN-SUFFIX,pdfexpert.com,🚀 节点选择",
    "DOMAIN-SUFFIX,periscope.tv,🚀 节点选择",
    "DOMAIN-SUFFIX,pinboard.in,🚀 节点选择",
    "DOMAIN-SUFFIX,pinterest.com,🚀 节点选择",
    "DOMAIN-SUFFIX,pixelmator.com,🚀 节点选择",
    "DOMAIN-SUFFIX,pixiv.net,🚀 节点选择",
    "DOMAIN-SUFFIX,playpcesor.com,🚀 节点选择",
    "DOMAIN-SUFFIX,playstation.com,🚀 节点选择",
    "DOMAIN-SUFFIX,playstation.com.hk,🚀 节点选择",
    "DOMAIN-SUFFIX,playstation.net,🚀 节点选择",
    "DOMAIN-SUFFIX,playstationnetwork.com,🚀 节点选择",
    "DOMAIN-SUFFIX,pushwoosh.com,🚀 节点选择",
    "DOMAIN-SUFFIX,rime.im,🚀 节点选择",
    "DOMAIN-SUFFIX,servebom.com,🚀 节点选择",
    "DOMAIN-SUFFIX,sfx.ms,🚀 节点选择",
    "DOMAIN-SUFFIX,shadowsocks.org,🚀 节点选择",
    "DOMAIN-SUFFIX,sharethis.com,🚀 节点选择",
    "DOMAIN-SUFFIX,shazam.com,🚀 节点选择",
    "DOMAIN-SUFFIX,skype.com,🚀 节点选择",
    "DOMAIN-SUFFIX,smartdns柚子酱.com,🚀 节点选择",
    "DOMAIN-SUFFIX,smartmailcloud.com,🚀 节点选择",
    "DOMAIN-SUFFIX,sndcdn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,sony.com,🚀 节点选择",
    "DOMAIN-SUFFIX,soundcloud.com,🚀 节点选择",
    "DOMAIN-SUFFIX,sourceforge.net,🚀 节点选择",
    "DOMAIN-SUFFIX,spotify.com,🚀 节点选择",
    "DOMAIN-SUFFIX,squarespace.com,🚀 节点选择",
    "DOMAIN-SUFFIX,sstatic.net,🚀 节点选择",
    "DOMAIN-SUFFIX,st.luluku.pw,🚀 节点选择",
    "DOMAIN-SUFFIX,stackoverflow.com,🚀 节点选择",
    "DOMAIN-SUFFIX,startpage.com,🚀 节点选择",
    "DOMAIN-SUFFIX,staticflickr.com,🚀 节点选择",
    "DOMAIN-SUFFIX,steamcommunity.com,🚀 节点选择",
    "DOMAIN-SUFFIX,symauth.com,🚀 节点选择",
    "DOMAIN-SUFFIX,symcb.com,🚀 节点选择",
    "DOMAIN-SUFFIX,symcd.com,🚀 节点选择",
    "DOMAIN-SUFFIX,tapbots.com,🚀 节点选择",
    "DOMAIN-SUFFIX,tapbots.net,🚀 节点选择",
    "DOMAIN-SUFFIX,tdesktop.com,🚀 节点选择",
    "DOMAIN-SUFFIX,techcrunch.com,🚀 节点选择",
    "DOMAIN-SUFFIX,techsmith.com,🚀 节点选择",
    "DOMAIN-SUFFIX,thepiratebay.org,🚀 节点选择",
    "DOMAIN-SUFFIX,theverge.com,🚀 节点选择",
    "DOMAIN-SUFFIX,time.com,🚀 节点选择",
    "DOMAIN-SUFFIX,timeinc.net,🚀 节点选择",
    "DOMAIN-SUFFIX,tiny.cc,🚀 节点选择",
    "DOMAIN-SUFFIX,tinypic.com,🚀 节点选择",
    "DOMAIN-SUFFIX,tmblr.co,🚀 节点选择",
    "DOMAIN-SUFFIX,todoist.com,🚀 节点选择",
    "DOMAIN-SUFFIX,trello.com,🚀 节点选择",
    "DOMAIN-SUFFIX,trustasiassl.com,🚀 节点选择",
    "DOMAIN-SUFFIX,tumblr.co,🚀 节点选择",
    "DOMAIN-SUFFIX,tumblr.com,🚀 节点选择",
    "DOMAIN-SUFFIX,tweetdeck.com,🚀 节点选择",
    "DOMAIN-SUFFIX,tweetmarker.net,🚀 节点选择",
    "DOMAIN-SUFFIX,twitch.tv,🚀 节点选择",
    "DOMAIN-SUFFIX,txmblr.com,🚀 节点选择",
    "DOMAIN-SUFFIX,typekit.net,🚀 节点选择",
    "DOMAIN-SUFFIX,ubertags.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ublock.org,🚀 节点选择",
    "DOMAIN-SUFFIX,ubnt.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ulyssesapp.com,🚀 节点选择",
    "DOMAIN-SUFFIX,urchin.com,🚀 节点选择",
    "DOMAIN-SUFFIX,usertrust.com,🚀 节点选择",
    "DOMAIN-SUFFIX,v.gd,🚀 节点选择",
    "DOMAIN-SUFFIX,v2ex.com,🚀 节点选择",
    "DOMAIN-SUFFIX,vimeo.com,🚀 节点选择",
    "DOMAIN-SUFFIX,vimeocdn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,vine.co,🚀 节点选择",
    "DOMAIN-SUFFIX,vivaldi.com,🚀 节点选择",
    "DOMAIN-SUFFIX,vox-cdn.com,🚀 节点选择",
    "DOMAIN-SUFFIX,vsco.co,🚀 节点选择",
    "DOMAIN-SUFFIX,vultr.com,🚀 节点选择",
    "DOMAIN-SUFFIX,w.org,🚀 节点选择",
    "DOMAIN-SUFFIX,w3schools.com,🚀 节点选择",
    "DOMAIN-SUFFIX,webtype.com,🚀 节点选择",
    "DOMAIN-SUFFIX,wikiwand.com,🚀 节点选择",
    "DOMAIN-SUFFIX,wikileaks.org,🚀 节点选择",
    "DOMAIN-SUFFIX,wikimedia.org,🚀 节点选择",
    "DOMAIN-SUFFIX,wikipedia.com,🚀 节点选择",
    "DOMAIN-SUFFIX,wikipedia.org,🚀 节点选择",
    "DOMAIN-SUFFIX,windows.com,🚀 节点选择",
    "DOMAIN-SUFFIX,windows.net,🚀 节点选择",
    "DOMAIN-SUFFIX,wire.com,🚀 节点选择",
    "DOMAIN-SUFFIX,wordpress.com,🚀 节点选择",
    "DOMAIN-SUFFIX,workflowy.com,🚀 节点选择",
    "DOMAIN-SUFFIX,wp.com,🚀 节点选择",
    "DOMAIN-SUFFIX,wsj.com,🚀 节点选择",
    "DOMAIN-SUFFIX,wsj.net,🚀 节点选择",
    "DOMAIN-SUFFIX,xda-developers.com,🚀 节点选择",
    "DOMAIN-SUFFIX,xeeno.com,🚀 节点选择",
    "DOMAIN-SUFFIX,xiti.com,🚀 节点选择",
    "DOMAIN-SUFFIX,yahoo.com,🚀 节点选择",
    "DOMAIN-SUFFIX,yimg.com,🚀 节点选择",
    "DOMAIN-SUFFIX,ying.com,🚀 节点选择",
    "DOMAIN-SUFFIX,yoyo.org,🚀 节点选择",
    "DOMAIN-SUFFIX,ytimg.com,🚀 节点选择",
    "DOMAIN-SUFFIX,telegra.ph,🚀 节点选择",
    "DOMAIN-SUFFIX,telegram.org,🚀 节点选择",
    "IP-CIDR,91.108.4.0/22,🚀 节点选择,no-resolve",
    "IP-CIDR,91.108.8.0/21,🚀 节点选择,no-resolve",
    "IP-CIDR,91.108.16.0/22,🚀 节点选择,no-resolve",
    "IP-CIDR,91.108.56.0/22,🚀 节点选择,no-resolve",
    "IP-CIDR,149.154.160.0/20,🚀 节点选择,no-resolve",
    "IP-CIDR6,2001:67c:4e8::/48,🚀 节点选择,no-resolve",
    "IP-CIDR6,2001:b28:f23d::/48,🚀 节点选择,no-resolve",
    "IP-CIDR6,2001:b28:f23f::/48,🚀 节点选择,no-resolve",
    "IP-CIDR,120.232.181.162/32,🚀 节点选择,no-resolve",
    "IP-CIDR,120.241.147.226/32,🚀 节点选择,no-resolve",
    "IP-CIDR,120.253.253.226/32,🚀 节点选择,no-resolve",
    "IP-CIDR,120.253.255.162/32,🚀 节点选择,no-resolve",
    "IP-CIDR,120.253.255.34/32,🚀 节点选择,no-resolve",
    "IP-CIDR,120.253.255.98/32,🚀 节点选择,no-resolve",
    "IP-CIDR,180.163.150.162/32,🚀 节点选择,no-resolve",
    "IP-CIDR,180.163.150.34/32,🚀 节点选择,no-resolve",
    "IP-CIDR,180.163.151.162/32,🚀 节点选择,no-resolve",
    "IP-CIDR,180.163.151.34/32,🚀 节点选择,no-resolve",
    "IP-CIDR,203.208.39.0/24,🚀 节点选择,no-resolve",
    "IP-CIDR,203.208.40.0/24,🚀 节点选择,no-resolve",
    "IP-CIDR,203.208.41.0/24,🚀 节点选择,no-resolve",
    "IP-CIDR,203.208.43.0/24,🚀 节点选择,no-resolve",
    "IP-CIDR,203.208.50.0/24,🚀 节点选择,no-resolve",
    "IP-CIDR,220.181.174.162/32,🚀 节点选择,no-resolve",
    "IP-CIDR,220.181.174.226/32,🚀 节点选择,no-resolve",
    "IP-CIDR,220.181.174.34/32,🚀 节点选择,no-resolve",
    "DOMAIN,injections.adguard.org,DIRECT",
    "DOMAIN,local.adguard.org,DIRECT",
    "DOMAIN-SUFFIX,local,DIRECT",
    "IP-CIDR,127.0.0.0/8,DIRECT",
    "IP-CIDR,172.16.0.0/12,DIRECT",
    "IP-CIDR,192.168.0.0/16,DIRECT",
    "IP-CIDR,10.0.0.0/8,DIRECT",
    "IP-CIDR,17.0.0.0/8,DIRECT",
    "IP-CIDR,100.64.0.0/10,DIRECT",
    "IP-CIDR,224.0.0.0/4,DIRECT",
    "IP-CIDR6,fe80::/10,DIRECT",
    "DOMAIN-SUFFIX,cn,DIRECT",
    "DOMAIN-KEYWORD,-cn,DIRECT",
    "GEOIP,CN,DIRECT",
    "MATCH,🚀 节点选择"
]

# ================= 核心工具函数 =================
def safe_base64_decode(s):
    if not s: return ""
    s = s.strip().replace("\n", "").replace("\r", "").replace(" ", "")
    s = s.replace('-', '+').replace('_', '/')
    missing_padding = 4 - len(s) % 4
    if missing_padding and missing_padding != 4:
        s += '=' * missing_padding
    try:
        return base64.b64decode(s).decode('utf-8')
    except Exception:
        return None

def fetch_subscription(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            content = response.read().decode('utf-8')
        decoded_content = safe_base64_decode(content)
        if decoded_content:
            return decoded_content.splitlines()
        else:
            return content.splitlines()
    except Exception as e:
        raise Exception(f"网络请求失败: {str(e)}")

# ================= 节点解析逻辑 =================
def parse_vmess(link, original_name):
    b64_str = link[8:]
    json_str = safe_base64_decode(b64_str)
    if not json_str: return None
    try:
        data = json.loads(json_str)
    except: return None
    
    name = data.get("ps", original_name)
    if not name: name = f"{data.get('add')}:{data.get('port')}"
    
    node = {
        "name": name, "type": "vmess", "server": data.get("add"),
        "port": int(data.get("port")), "uuid": data.get("id"),
        "alterId": int(data.get("aid", 0)), "cipher": data.get("scy", "auto"),
        "udp": True, "xudp": True, "network": data.get("net", "tcp")
    }
    if data.get("tls") == "tls":
        node["tls"] = True
        node["servername"] = data.get("sni") or data.get("host") or ""
    if node["network"] == "ws":
        ws_opts = {}
        if data.get("path"): ws_opts["path"] = data.get("path")
        if data.get("host"): ws_opts["headers"] = {"Host": data.get("host")}
        if ws_opts: node["ws-opts"] = ws_opts
    if node["network"] == "grpc":
        if data.get("path"): node["grpc-opts"] = {"grpc-service-name": data.get("path")}
    return node

def parse_trojan(parsed, params, name):
    node = {
        "name": name, "type": "trojan", "server": parsed.hostname,
        "port": parsed.port, "password": parsed.username, "udp": True,
        "sni": params.get("sni", [parsed.hostname])[0],
        "skip-cert-verify": params.get("allowInsecure", ["0"])[0] == "1"
    }
    net_type = params.get("type", ["tcp"])[0]
    node["network"] = net_type
    if net_type == "ws":
        ws_opts = {}
        if "path" in params: ws_opts["path"] = params["path"][0]
        if "host" in params: ws_opts["headers"] = {"Host": params["host"][0]}
        if ws_opts: node["ws-opts"] = ws_opts
    if net_type == "grpc" and "serviceName" in params:
        node["grpc-opts"] = {"grpc-service-name": params["serviceName"][0]}
    return node

def parse_ss(link, name):
    body = link[5:].split("#")[0].split("?")[0]
    if "@" not in body:
        decoded = safe_base64_decode(body)
        if decoded: body = decoded
    try:
        if "@" in body:
            user_part, server_part = body.rsplit("@", 1)
            if ":" not in user_part:
                decoded_user = safe_base64_decode(user_part)
                if decoded_user: user_part = decoded_user
            method, password = user_part.split(":", 1)
            server, port = server_part.rsplit(":", 1)
            return {
                "name": name, "type": "ss", "server": server, "port": int(port),
                "cipher": method, "password": password, "udp": True
            }
    except: pass
    return None

def parse_hy2(parsed, params, name):
    node = {
        "name": name, "type": "hysteria2", "server": parsed.hostname,
        "port": parsed.port, "password": parsed.username,
        "sni": params.get("sni", [""])[0],
        "skip-cert-verify": params.get("insecure", ["0"])[0] == "1", "tfo": True
    }
    if "obfs" in params:
        node["obfs"] = params["obfs"][0]
        if "obfs-password" in params: node["obfs-password"] = params["obfs-password"][0]
    return node

def parse_vless(parsed, params, name):
    try: port = int(parsed.port)
    except: port = 443
    node = {
        "name": name, "type": "vless", "server": parsed.hostname,
        "port": port, "uuid": parsed.username, "udp": True, "xudp": True,
        "packet-encoding": "xudp"
    }
    security = params.get("security", ["none"])[0]
    net_type = params.get("type", ["tcp"])[0]
    node["network"] = net_type
    if "flow" in params: node["flow"] = params["flow"][0]
    if security in ["tls", "reality"]:
        node["tls"] = True
        node["servername"] = params.get("sni", [""])[0]
        if "fp" in params: node["client-fingerprint"] = params["fp"][0]
        if security == "reality":
            node["reality-opts"] = {
                "public-key": params.get("pbk", [""])[0], "short-id": params.get("sid", [""])[0]
            }
    if net_type == "ws":
        ws_opts = {}
        if "path" in params: ws_opts["path"] = params["path"][0]
        if "host" in params: ws_opts["headers"] = {"Host": params["host"][0]}
        if ws_opts: node["ws-opts"] = ws_opts
    if net_type == "grpc" and "serviceName" in params:
        node["grpc-opts"] = {"grpc-service-name": params["serviceName"][0]}
    return node

def parse_link(link):
    try:
        link = link.strip()
        if not link or link.startswith("#"): return None
        name = "Unknown"
        real_link = link
        if "#" in link:
            parts = link.split("#", 1)
            real_link = parts[0]
            name = urllib.parse.unquote(parts[1]).strip()
        
        parsed = None
        params = {}
        if not real_link.startswith("vmess://"):
            try:
                parsed = urllib.parse.urlparse(real_link)
                params = urllib.parse.parse_qs(parsed.query)
                if name == "Unknown" and parsed.fragment: name = urllib.parse.unquote(parsed.fragment)
                if name == "Unknown": name = f"{parsed.hostname}:{parsed.port}"
            except: pass

        if real_link.startswith("hysteria2://"): return parse_hy2(parsed, params, name)
        elif real_link.startswith("vless://"): return parse_vless(parsed, params, name)
        elif real_link.startswith("ss://"): return parse_ss(real_link, name)
        elif real_link.startswith("vmess://"): return parse_vmess(real_link, name)
        elif real_link.startswith("trojan://"): return parse_trojan(parsed, params, name)
        return None
    except: return None

# ================= 弹窗配置类 =================
class RouterConfigDialog(tk.Toplevel):
    def __init__(self, parent, default_ui, default_ctrl, default_secret):
        super().__init__(parent)
        self.title("旁路由参数配置")
        self.geometry("400x300")
        self.result = None
        
        # 居中显示
        x = parent.winfo_x() + 60
        y = parent.winfo_y() + 60
        self.geometry(f"+{x}+{y}")
        self.transient(parent)
        self.grab_set()

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)

        # UI 路径
        ttk.Label(frame, text="Linux UI 路径 (External UI):").pack(anchor="w")
        self.ui_var = tk.StringVar(value=default_ui)
        ttk.Entry(frame, textvariable=self.ui_var, width=40).pack(fill="x", pady=(0, 10))

        # 控制地址
        ttk.Label(frame, text="监听地址 (External Controller):").pack(anchor="w")
        ttk.Label(frame, text="* 默认 0.0.0.0:9090 以允许局域网访问", font=("Arial", 8), foreground="gray").pack(anchor="w")
        self.ctrl_var = tk.StringVar(value=default_ctrl)
        ttk.Entry(frame, textvariable=self.ctrl_var, width=40).pack(fill="x", pady=(0, 10))

        # 密钥
        ttk.Label(frame, text="API 密钥 (Secret):").pack(anchor="w")
        self.secret_var = tk.StringVar(value=default_secret)
        ttk.Entry(frame, textvariable=self.secret_var, width=40).pack(fill="x", pady=(0, 20))

        # 按钮
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x")
        ttk.Button(btn_frame, text="取消", command=self.cancel).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="确定生成", command=self.confirm).pack(side="right", padx=5)

        self.wait_window()

    def confirm(self):
        self.result = {
            "ui": self.ui_var.get().strip(),
            "ctrl": self.ctrl_var.get().strip(),
            "secret": self.secret_var.get().strip()
        }
        self.destroy()

    def cancel(self):
        self.destroy()

# ================= 图形界面逻辑 =================

class ClashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SubX")
        self.root.geometry("520x400")
        self.root.resizable(False, False)

        try:
            icon_path = resource_path("000.ico")
            self.root.iconbitmap(icon_path)
        except Exception:
            pass

        style = ttk.Style()
        style.configure("TButton", padding=6, font=("Microsoft YaHei", 9))
        style.configure("TLabel", font=("Microsoft YaHei", 10))

        # 顶部栏
        frame_top = ttk.Frame(root)
        frame_top.pack(fill="x", padx=10, pady=5)
        btn_about = ttk.Button(frame_top, text="关于", width=6, command=self.show_about)
        btn_about.pack(side="right")

        # 选项卡
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=5)

        # Tab 1
        self.tab_file = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_file, text="📁 本地文件")
        ttk.Label(self.tab_file, text="请选择包含节点链接的 .txt 文件：").pack(anchor="w", pady=(0,5))
        self.file_path_var = tk.StringVar()
        frame_file_input = ttk.Frame(self.tab_file)
        frame_file_input.pack(fill="x")
        ttk.Entry(frame_file_input, textvariable=self.file_path_var, width=40).pack(side="left", fill="x", expand=True, padx=(0,5))
        ttk.Button(frame_file_input, text="浏览...", command=self.select_file).pack(side="left")

        # Tab 2
        self.tab_url = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.tab_url, text="🌐 订阅链接")
        ttk.Label(self.tab_url, text="请输入机场/订阅链接 (http/https)：").pack(anchor="w", pady=(0,5))
        self.url_var = tk.StringVar()
        ttk.Entry(self.tab_url, textvariable=self.url_var, width=50).pack(fill="x", pady=5)
        ttk.Label(self.tab_url, text="* 自动下载并解码 Base64", foreground="gray", font=("Arial", 9)).pack(anchor="w")

        # 高级选项
        frame_options = ttk.LabelFrame(root, text="通用选项", padding=10)
        frame_options.pack(fill="x", padx=15, pady=5)
        self.udp_var = tk.BooleanVar(value=True)
        chk_udp = ttk.Checkbutton(frame_options, text="开启 UDP 转发", variable=self.udp_var)
        chk_udp.pack(side="left", padx=15)
        self.xudp_var = tk.BooleanVar(value=True)
        chk_xudp = ttk.Checkbutton(frame_options, text="开启 XUDP (Meta优化)", variable=self.xudp_var)
        chk_xudp.pack(side="left", padx=15)

        # 底部
        frame_bottom = ttk.Frame(root, padding=15)
        frame_bottom.pack(fill="x")
        ttk.Separator(frame_bottom, orient='horizontal').pack(fill='x', pady=(0, 10))
        
        ttk.Label(frame_bottom, text="输出文件名:").pack(anchor="w")
        self.output_name_var = tk.StringVar(value="config.yaml")
        ttk.Entry(frame_bottom, textvariable=self.output_name_var, width=50).pack(fill="x", pady=5)
        
        # === 按钮区域 ===
        btn_frame = ttk.Frame(frame_bottom)
        btn_frame.pack(fill="x", pady=10)
        
        # 按钮 1: 生成普通电脑端配置
        self.btn_generate = ttk.Button(btn_frame, text="💻 生成电脑端配置", command=lambda: self.process_config(mode="desktop"))
        self.btn_generate.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        # 按钮 2: 生成旁路由配置
        self.btn_router = ttk.Button(btn_frame, text="🛠️ 生成旁路由配置", command=lambda: self.process_config(mode="router"))
        self.btn_router.pack(side="left", fill="x", expand=True, padx=(5, 0))

        self.status_label = ttk.Label(frame_bottom, text="准备就绪", foreground="gray")
        self.status_label.pack()

    def show_about(self):
        messagebox.showinfo("关于作者", "联系邮箱：zl5@outlook.de")

    def select_file(self):
        filename = filedialog.askopenfilename(title="选择文件", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filename: self.file_path_var.set(filename)

    def _get_valid_nodes(self):
        current_tab = self.notebook.index(self.notebook.select())
        raw_lines = []
        enable_udp = self.udp_var.get()
        enable_xudp = self.xudp_var.get()
        output_dir = os.getcwd()

        try:
            if current_tab == 0:
                input_path = self.file_path_var.get()
                if not input_path:
                    messagebox.showwarning("提示", "请先选择文件！")
                    return None, None
                self.status_label.config(text="正在读取文件...", foreground="blue")
                with open(input_path, 'r', encoding='utf-8') as f:
                    raw_lines = f.readlines()
                output_dir = os.path.dirname(input_path)
            elif current_tab == 1:
                url = self.url_var.get().strip()
                if not url:
                    messagebox.showwarning("提示", "请输入订阅链接！")
                    return None, None
                self.status_label.config(text="正在下载订阅...", foreground="blue")
                self.root.update()
                raw_lines = fetch_subscription(url)

            self.status_label.config(text="正在解析节点...", foreground="blue")
            valid_nodes = []
            for line in raw_lines:
                node = parse_link(line)
                if node:
                    node['udp'] = enable_udp
                    if enable_xudp:
                        node['xudp'] = True
                        if node['type'] in ['vmess', 'vless']:
                            node['packet-encoding'] = 'xudp'
                    else:
                        node['xudp'] = False
                        if 'packet-encoding' in node:
                            del node['packet-encoding']
                    valid_nodes.append(node)
            
            return valid_nodes, output_dir

        except Exception as e:
            self.status_label.config(text="❌ 解析错误", foreground="red")
            messagebox.showerror("错误", str(e))
            return None, None

    # === 核心配置处理函数 ===
    def process_config(self, mode="desktop"):
        output_name = self.output_name_var.get()
        if not output_name.endswith((".yaml", ".yml")): output_name += ".yaml"

        # 1. 旁路由模式下，先弹窗询问参数
        router_params = {}
        if mode == "router":
            dialog = RouterConfigDialog(
                self.root, 
                default_ui="/home/hzl/mihomo/ui", 
                default_ctrl="0.0.0.0:9090",
                default_secret="123456"
            )
            if not dialog.result: return # 用户点了取消
            router_params = dialog.result

        valid_nodes, output_dir = self._get_valid_nodes()
        if not valid_nodes: return

        try:
            node_names = [n["name"] for n in valid_nodes]
            
            # === 定义代理组对象 ===
            
            # 1. 自动选择 (URL-Test)
            group_auto = {
                "name": "⚡ 自动选择", 
                "type": "url-test", 
                "url": "http://www.gstatic.com/generate_204", 
                "interval": 300, 
                "tolerance": 50, 
                "proxies": node_names
            }
            
            # 2. 故障转移 (Fallback)
            group_fallback = {
                "name": "🐢 故障转移", 
                "type": "fallback", 
                "url": "http://www.gstatic.com/generate_204", 
                "interval": 300, 
                "proxies": node_names
            }
            
            # 3. 主选择组 (Select) - 包含自动和故障转移
            group_select = {
                "name": "🚀 节点选择", 
                "type": "select", 
                "proxies": ["⚡ 自动选择", "🐢 故障转移"] + node_names
            }
            
            # 4. 漏网之鱼 (Select)
            group_final = {
                "name": "🐟 漏网之鱼", 
                "type": "select", 
                "proxies": ["🚀 节点选择", "DIRECT"]
            }

            proxy_groups = [group_select, group_auto, group_fallback, group_final]

            rules = ADVANCED_RULES

            if mode == "router":
                # === 旁路由配置 ===
                config = {
                    "allow-lan": True,
                    # 修改点3：添加 Mixed-Port 7890
                    "mixed-port": 7890, 
                    "mode": "rule",
                    "log-level": "error",
                    "external-controller": router_params["ctrl"], 
                    "secret": router_params["secret"],
                    "external-ui": router_params["ui"],
                    "ipv6": False,
                    "tun": {
                        "enable": True,
                        "stack": "system",
                        "auto-route": True,
                        "auto-detect-interface": True,
                        "dns-hijack": ["any:53"]
                    },
                    "dns": {
                        "enable": True,
                        "listen": "0.0.0.0:1053",
                        "ipv6": False,
                        "enhanced-mode": "fake-ip",
                        "fake-ip-range": "198.18.0.1/16",
                        "nameserver": ["223.5.5.5", "119.29.29.29"],
                        "fallback": ["8.8.8.8", "1.1.1.1"],
                        "fallback-filter": {"geoip": True, "ipcidr": ["240.0.0.0/4"]}
                    },
                    "proxies": valid_nodes,
                    "proxy-groups": proxy_groups,
                    "rules": rules
                }
                success_msg = f"配置生成成功！\n\n文件: {output_name}\n\n已应用参数:\nMixed-Port: 7890\nUI: {router_params['ui']}\nCtrl: {router_params['ctrl']}"

            else:
                # === 普通电脑端配置 ===
                config = {
                    "port": 7890, "socks-port": 7891, "allow-lan": True,
                    "mode": "rule", "log-level": "info", "external-controller": ":9090",
                    "dns": {"enable": True, "ipv6": False, "enhanced-mode": "fake-ip", "nameserver": ["8.8.8.8", "1.1.1.1"]},
                    "proxies": valid_nodes, "proxy-groups": proxy_groups, "rules": rules
                }
                success_msg = f"电脑端配置已生成！\n\n文件: {output_name}"

            output_path = os.path.join(output_dir, output_name)
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(config, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            self.status_label.config(text=f"🎉 成功！{len(valid_nodes)} 个节点", foreground="green")
            messagebox.showinfo("生成成功", success_msg)

        except Exception as e:
            self.status_label.config(text="❌ 生成失败", foreground="red")
            messagebox.showerror("系统错误", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ClashApp(root)
    root.mainloop()
