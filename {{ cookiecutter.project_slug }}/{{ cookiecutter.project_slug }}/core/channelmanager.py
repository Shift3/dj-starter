from django_eventstream.channelmanager import DefaultChannelManager

class UserChannelManager(DefaultChannelManager):
    def can_read_channel(self, user, channel):
        if user is None:
            return False

        if str(user.id) == channel:
            return True

        return False
