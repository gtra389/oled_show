from PIL import Image,ImageDraw,ImageFont
from devi2c import I2C

# Reference
# 1. i2cdev        https://github.com/cbeytas/i2cdev
# 2. i2C on rpi    https://stackoverflow.com/questions/41376518/i2c-communication-in-raspberry-pi-using-python
# 3. SSD1306       http://shihhsiung.blogspot.com/2018/11/i2c-ssd1306-096-oled.html
# 4. scim-chewing  http://yhhuang1966.blogspot.com/2017/10/scim-chewing.html
# 5. font download http://wordpress.bestdaylong.com/blog/archives/16103

# SSD1306 class
class SSD1306:
    DEV_ADDR = 0x3c
    CMDSET_INIT = (0xae,      #display off
                   0x20,0,    #horizontal addressing mode
                   0x40,      #display start line from 0
                   0xa0,      #column address 0 mapped to seg0
                   0xa8,0x3f, #set multiplex ratio to 64
                   0xc0,      #scan from com0
                   0xd3,0,    #vertical shift by com0
                   0xda,0x12, #alternative com pin configuration
                   0xd5,0x80, #display clock divide ratio, oscillator frequency
                   0xd9,0xf1, #pre-charge period
                   0xdb,0x30, #Vcomh deselect level
                   0x81,0x7f, #contrast control
                   0xa4,      #output follows ram content
                   0xa6,      #normal display
                   0x8d,0x14, #enable charge pump
                   0xaf)      #display on

    def __init__(self):
        self.dev = I2C(self.DEV_ADDR, 1) # Bus 1 is available on the GPIO Connector
        self.command(self.CMDSET_INIT)
        self.img = Image.new('1',(128,64))
        self.draw = ImageDraw.Draw(self.img)
        self.font = ImageFont.load_default()
        self.tfont = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',16)

    def command(self, cmdset):
        d = []
        for c in cmdset:
            d.extend((0x80,c))
        self.dev.write(d) 

    def display(self, on=None):
        if on:
            self.command([0xaf])
            return
        elif on is False:
            self.command([0xae])
            return
        gd = [0x40]
        gd.extend([0] *(128*8))
        p = self.img.load()
        for pg in range(8):
            for col in range(128):
                b = 0
                for i in range(8):
                    b = b >> 1
                    b |= 0 if p[(col, pg*8 +i)] == 0 else 0x80
                gd[pg*128 +col+1] = b
        self.command([0x21,0,127,0x22,0,7])
        self.dev.write(gd)

    def clear(self):
        self.draw.rectangle((0,0,127,63),outline=0,fill=0)
        self.display()

    def text(self,pos,msg,ttc=False):
        self.draw.text(pos,msg,font=self.tfont if ttc else self.font, fill=255)

    def close(self):
        self.display(on=False)
        self.dev.close()
    
    def start_scroll(self,dir,pg_start,pg_end,rows=None):
        cmd = [0x29] if rows else [0x26]
        cmd[0] += dir
        cmd.extend([0,pg_start,0,pg_end,rows,0x2f] if rows else [0,pg_start,0,pg_end,0,0xff,0x2f])
        self.stop_scroll()
        self.command(cmd)

    def stop_scroll(self):
        self.command([0x2e])
        self.display()
