
from aiohttp.web import Application, RouteTableDef, Request, Response, run_app

TOKEN: str = "EAALQZBko5cOEBAPIAMwZAGWkMlZCfDAonaZBZCFuJlULwl9DsrMNI8ZCy7h1zNOkNm4JTSqZA9DLpS70fP3J26NOcwYGrgzAwWIl5BtAavoZCvpktl8ZA2HUg3oXgZCcZCnffgtJpfITi1ymAo8EVLqLTkZBYUSOam1IPMGqf5UQ8MtpZBX1wXKUzcBHZB"
VERIFICATION_TOKEN: str = "2x1pmp2of11-mvvoa"
PORT: int = 6541
HOST: str = "localhost"

app: Application = Application()

routes: RouteTableDef = RouteTableDef()


@routes.get("/facebook")
async def validation(request: Request) -> Response:
    print(await request.read())
    if request.query.get("hub.verify_token") == VERIFICATION_TOKEN:
        return Response(text=request.query.get("hub.challenge"))

    return Response(text="Not validated")


@routes.post("/facebook")
async def event(request: Request) -> Response:
    print(await request.read())
    return Response(text="", status=200)


app.add_routes(routes)

if __name__ == '__main__':
    run_app(app, port=PORT, host=HOST)
