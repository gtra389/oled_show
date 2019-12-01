# coding=utf-8
import oledClass
import time

disp = oledClass.SSD1306()
time.sleep(3)
disp.draw.rectangle((0,0,127,63),outline=1,fill=0)
disp.text((8,8),'SSD1306 Testing...')
disp.display()
time.sleep(5)
disp.draw.rectangle((0,0,127,63),outline=0,fill=0)
disp.text((8,0),u'三山半落青天外',ttc=True)
disp.text((8,16),u'二水中分白鷺洲',ttc=True)
disp.text((8,32),u'總為浮雲能蔽日',ttc=True)
disp.text((8,48),u'長安不見使人愁',ttc=True)
disp.display()
time.sleep(5)
disp.start_scroll(0, 0, 7)
time.sleep(10)
disp.start_scroll(1, 0, 7, 1)
time.sleep(10)
disp.stop_scroll()
time.sleep(10)
disp.close()