import asyncio
from kasa import SmartPlug, SmartDevice, SmartStrip
# dev = SmartDevice("192.168.1.232")

############################################################################
# from macos terminal
# kasa discover
############################################################################

class LightControl():
  def __init__(self):
    print('Lights enabled')
    # self.dev = SmartPlug("192.168.1.232")
    self.devices = {}
    self.lightsready = False

  def start(self):
    self.devices['powerstrip'] = SmartStrip('192.168.37.210')
    # self.devices['powerstrip2'] = SmartStrip('192.168.37.210')
    # self.devices['powerstrip'] = SmartStrip('192.168.8.185')
    # self.devices['plug'] = SmartPlug('192.168.8.121')
    # self.devices['powerstrip'] = SmartStrip('192.168.1.210')
    # self.devices['plug'] = SmartPlug('192.168.1.231')
    self.lightsready = True
    return self
  
  # asyncio.run(self.devices['powerstrip'].turn_off())
  # asyncio.run(self.devices['powerstrip'].children[2].turn_on())
  # asyncio.run(self.devices['powerstrip'].update())
  # strip.is_on

  # asyncio.run(test())

  async def test (self):
    print('test lights')
    await self.devices['plug'].update()
    await self.devices['plug'].turn_on()
    await asyncio.sleep(0.5)
    await self.devices['plug'].turn_off()
    # asyncio.run(dev.turn_off())
    # asyncio.run(dev.turn_on())
    # asyncio.run(dev.update())
  
  async def testStrip (self, dur=0.5):
    print('test power strip 1, 2, 3')
    await self.devices['powerstrip'].update()
    await self.devices['powerstrip'].children[0].turn_on()
    await asyncio.sleep(dur)
    await self.devices['powerstrip'].children[1].turn_on()
    await asyncio.sleep(dur)
    await self.devices['powerstrip'].children[2].turn_on()
    await asyncio.sleep(dur)
    await self.devices['powerstrip'].children[0].turn_off()
    await asyncio.sleep(dur)
    await self.devices['powerstrip'].children[1].turn_off()
    await asyncio.sleep(dur)
    await self.devices['powerstrip'].children[2].turn_off()
    await asyncio.sleep(dur)
    # await self.devices['powerstrip'].turn_off()

  async def onPlugLight (self):
    await self.devices['plug'].update()
    await self.devices['plug'].turn_on()

  async def onLight (self, lightkey):
    # dev = SmartPlug("192.168.1.232")
    await self.devices['powerstrip'].update()
    await self.devices['powerstrip'].children[lightkey].turn_on()

  async def offLight (self, lightkey):
    # dev = SmartPlug("192.168.1.232")
    await self.devices['powerstrip'].update()
    await self.devices['powerstrip'].children[lightkey].turn_off()
  
  async def onLight2 (self, lightkey):
    await self.devices['powerstrip'].update()
    await self.devices['powerstrip'].children[lightkey].turn_on()
    # await self.devices['powerstrip2'].update()
    # await self.devices['powerstrip2'].children[lightkey].turn_on()
  
  async def offLight2 (self, lightkey):
    await self.devices['powerstrip'].update()
    await self.devices['powerstrip'].children[lightkey].turn_off()
    # await self.devices['powerstrip2'].update()
    # await self.devices['powerstrip2'].children[lightkey].turn_on()

  async def flashLight2 (self, lightkey, times=3, dur=0.5):
    for i in range(times):
      await self.onLight2(lightkey)
      await asyncio.sleep(dur)
      await self.offLight2(lightkey)
      await asyncio.sleep(dur)
  
  # def flashLight2 (self, lightkey, times, dur=0.25):
  #   flasher = self.flasher2(lightkey, times, dur)

  async def resetLightStrip (self):
    await self.devices['powerstrip'].update()
    await self.devices['powerstrip'].children[0].turn_off()
    await self.devices['powerstrip'].children[1].turn_off()
    await self.devices['powerstrip'].children[2].turn_off()
  
  async def resetLightPlug (self):
    await self.devices['plug'].update()
    await self.devices['plug'].turn_off()

  async def resetLights (self):
    await self.resetLightStrip()
    await self.resetLightPlug()
    
  async def flashLights (self):
    # dev = SmartPlug("192.168.1.232")
    await self.devices['powerstrip'].update()
    await self.devices['powerstrip'].children[2].turn_on()
    await asyncio.sleep(2)
    await self.devices['powerstrip'].children[2].turn_off()
    
  async def flashLightsOLD (self):
    # dev = SmartPlug("192.168.1.232")
    await self.dev.update()
    await self.dev.turn_on()
    await asyncio.sleep(2)
    await self.dev.turn_off()