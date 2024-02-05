import tkinter as tk
from tkinter import filedialog
import socket
# 验证拼接子域名是否能够访问
def resolve_subdomain(subdomain: str) -> list:
    try:
        ip_addresses = socket.gethostbyname_ex(subdomain)
        #[2] 为 ip地址  [0]真实的主机名   [1] 别名列表
        return ip_addresses[2]
    except socket.gaierror:
        return[]


# 拼接子域名 并返回resolve_subdomain 检查是否可以访问
def scan_subdomains(domain: str) -> dict:
    subdomains = {}
    with open('subdomains.txt') as file:
        for line in file:
            subdomain = line.strip() + '.' + domain
            ips = resolve_subdomain(subdomain)
            if ips:
                subdomains[subdomain] = ips
    return subdomains

#扫描一个子域名
def scan_domain():
    domain = entry.get()
    subdomains = scan_subdomains(domain)
#判断subdomains 是否为空
    if subdomains:
        result_text.config(state="normal")
        result_text.delete('1.0',tk.END)
        result_text.insert(tk.END,f"Subdomains found: {domain}:\n")
        for subdomain,ips in subdomains.items():
            result_text.insert(tk.END,f"{subdomain}\n")
            result_text.insert(tk.END, "\n".join(ips))
            result_text.insert(tk.END,'\n\n')

        result_text.config(state="disabled")
    else:
        result_text.config(state="normal")
        result_text.delete('1.0',tk.END)
        result_text.insert(tk.END,f"No subdomains found for {domain}")
        result_text.config(state="disabled")
#扫描文件
def scan_file():
    file_path = filedialog.askdirectory()
    domains = []
    with open(file_path + "/domains.txt") as file:
        domains = file.readlines()
    domains = [domain.strip() for domain in domains]
    for domain in domains:
        subdomains = scan_subdomains(domain)
#GUI界面创建
window = tk.Tk()
window.title("Scan Subdomains")

lable = tk.Label(window,text = "Enter your domain:")
lable.pack()

entry = tk.Entry(window)
entry.pack()

scan_button = tk.Button(window,text = 'Scan Domain',command = scan_domain)
scan_button.pack()


scan_file = tk.Button(window,text ='Scan File',command = scan_file)
scan_file.pack()

result_text = tk.Text(window,state='disabled')
result_text.pack()

try:
    with open('subdomains.txt',"x") as file:
        file.write('subdomain1\nsubdomain2\nsubdomain3')
except FileExistsError:
    pass

window.mainloop()
