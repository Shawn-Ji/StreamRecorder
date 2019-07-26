import liveplatform.douyu
import liveplatform.huya

def live_platform_factory(platform_name):
    if platform_name == "douyu":
        return liveplatform.douyu.Douyu()
    elif platform_name == "huya":
        return liveplatform.huya.Huya()
    else:
        return None
