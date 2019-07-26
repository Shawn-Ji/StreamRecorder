import liveplatform.douyu


def live_platform_factory(platform_name):
    if platform_name == "douyu":
        return liveplatform.douyu.Douyu()
    else:
        return None
