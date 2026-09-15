# Introduction to agentic thinking


## Using OpenCode - CLI
First create a project folder, perhaps start a project hierachy. Anything you create - data, files, programs, agents, skills - lives in the folder.<br>
Go to the folder and start OpenCode.<br>
Use TAB to switch between **Plan** mode, which does nothing but talk and plan and read files, and **Build** mode, which actually creates and (re)writes files on you computer.

## Skill example: PDB download
Create skill that you interactively can use and is also usable by agents.

In OpenCode start the **Plan** mode. Simply write on the command prompt:<br>
"Create a skill that downloads a pdb file"<br>
The AI will start thinking and maybe ask a few follow-up questions, which you answer. Eventually it says it is ready, and you change to **Build** mode and asks it to implement the skill.
After the build, you switch back to **Plan** mode and ask it to improve it to add a checksum check into the pdb download skill based on file checksums found on the download site and add some structural
validation of the download pdb file, if that is not done already. You might again encounter some clarifying questions from the AI. Eventually switch to **Build** mode to improve the skill.<br>
Stop OpenCode by typing **exit** and start it again. Now the skill is always present and can be used anytime, like "download 4hhb" or "download the pdb files named in to_download.txt".

The take-home message here is that skills are created by a conversation between you and the AI about what the skill should do and how it should verify the correctness of the skills actions.
The conversation (planning) should not be "too" big/complicated as that means could be split up in several simpler skills, which may be used by an agent.

## Skill example: PDB 3D image download
Again this is a simple conversation in OpenCode **Plan** mode. Start with something like:<br>
"Create a skill to download the 3D image of a pdb entry which is already rendered at the repository"<br>
You might run into a conversation about how it should work and where the skill should be, which is perfectly normal and expected.
When you are happy with the plan, change to **Build** mode and execute - say "approved" or "build it" or something in that style.

The take-home message is that the planning phase starts the discussion of how the skill should work and when happy switch to building. It is important to exit OpenCode and start it again to load the new skill to make it become active. If there is something you do not understand about the process, then **ask** the AI to explain. The AI is doing the heavy lifting while you direct the process.

## Skill location
A skill either lives in the project you are currently working in, or globally in all OpenCode environments.
