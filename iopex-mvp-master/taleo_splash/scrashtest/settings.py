BOT_NAME = 'scrashtest'
FEED_EXPORT_ENCODING = 'utf-8'
AUTOTHROTTLE_ENABLED = True
SPIDER_MODULES = ['scrashtest.spiders']
NEWSPIDER_MODULE = 'scrashtest.spiders'
CONCURRENT_REQUESTS =10

DOWNLOADER_MIDDLEWARES = {
 # Engine side
 'scrapy_splash.SplashCookiesMiddleware': 723,
 'scrapy_splash.SplashMiddleware': 725,
 'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
 'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 350,

 # Downloader side
}

SPIDER_MIDDLEWARES = {
 'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
SPLASH_URL = 'http://10.20.103.95:8050/'

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'