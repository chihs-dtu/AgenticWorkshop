# Introduction to agentic thinking


## Using OpenCode - CLI
First create a project folder, perhaps start a project hierachy. Anything you create - data, files, programs, agents, skills - lives in the folder.<br>
Go to the folder and start OpenCode. 

## Skill example: PDB download
Create skill that you interactively can use and is also usable by agents.

In OpenCode start the ''Plan'' mode. Simply write on the command prompt:<br>
"Create a skill that downloads a pdb file"<br>
The AI will start thinking and maybe ask a few follow-up questions, which you answer. Eventually it says it is ready, and you change to "Build" mode and asks it to implement the skill.
After the build, you switch back to "Plan" mode and ask it to improve it to add a checksum check into the pdb download skill based on file checksums found on the download site and add some structural
validation of the download pdb file, if that is not done already. You might again encounter some clarifying questions from the AI. Eventually switch to "Build" mode to improve the skill.<br>
Stop OpenCode by typing "exit" and start it again. Now the skill is always present and can be used anytime, like "download 4hhb" or "download the pdb files named in to_download.txt".

The take-home message here is that skills are created by a conversation between you and the AI about what the skill should do and how it should verify the correctness of the skills actions.
The conversation (planning) should not be "too" big/complicated as that means could be split up in several simpler skills, which may be used by an agent.
