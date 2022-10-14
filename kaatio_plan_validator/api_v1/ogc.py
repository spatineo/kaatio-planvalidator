from osgeo import gdal


class GdalErrorHandler(object):
    def __init__(self):
        self.err_level = gdal.CE_None
        self.err_no = 0
        self.err_msg = ""

    def handler(self, err_level, err_no, err_msg):
        self.err_level = err_level
        self.err_no = err_no
        self.err_msg = err_msg


gdal_err = GdalErrorHandler()
gdal.PushErrorHandler(gdal_err.handler)
gdal.UseExceptions()
