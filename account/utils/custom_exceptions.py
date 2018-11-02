class EmptyException(Exception):
    
    def __init__(self, message):
        self.message = message

class DuplicateUser(Exception):

    def __init__(self):
        Exception.__init__(self)

class UserNotFound(Exception):
    
    def __init__(self):
        Exception.__init__(self)

class IncorrectPassword(Exception):

    def __init__(self):
        Exception.__init__(self)


class TokenNotPresent(Exception):

    def __init__(self):
        self.message = "Auth token not found in request"

class SessionExpired(Exception):

    def __init__(self):
        Exception.__init__(self)

class AlreadyFollowingUser(Exception):

    def __init__(self):
        Exception.__init__(self)

class CannotFollowItself(Exception):
    
    def __init__(self):
        Exception.__init__(self)


class PasswordExpired(Exception):



    def __init__(self, message):
        Exception.__init__(self, message)


class LockedAccount(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class InvalidUser(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class ForceChangePassword(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class PasswordNotAllowed(Exception):

    def __init__(self, message):
        Exception.__init__(self, message)


class PasswordChangeRequiredException(Exception):

    def __init__(self, data):
        Exception.__init__(self, data)


