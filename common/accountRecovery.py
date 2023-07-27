
class AccountRecovery(web.View):
    def __init__(self):
        pass

    async def get(self):
        token = request.match_info.get('token', "None")
        data = session_token.find_one({"Token":token},{"_id":0,"createdAt":0})
        if data is None:
            return web.Response(text="link Expired")
        else:
            # print(token,data)
            mail_context = {}
            response = aiohttp_jinja2.render_template("password_correction.html", request, context=mail_context)
            return response

    async def post(self):
        return web.Response(text="Post Method")