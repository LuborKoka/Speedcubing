from fastapi.responses import HTMLResponse
from app.constants import TEMPLATES
from app.services.scramble_service import ScrambleService

class ScrambleController:
    @classmethod
    def get_scramble_view(cls, puzzle: str):
        scramble = ScrambleService.generate_scramble(puzzle)
        html = TEMPLATES.get_template('templates/scramble.html').render({
            'scramble': scramble
        })

        return HTMLResponse(html)