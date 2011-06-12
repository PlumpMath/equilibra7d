class Manager(object):
    def setup(self):
        """Reset manager to default configuration"""
        raise NotImplementedError
    
    def clear(self):
        """Remove manager state"""
        raise NotImplementedError

