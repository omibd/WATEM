# WATEM



## Xpath Query Syntax

### contains() and text()
1. //*[contains(@class,'head')]
2. //*[contains(text(),'abcd')]
3. //*[contains(normalize-space(text()),'abcd')]
4. //div[contains(@class, 'measure-tab') and contains(.//span, 'someText')]
    5. First fetch text via class 'measure-tab'  then filter by  'someText'
6. //div[contains(@class, 'measure-tab') and contains(.,'someText')]
7. //div[@class='credit_summary_item' and contains(., 'Professor')]
8. //div[@class='credit_summary_item' and text()='Professor']
9. //*[text() = 'qwerty' and not(text()[2])]

###  starts-with() and ends-with()
1. //*[starts-with(@class,'head')] 
2. //*[ends-with(@class,"head")]
3. //*[starts-with(name(), 'him')]

### position() and count()
1. //table[count(tr)=1]
2. //ol/li[position()=2]

### text() match
1. //button[text()='Submit']
2. //button[normalize-space(text())='Submit']
3. //button/text()
4. //form[@id='myform']//input[@type='submit']