


MSG_INX:
	"(//div[@id='main']//div[@data-testid='msg-container'])[_i_]"
	- dc:
		sender_and_datetime:
			- xFC: msg_sender_dttm
			- arg: ''
		text : "//div[@class='_21Ahp']/span[1]/span"
		q_sende : "//div[@class='_3pMOs yKTUI']//div[1]/span"
		q_text : "//div[@class='_3pMOs yKTUI']//div[2]/span"
		time : "//div[@data-testid='msg-meta']"
		istrue_contains_image : "//img"