class Cryptocurrency:
  def __init__(self, name, value, change24h):
    self.name = name
    self.value = value
    self.change24h = change24h

  def to_json(self):
      return dict(name = self.name,
                  value = self.value,
                  change24h = self.change24h)