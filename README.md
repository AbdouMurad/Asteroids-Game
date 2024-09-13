Classic Asteroids Game is made to implement more realistic physics using simple equations to apply forces on objects. 
- The gravitational constant is exaggerated to provide better gameplay and can be adjusted from the CONST script.
- Every level one more asteroid spawns, and at levels 3-5 an enemy spawns, at level 6-8 2 enemies spawn and so on.
- Enemies are controlled using an adaptive targeting behavior, where depending on the percent of shots hit, the error margin of the enemies aim will increase/decrease to maintain a level of difficulty.

CONTROLS:
W - Apply force to the ship -> force affects acceleration meaning there is no cap on the ship's velocity

A - Rotate Left

D - Rotate Right

S - Proton Wave -> When the blue bar at the bottom left is full, a circular wave is created at the player ship and extends outwards destroying everything within its radius
![image](https://github.com/user-attachments/assets/a24014c2-a752-4ac0-8bc6-ed83a38903c0)


SHIFT - Portal -> Create a 2-ended portal that teleports the player from one gate to the other (with a time cooldown in between) and gives the player a small health boost. Only works when the white bar in the bottom left is full. Only one portal is active at once and 
using this again destroys the first portal and creates a new one

LCTRL - Time Freeze -> When holding this button, time is processed at half speed. Everything is slowed down proportionally but it allows the player to see the surroundings for a short period and plan a move

SPACE - Fire -> Fire bullets from the player ship. The bullets carry the ship's original velocity creating a momentum effect, this means if the ship is traveling at a high speed and fires in the opposite direction, the bullets will travel very slowly because their momentum is carrying them backwards. 
