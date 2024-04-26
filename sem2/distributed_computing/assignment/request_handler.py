import requests
from common import ServerRequestData

class RequestHandler:

   @classmethod
   def Request(cls, requestData : ServerRequestData):
      """
      Calls request API based of preset arguments in
      requestData dictionary and downloads

      raises:
         RuntimeError

      returns:
         response dictionary
      """
      response = requests.request(
         method=requestData.method,
         url=requestData.url,
         headers=requestData.header,
         json=requestData.body,
         timeout=5
      )
      if not response.ok:
         raise RuntimeError('Request returned status code: %d'
                            % (response.status_code))

      return response.json()