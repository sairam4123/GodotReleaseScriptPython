# GodotReleaseScriptPython
A release script made by me to export Godot projects with ease

# FAQ

## 1. What does it do?:
- A: Manages versioning and releasing the game.

## What doesn't it do?
- A: Creates Godot Projects and configures exports.

## Are there any prerequisites?
- A: Yes, there are some prerequisites to use this.  
    1. Godot project.  
        - Without Godot project in the root folder, this tool won't work.
    2. Configured Export Presets.
        - To use this tool, you should have configured export presets.
    3. File System.
        - This tool uses the project.godot and export_presets.cfg to create builds.
        - So, you should make sure to keep the Godot project in the root folder and place this in releases folder. 
        - Like this, `root/releases/`, here root is where the project.godot lies.  
    4. 7zip and Godot in Path. (For Windows only) (I don't know about Linux and Mac. I'll let you know soon.)
        - Keep the 7zip and Godot in Path. (Make sure that 7zip and Godot executable is installed and set in Path.)

## How should I use this? 
- First, run the make_release.bat.
![img](https://i.imgur.com/deIEZ1K.png) You will get something like this.  
- Then, press c and enter twice. It should look like this. ![img](https://i.imgur.com/VHOzHdF.png)
- Then, type `yes`. It should initialize like this. ![img](https://i.imgur.com/sqynZRu.png)
- Now, close the window and reopen it again.
- Do same as second step, and on the third question type `no`.
- Then on the last question, select yes. Now it will generate you a build, this is your first build. It should take a while and generate all the builds and create all file paths. Here's a video showing how it works. ![video](https://streamable.com/mtfdwn)
- The build files will be located in this path, `root/releases/{project_name}/Public/v0.1.0/`. There will be three builds, Windows, Mac and Linux. (Mac build doesn't work well, improving it.)

# What's the use of other two questions?
- It is used for making next releases.
- As I previously said, this tool comes with versioning system.
- The first question reads like this, `What type of release do you want to make?`. This means that which number do you want to increase, like do you want to release a major version, ect.
- The second question reads like this, `Which release level do you want your release be set?`. This means that which release level such as Alpha, beta, RC, public ect, be set to your release. The level of release changes the folder which the game builds, like when you set to Alpha,
it exports your game to `root/releases/{project_name}/Alpha/{version}`. Same for others. Beta => Beta, RC => Release Candidate and Public => Public.
- It also manages your serial number, the serial number starts from 0 and uses this regex, `(\d)\.(\d)\.?(\d)?\.?(\d)?\.?([a-z]{1,2})?(\d{1,3})?` You can take a look into this, https://regex101.com/r/8Dcvts/1.
- Examples: 
   1. v0.1.0 (Initial release)
   2. v0.2.0 (Minor release)
   3. v0.2.1 (Bugfix release)
   4. v0.3.0a0 (Alpha release)
   5. v0.3.0a1 (Alpha release)
   6. v0.3.0b0 (Beta release)
   7. v0.3.0b1 (Beta release)
   8. v0.3.0rc0 (RC release)
   9. v0.3.0 (Minor release)
   10. v0.3.1 (Patch or bugfix)
   11. v0.3.1.1 (Hotfix)
   12. v1.0.0 (Major release)  
#### Hope my tool would be helpful for you.
You can always contact me on Discord (Sairam#1724) or Guilded (Sairam)