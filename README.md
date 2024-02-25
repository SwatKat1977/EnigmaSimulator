# EnigmaSimulator

A software simulator of the World War II German Enigma encryption machine.

The simulator will eventually allow different models of the machine to be configured with various rotors or reflectors.  The initial version will concentrate on the Enigma 1 model.

The project is designed to be educational and released in the hope it will be useful and entertaining.

## Enigma Machine Variants

Implemented|Supported|Short Name|No. of Rotors|Reflector|Plugboard|Decription|
---------|---------|----------|-------------|---------|---------|----------|
|N| Y       |	Enigma1  | 3           | fixed position | optional | The main Enigma machine used by the German Army |
|N| Y       | M3       | 3      	   | fixed position | optional | used by the German Navy (Kriegsmarine). |
|N| N       | M4       | 4      	   | fixed position | Yes | Used exclusively by the U-boat division of the German Navy (Kriegsmarine)|
|N| N       | Swiss-K  | 3           | settable, not rotating | No | All Enigma K machines were delivered by the Germans with the standard commercial wheel wiring, also known from the Enigma D |
|N| N       |	Enigma KD | 3          | settable, not rotating | No | A standard commercial Enigma K machine with a rewirable reflector (UKW-D). |
|N| N       |	Railway | 3            | settable, not rotating | No | During WWII, the Germans used a special Enigma machine for the German Railway (Reichsbahn). |
|N| N       |	Tirpitz | 3            | settable, not rotating | No | The Enigma T (Tirpitz) was a special version of the Enigma K that was made for the Japanese Army during WWII. |
|N| N       |	Zählwerk | 3            | settable, and rotating | No | The Enigma T (Tirpitz) was a special version of the Enigma K that was made for the Japanese Army during WWII. |
