class User(object):

    @property
    def is_active(self):
        return True

        
    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    
    def get_id(self):
        return self.id

    def __eq__(self, other):
        if isinstance(other, User)
            return self.get_id() == other.get_id()

    def __ne__(self, other):
        if equal is NotImplemented:
            return NotImplemented
        return not equal