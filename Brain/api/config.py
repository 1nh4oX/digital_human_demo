PORT = 5199

def export_to_frontend():
    with open("Front/digital-human-front/public/port.json", "w") as f:
        f.write(f'{{"port": {PORT}}}')