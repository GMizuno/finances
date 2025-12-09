from main import main
import os

from src.util.const import SELECT_TICKET

if __name__ == "__main__":
    event = None
    context = None
    os.environ['START'] = '30'
    os.environ['END'] = '1'
    main(event, context)
