from fastapi import FastAPI

from .api_v1 import routes

description = """
Tässä kuvattu rajapinta simuloi [KAATIO-projektissa](https://spatineo.github.io/ry-tietomallit/kehitys/kaatio/) määritellyn XML-muotoisen kaavatiedon tallennusrajapintaa. Rajapinta on laadittu KAATIO-hankkeen aikaista ohjelmistojen testausta varten, eikä se ole tarkoitettu operatiiviseen käyttöön.

Rajapinta ottaa vastaan XML-muotoisen kaavan paketoituna `LandUseFeatureCollection`-juurielementin sisään, kuten kuvattu [Esimerkit](https://spatineo.github.io/ry-tietomallit/kehitys/kaatio/xml/esimerkit/)-sivulla. Lähetettäviä tiedostoja ei tallenneta mihinkään.
"""

app = FastAPI(
    contact={
        "name": "Spatineo Inc.",
        "email": "support@spatineo.com",
    },
    description=description,
    license_info={
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
        "name": "GPL v3.0",
    },
    title="Kaava-XML:n simuloitu tallennuspalvelu",
)


app.include_router(
    prefix="/v1",
    router=routes.router,
)
