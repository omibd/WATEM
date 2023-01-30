Set objStdOut = WScript.StdOut
set osh = createObject("Wscript.shell")
user_profile = """F:\Browser_Profile\chrome\selenium_chrome_profile"""
osh.run "cmd /c " & "chrome.exe https://web.whatsapp.com/ --remote-debugging-port=9222 --user-data-dir=" & user_profile, 0, True
set osh = Nothing