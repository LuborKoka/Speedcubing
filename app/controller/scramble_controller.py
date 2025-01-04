from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.scramble_service import ScrambleService

TEMPLATES = Jinja2Templates(directory="./app/view")

class ScrambleController:
    @classmethod
    def get_scramble_view(cls, puzzle: str):
        scramble = ScrambleService.generate_scramble(puzzle)
        html = TEMPLATES.get_template('templates/scramble.html').render({
            'scramble': scramble
        })

        return HTMLResponse(html)