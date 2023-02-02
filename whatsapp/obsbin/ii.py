"'@3' : active alarm last 7 days" 
"'$25-09-2021' history of 25-09-2021"
"*sitecode=pbsdr01,pbsdr02@7"
"*sitecode=pbsdr01,pbsdr02^timestamp^timestamp"
import os, sys

lsFile = lambda alarm_folder : [alarm_folder + "\\" + f for f in os.listdir(alarm_folder) if os.path.isfile(os.path.join(alarm_folder, f))]
files = lsFile(os.getcwd())
print(chr(10).join(files))


pane = "(//div[@id='pane-side']//div[@class='_3OvU8'])"
node = lambda x : pane + "[" + str(x) + "]"
panedic = {'chat_name' : ["//span[@class='_3q9s6']", "//div[@class='zoWT4']"],
           'chat_last_msg' : ["//span[@class='Hy9nV']", "//span[@class='_ccCW FqYAR i0jNr']","'/child::div[2]/div/span/span[3]'"],
           'chat_last_msg_sender' : ["//span[@class='l7jjieqr i0jNr']", "//span[@class='FqYAR i0jNr']"],
           'chat_last_msg_date' : ["//div[@class='_1i_wG']", "//div[@class='_3vPI2']/div[@class='_1i_wG']"],
           'notif' : ["//div[@class='_1pJ9J']/span"]
}


