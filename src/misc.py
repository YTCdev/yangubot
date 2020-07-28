from config import Config


class Misc:
    @staticmethod
    def is_staff(ctx):
        roles = [role.id for role in ctx.author.roles]
        return any(id in roles for id in Config.STAFF_IDS)
