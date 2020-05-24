from ..interactor import Interactor

from helpers import lookup

class Quote(Interactor):
  def __init__(self, request):
    self.request = request
    
    super().__init__()

  def call(self):
    steps = [
      self.__request_stock_info
    ]

    self._interact(steps)

  def __request_stock_info(self):
    symbol = self.request.form.get("symbol")
    self.quote_result = lookup(symbol)

    if not self.quote_result:
      self.operation_message = 'invalid symbol'
      self.operation_status = 422
      return