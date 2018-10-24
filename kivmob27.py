from kivy.utils import platform
from kivy.logger import Logger

if platform == 'android':
    try:
        from android.runnable import run_on_ui_thread
    except:
         pass
else:
    def run_on_ui_thread(x):
        pass


class AdMobBridge():
    """ Interface for communicating with native AdMob library.
    """

    def __init__(self, appID):
        """ Initialize platform specific features here.
        """
        Logger.info('KivMob: __init__ called.')
        
    def add_test_device(self, testID):
        """ Add a test device.
        """
        Logger.info('KivMob: add_test_device() called.')

    def is_interstitial_loaded(self):
        Logger.info('KivMob: is_interstitial_loaded() called.')
        return False

    def is_rewarded_loaded(self):
        Logger.info('KivMob: is_rewarded_loaded() called.')
        return False
        
    def new_banner(self, options):
        """ Create a new banner ad.
        """
        Logger.info('KivMob: new_banner() called.')

    def new_interstitial(self, unitID):
        """ Create a new interstitial ad.
        """
        Logger.info('KivMob: new_interstitial() called.')

    def new_rewarded(self, unitID):
        """ Create a new rewarded ad.
        """
        Logger.info('KivMob: new_rewarded() called.')
    
    def request_banner(self, options):
        """ Requests new banner ad.
        """
        Logger.info('KivMob: request_banner() called.')

    def request_interstitial(self, options):
        """ Requests new interstitial ad.
        """
        Logger.info('KivMob: request_interstitial() called.')

    def request_rewarded(self):
        """ Requests new rewarded ad.
        """
        Logger.info('KivMob: request_rewarded() called.')
        
    def show_banner(self):
        """ If possible, show banner ad.

        NOTE: You must call request_banner() beforehand!
        """
        Logger.info('KivMob: show_banner() called.')

    def playerRewarded(self):
        Logger.info('KivMob: playerRewarded() called.')        

    def show_interstitial(self):
        """ If possible, show interstitial ad.

        NOTE: You must call request_interstitial() beforehand!
        """
        Logger.info('KivMob: show_interstitial() called.')

    def show_rewarded(self, reward_type=""):
        """ If possible, show rewarded ad.

        NOTE: You must call request_rewarded() beforehand!
        """
        Logger.info('KivMob: show_rewarded() called.')
    
    def destroy_banner(self):
        """ Destory current banner ad.
        """
        Logger.info('KivMob: destroy_banner() called.')

    def destroy_interstitial(self):
        """ Destroy interstitial ad.
        """
        Logger.info('KivMob: destroy_interstitial() called.')

    def hide_banner(self):
        """ Hide banner ad.
        """
        Logger.info('KivMob: hide_banner() called.')

    def get_reward_type(self):
        Logger.info('KivMob: get_reward_type() called.')
        return ""


