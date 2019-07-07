



class Webcrawler:

  def __init__(self, site_name, description=""):
    self.site_name = site_name
    self.description = description

   def setBaseURL(self,baseurl):
       self.baseurl = baseurl

   def setStartDate(self,start_date):
       self.start_date = start_date

   def setEndDate(self,end_date):
       self.end_date = end_date
