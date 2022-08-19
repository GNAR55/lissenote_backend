from deepmultilingualpunctuation import PunctuationModel

model = PunctuationModel(model="oliverguhr/fullstop-dutch-sonar-punctuation-prediction")

def punctaute(text):
    result = model.restore_punctuation(text)
    result = '. '.join([x.capitalize() for x in result.split('. ')])
    return result

if __name__ == "__main__":
    text = '''
    digital systems have such prominent role in every day lift refer to the present technology rod as the system a communication business transactions ati guidance medical treatment when the one internet and many of the metal industrial and scientific we have lesion by is cameras hand devices and of case computers then join in down load a player example i part and other devices have an higher resolution these devices have graphically using inter cases which execute commands that apart user to the but which in fact precision of sequence of plates internal instructions most if not of the devices have special varied the most string property outer it flue of nuctions called the program that operate on given data the can specify and change program of data according to the specific because of this flexibility in general outer can perform a variety of on processing tasks that range over wide spectrum of application characteristic systems it represent a manipulatite elements of ton is restricted to finite number of elements criteamples of discrete sets are the ten decipledejicts the twenty rate of the alphabet to playing parts and sixty for square of specular computer use enumerating
    '''
    print(punctaute(text))

