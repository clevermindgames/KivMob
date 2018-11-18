from kivy.utils import platform
from kivy.logger import Logger
from jnius import autoclass, cast
import jnius
try:
    PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity
except:
    PythonActivity = None

if platform == 'android':
    try:
        from android.runnable import run_on_ui_thread
    except:
         pass
else:
    def run_on_ui_thread(x):
        pass

AdCmd =  {'INIT_ADS': 0, 'ADD_TEST_DEVICE': 1, 'NEW_BANNER': 2, 'NEW_INTERSTITIAL': 3, 'REQ_BANNER': 4, 'REQ_INTERSTITIAL': 5,
          'SHOW_BANNER': 6, 'SHOW_INTERSTITIAL': 7, 'HIDE_BANNER': 8, 'NEW_REWARDED': 9, 'REQ_REWARDED': 10, 'SHOW_REWARDED': 11};


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
    
    def __init__(self, appID):
        global PythonActivity
        self._loaded = False
        self._rewarded_loaded = False
        self._reward_type = ""
        if not PythonActivity:
            PythonActivity = autoclass('org.kivy.android.PythonActivity').mActivity
        PythonActivity.adHandler.sendMessage(self._build_msg(AdCmd['INIT_ADS'], {"appID":appID}))


    def new_banner(self, options={}):
        PythonActivity.adHandler.sendMessage(self._build_msg(AdCmd['NEW_BANNER'], options))
        

    def new_interstitial(self, unitID):
        PythonActivity.adHandler.sendMessage(self._build_msg(AdCmd['NEW_INTERSTITIAL'], {"unitID":unitID}))
        

    def new_rewarded(self, unitID):
        PythonActivity.adHandler.sendMessage(self._build_msg(AdCmd['NEW_REWARDED'], {"unitID":unitID}))
        

    def add_test_device(self, deviceID):
        PythonActivity.adHandler.sendMessage(self._build_msg(AdCmd['ADD_TEST_DEVICE'], {"deviceID":deviceID}))
        

    def request_banner(self, options={}):
        PythonActivity.adHandler.sendEmptyMessage(AdCmd['REQ_BANNER']) #mActivity.req_banner()#


    def request_interstitial(self, options={}):
        PythonActivity.adHandler.sendEmptyMessage(AdCmd['REQ_INTERSTITIAL']) #mActivity.req_interstitial()
            

    def request_rewarded(self):
        PythonActivity.adHandler.sendEmptyMessage(AdCmd['REQ_REWARDED'])
        

    @run_on_ui_thread
    def _is_interstitial_loaded(self):
        self._loaded = PythonActivity.isLoaded()
        

    @run_on_ui_thread
    def _is_rewarded_loaded(self):
        self._rewarded_loaded = PythonActivity.isRewardedLoaded()

    def _get_reward_type(self):
        self._reward_type = PythonActivity.getRewardType()

    def playerRewarded(self):
        PythonActivity.playerRewarded()
        

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

    def show_banner(self):
        PythonActivity.adHandler.sendEmptyMessage(AdCmd['SHOW_BANNER'])
        
    def show_interstitial(self):
        PythonActivity.adHandler.sendEmptyMessage(AdCmd['SHOW_INTERSTITIAL'])
        

    def show_rewarded(self, reward_type=""):
        PythonActivity.adHandler.sendMessage(self._build_msg(AdCmd['SHOW_REWARDED'], {"reward_type": reward_type}))
        

    def hide_banner(self):
        PythonActivity.adHandler.sendEmptyMessage(AdCmd['HIDE_BANNER'])
        

    def _build_msg(self, ordinal, options):
        # Builds message to for controlling admob backend.
        Message = autoclass('android.os.Message')
        Bundle = autoclass('android.os.Bundle')
        msg = Message.obtain()
        msg.what = ordinal
        bundle = Bundle()
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
        self.interstitial_id = ""
        self.banner_options = {}
        self.rewarded_id = ""
        self.ui_run_counter = 0
        self.max_ui_run_counter = 440
        self.valid_banner = True
        if platform == 'android':
            Logger.info('KivMob: Android platform detected.')
            self.bridge = AndroidBridge(appID)
        elif platform == 'ios':
            Logger.warning('KivMob: iOS not yet supported.')
            self.bridge = iOSBridge(appID)
        else:
            Logger.warning('KivMob: Ads will not be shown.')
            self.bridge = AdMobBridge(appID)
        self.ui_run_counter += 1

    def add_test_device(self, device):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.add_test_device(device)

    def get_reward_type(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            return self.bridge.get_reward_type()
        else:
            return ""
    
    def new_banner(self, options={}):
        if options:
            self.banner_options = options
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.new_banner(self.banner_options)

    def new_interstitial(self, unitID=""):
        if unitID:
            self.interstitial_id = unitID
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.new_interstitial(self.interstitial_id)

    def playerRewarded(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.playerRewarded()

    def new_rewarded(self, unitID=""):
        if unitID:
            self.rewarded_id = unitID
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.new_rewarded(self.rewarded_id)

    def is_interstitial_loaded(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            return self.bridge.is_interstitial_loaded()
        else:
            return False

    def is_rewarded_loaded(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            return self.bridge.is_rewarded_loaded()
        else:
            return False

    def request_banner(self, options={}):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.request_banner(options)
        
    def request_interstitial(self, options={}):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.request_interstitial(options)

    def request_rewarded(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.request_rewarded()
        
    def show_banner(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.show_banner()

    def show_interstitial(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.show_interstitial()

    def show_rewarded(self, reward_type=""):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.show_rewarded(reward_type)

    def destroy_banner(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.destroy_banner()

    def destroy_interstitial(self):
        if self.ui_run_counter < self.max_ui_run_counter:
            self.ui_run_counter += 1
            self.bridge.destroy_interstitial()

    def hide_banner(self):
        if self.ui_run_counter < self.max_ui_run_counter or self.valid_banner:
            self.ui_run_counter += 1
            if self.ui_run_counter > self.max_ui_run_counter:
                self.valid_banner = False
            self.bridge.hide_banner()

if __name__ == '__main__':
    print("\033[92m  _  ___       __  __       _\n" +\
          " | |/ (_)_   _|  \/  | ___ | |__\n" +\
          " | ' /| \ \ / / |\/| |/ _ \| '_ \\\n" +\
          " | . \| |\ V /| |  | | (_) | |_) |\n" +\
          " |_|\_\_| \_/ |_|  |_|\___/|_.__/\n\033[0m")
    print(" Michael Stott, 2017\n")
    
