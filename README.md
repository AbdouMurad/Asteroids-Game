Classic Asteroids Game is made to implement more realistic physics using simple equations to apply forces on objects. 

Newton's second law is implemented by moving objects only through applied forces. Asteroids and players also have a gravitational force pulling them together depending on their masses.

By destroying small asteroids, the player has a chance of receiving a power-up. The corresponding icon of the power-up will turn on in the bottom corner. These powerups include a smaller wait time for proton wave, double 
fire rate, and double the score received for destroying asteroids and enemies. The only power-up that does not have an icon is the health power-up, which will refill the player's health.
The remaining indicators are bars that indicate the time until the next use of the player's abilities. The top one indicates how much freeze time the player has available (how long can the player slow time for), the one 
under indicates the time until the player can place a dimensional passage, the one under shows the time until the next proton wave, and finally, the final bar shows the player's current health
![image](https://github.com/user-attachments/assets/a203fdd5-190c-4de2-86f8-3fb0d862b7aa)

CONTROLS:

W - Apply force to the ship -> force affects acceleration meaning there is no cap on the ship's velocity

A - Rotate Left

D - Rotate Right

S - Proton Wave -> When the blue bar at the bottom left is full, a circular wave is created at the player ship and extends outwards destroying everything within its radius
![image](https://github.com/user-attachments/assets/a24014c2-a752-4ac0-8bc6-ed83a38903c0)


SHIFT - Dimensional Passage -> Create a 2-ended portal that teleports the player from one gate to the other (with a time cooldown in between) and gives the player a small health boost. Only works when the white bar in the bottom left is full. Only one portal is active at once and 
using this again destroys the first portal and creates a new one
![image](https://github.com/user-attachments/assets/fddc8fa3-0313-43f3-95a3-0a9801217380)

LCTRL - Time Freeze -> When holding this button, time is processed at 1/3 of the normal speed. Everything is slowed down proportionally but it allows the player to see the surroundings for a short period and plan a move
![image](https://github.com/user-attachments/assets/343aef50-5527-4fce-9eb9-d658525a66cc)

SPACE - Fire -> Fire bullets from the player ship. The bullets carry the ship's original velocity creating a momentum effect, this means if the ship is traveling at a high speed and fires in the opposite direction, the bullets will travel very slowly because their momentum is carrying them backward. 

The enemies were designed using an adaptive targeting system. By determining the distance between the enemy and the player and using the velocities of both ships, the enemy can predict the location in which the player is headed to. Using this the enemy hoams in on that position which is being constantly updated and fires in that direction. Initially, this simple procedure proved to be too successful and the enemies were too strong. To adjust to this, an error margin was introduced which significantly lowered the accuracy of the enemy. Then based on how many shots the enemy was hitting, the error margin would either decrease or increase which meant the enemy would eventually hit an accuracy percent in which it was neither missing too many shots nor hitting too many shots. Based on experience from play testing the game, with the new model the enemy hits around 20$ of the shots they fire which is still a high accuracy rate but not too high that the game becomes unplayable. 

Gameplay available on LinkedIn: https://www.linkedin.com/feed/update/urn:li:activity:7240063514294243328/
