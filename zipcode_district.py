from lxml import etree
import requests
def zipcode_func():
    """
    create table zipcode_district (
    province varchar(50) comment '省份',
    ty varchar(50) comment '类型city/district',
    city varchar(50) comment '城市名称',
    district_name varchar(50) comment '区县名称',
    district_phone varchar(50) comment '区划号码',
    district_zipcode varchar(50) comment '邮编',
    primary key (province,ty,city,district_name))
    ENGINE=InnoDB  DEFAULT CHARSET=utf8 comment "中国邮编省份、县市区映射关系";
    """
    url="http://tools.2345.com/yb.htm" #2345网站邮编、省市区
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36'
    }
    html=requests.get(url,headers=headers)
    html.encoding="gbk"
    html=html.text
    html = etree.HTML(html)
    result = []
    for d in html.xpath('//div[@id="J_tab_bd"]/div'):
        province = "".join(d.xpath('./h3/span/text()'))

        city = 0
        for k, di in enumerate(d.xpath('./table/tbody/tr')):
            ty = di.xpath("@class")
            if len(ty) > 0:
                ty = ty[0]

            if ty == "tit":
                continue
            if (k == 1) | ((k > 1) & (ty != [])):
                ty = "city"
                district_name = "0"
                city = "".join(di.xpath('./td[1]/span/text()'))
            else:
                ty = "district"
                district_name = "".join(di.xpath('./td[1]/text()'))

            district_phone = "".join(di.xpath('./td[2]/text()'))
            district_zipcode = "".join(di.xpath('./td[3]/text()'))

            l = [province, ty, city, district_name, district_phone, district_zipcode]
            result.append(l)
    return result