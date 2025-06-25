from logger import fileLog as fl
def createEmtpySettings():
    with open('config/config.json', 'w') as file:
        file.write("Hello!")