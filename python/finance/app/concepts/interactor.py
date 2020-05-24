class Interactor():
  def __init__(self):
    self.operation_message = ''
    self.operation_status = 0

  def _interact(self, steps):
    for step in steps:
      step()

      if self.operation_status != 0:
        return None
