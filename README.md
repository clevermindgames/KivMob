![KivMob](https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/kivmob-title.png)

Provides interface for [Kivy] applications to access [Google Admob] functionalty on Android devices.

  - No need to change internal Android project manifest templates, Java code, or manually add external libraries.
  - Support for interstitial, banner and Rewarded Video ads.

### Demo Screenshot

<p align="center">
  <img src="https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/demo-screenshot-github.png">
</p>

### Installation

Download python-for-android-kivmob27 and install KivMob27 using the following commands.
```sh
$ git clone https://github.com/clevermindgames/python-for-android-kivmob27.git
```
### Tutorial & Build Instructions

This tutorial assumes you are familiar with AdMob. Additionally, be sure that you have the latest version of [Buildozer] installed, as KivMob uses the android_new toolchain.

Create a new directory. Copy the following and paste it into a new main.py file. Be sure to include your AdMob app ID, your test device ID, REWARDED_ID and interstitial ID.
copy kivmob27.py from this repo to the same directory

```python
from kivmob27 import KivMob
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

class KivMobTest(App):
    ads = ObjectProperty(allownone=True)
    
    def build(self):
        self.ads = KivMob("APP_ID")
        self.ads.add_test_device("TEST_DEVICE_ID")
        self.ads.new_interstitial("INTERSTITIAL_ID")
        self.ads.request_interstitial()
        self.ads.new_rewarded("REWARDED_ID")
        self.ads.request_rewarded()
        bl = BoxLayout(orientation='vertical')
        b1 = Button(text='Show Interstitial',
                      on_release= lambda a:ads.show_interstitial())
        b2 = Button(text='Show Rewarded',
                      on_release= lambda a:ads.show_rewarded(reward_type='your reward type'))
        bl.add_widget(b1)
        bl.add_widget(b2)
        return bl

    def on_resume(self):
        res = self.ads.get_reward_type()
        if res != "No reward":
            #Give reward based on reward_type
            self.reward(res)

    def reward(self, reward_type)
        #reward the player
        self.ads.playerRewarded() #reset the reward so it is not triggered again

KivMobTest().run()
```

In the same directory, generate buildozer.spec and make the following changes.

```sh
android.api = 27
android.minapi = 19
requirements = kivy, hostpython2, android, kivmob27, jnius
android.permissions = INTERNET, ACCESS_NETWORK_STATE
android.p4a_dir = # dir/to/python-for-android-kivmob27/
android.gradle_dependencies = 'com.google.android.gms:play-services-ads:16.0.0','com.android.support:appcompat-v7:26.1.0'
```

To build and deploy the project, run the following command. Wait a few moments for the ad to load before pressing the button.

```sh
$ buildozer android release
```

<p align="center">
  <img src="https://raw.githubusercontent.com/MichaelStott/KivMob/master/demo/assets/tutorial-screenshot.png">
</p>

Look under the demo folder for a more extensive example for interstitials and banners

### Todo
 - Add in-App purchases
 - Finish remaining unimplemented methods in AdMobBridge interface.
 - Write documentation.
 - Develop Buildozer recipe for KivMob that would make changes to Android project, download AdMob library, and provide Java backend. (Eliminating need for python-for-android-admob)

### Future Work
 - Layout that repositions widgets when banner ad is displayed.
 - iOS support.

[Google Admob]: <https://www.google.com/admob/>
[Kivy]: <https://kivy.org/>
[Buildozer]: <https://github.com/kivy/buildozer>
[MichaelStott Kivmob]: <https://github.com/MichaelStott/KivMob>