class AndroidBridge(AdMobBridge):
    
    @run_on_ui_thread
    def __init__(self, appID):
        self._loaded = False
        self._rewarded_loaded = False
        self._reward_type = ""

        from jnius import autoclass, cast
        self.activity = autoclass('org.kivy.android.PythonActivity')
        self.Cmd = autoclass('org.kivy.android.PythonActivity$AdCmd')
        self.Handler = autoclass('org.kivy.android.PythonActivity').adHandler
        self.Message = autoclass('android.os.Message')
        self.Bundle = autoclass('android.os.Bundle')

        self.Handler.sendMessage(self._build_msg(self.Cmd.INIT_ADS.ordinal(),
                                            {"appID":appID}))
        
    @run_on_ui_thread
    def new_banner(self, options={}):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.NEW_BANNER.ordinal(), options))
        
    @run_on_ui_thread
    def new_interstitial(self, unitID):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.NEW_INTERSTITIAL.ordinal(), {"unitID":unitID}))

    @run_on_ui_thread
    def new_rewarded(self, unitID):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.NEW_REWARDED.ordinal(), {"unitID":unitID}))

    @run_on_ui_thread
    def add_test_device(self, deviceID):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.ADD_TEST_DEVICE.ordinal(), {"deviceID":deviceID}))

    @run_on_ui_thread
    def request_banner(self, options={}):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.REQ_BANNER.ordinal(), options))
        
    @run_on_ui_thread
    def request_interstitial(self, options={}):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.REQ_INTERSTITIAL.ordinal(), options))

    @run_on_ui_thread
    def request_rewarded(self):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.REQ_REWARDED.ordinal()))

    @run_on_ui_thread
    def _is_interstitial_loaded(self):
        self._loaded = self.activity.isLoaded()

    @run_on_ui_thread
    def _is_rewarded_loaded(self):
        self._rewarded_loaded = self.activity.isRewardedLoaded()

    @run_on_ui_thread
    def _get_reward_type(self):
        self._reward_type = self.activity.getRewardType()

    @run_on_ui_thread
    def playerRewarded(self):
        self.activity.playerRewarded()

    def get_reward_type(self):
        self._get_reward_type()
        return self._reward_type

    def is_interstitial_loaded(self):
        # Values returned from run_on_ui_thread appear as
        # NoneType. Setting the result to private variable
        # self._loaded before returning solves this issue.
        self._is_interstitial_loaded()
        return self._loaded

    def is_rewarded_loaded(self):
        self._is_rewarded_loaded()
        return self._rewarded_loaded

    @run_on_ui_thread
    def show_banner(self):
        self.Handler.sendEmptyMessage(self.Cmd.SHOW_BANNER.ordinal())
        
    @run_on_ui_thread
    def show_interstitial(self):
        self.Handler.sendEmptyMessage(self.Cmd.SHOW_INTERSTITIAL.ordinal())

    @run_on_ui_thread
    def show_rewarded(self, reward_type=""):
        self.Handler.sendMessage(self._build_msg(
            self.Cmd.SHOW_REWARDED.ordinal(), {"reward_type": reward_type}))
        

    @run_on_ui_thread
    def hide_banner(self):
        self.Handler.sendEmptyMessage(self.Cmd.HIDE_BANNER.ordinal())

    def _build_msg(self, ordinal, options):
        # Builds message to for controlling admob backend.
        msg = self.Message.obtain()
        msg.what = ordinal
        bundle = self.Bundle()
        for key, value in options.iteritems():
            if isinstance(value, bool):
                bundle.putBoolean(key,value)
            elif isinstance(value, int):
                bundle.putInt(key,value)
            elif isinstance(value, float):
                bundle.putDouble(key, value)
            elif isinstance(value, basestring):
                bundle.putString(key, value)
        msg.setData(bundle)
        return msg


class iOSBridge(AdMobBridge):
    # TODO
    pass


class KivMob():

    def __init__(self, appID):
        if platform == 'android':
            Logger.info('KivMob: Android platform detected.')
            self.bridge = AndroidBridge(appID)
        elif platform == 'ios':
            Logger.warning('KivMob: iOS not yet supported.')
            self.bridge = iOSBridge(appID)
        else:
            Logger.warning('KivMob: Ads will not be shown.')
            self.bridge = AdMobBridge(appID)

    def add_test_device(self, device):
        self.bridge.add_test_device(device)

    def get_reward_type(self):
        return self.bridge.get_reward_type()
    
    def new_banner(self, options={}):
        self.bridge.new_banner(options)

    def new_interstitial(self, options={}):
        self.bridge.new_interstitial(options)

    def playerRewarded(self):
        self.bridge.playerRewarded()

    def new_rewarded(self, options={}):
        self.bridge.new_rewarded(options)

    def is_interstitial_loaded(self):
        return self.bridge.is_interstitial_loaded()

    def is_rewarded_loaded(self):
        return self.bridge.is_rewarded_loaded()

    def request_banner(self, options={}):
        self.bridge.request_banner(options)
        
    def request_interstitial(self, options={}):
        self.bridge.request_interstitial(options)

    def request_rewarded(self):
        self.bridge.request_rewarded()
        
    def show_banner(self):
        self.bridge.show_banner()

    def show_interstitial(self):
        self.bridge.show_interstitial()

    def show_rewarded(self, reward_type=""):
        self.bridge.show_rewarded(reward_type)

    def destroy_banner(self):
        self.bridge.destroy_banner()

    def destroy_interstitial(self):
        self.bridge.destroy_interstitial()

    def hide_banner(self):
        self.bridge.hide_banner()

if __name__ == '__main__':
    print("\033[92m  _  ___       __  __       _\n" +\
          " | |/ (_)_   _|  \/  | ___ | |__\n" +\
          " | ' /| \ \ / / |\/| |/ _ \| '_ \\\n" +\
          " | . \| |\ V /| |  | | (_) | |_) |\n" +\
          " |_|\_\_| \_/ |_|  |_|\___/|_.__/\n\033[0m")
    print(" Michael Stott, 2017\n")
    
