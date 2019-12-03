# SpaceInvadersAI

Group : Alex Morales , Daniel Ariza

Space Invaders AI Project

Uses Deep Reinforcement Learning to teach an AI how to play Space Invaders

Model used for learning based on Open Source resource found on : https://medium.com/acing-ai/how-i-build-an-ai-to-play-dino-run-e37f37bdf153

Modified to better fit our game.

How To run: 
1. install all the libraries from the Requirements below on a python 2.7 environment. These can be installed using pip install command.
2. *If you are going to use keras with cntk make sure to change keras.json file and se the backend to be cntk more info can be found here:
https://docs.microsoft.com/en-us/cognitive-toolkit/Using-CNTK-with-Keras

3.once all the libraries are installed run the AI.py and the AI should be up and running 


Requirements (external libraries):
pygame==1.9.6
scipy==1.2.2
numpy==1.16.5
Keras==2.3.1
opencv_python==4.1.1.26
Pillow==6.2.1
cntk==2.7 //used as keras backend could be replaced with tensorflow 
