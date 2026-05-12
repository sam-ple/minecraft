# 📝 Minescript FAQ

💬 *Some information may be outdated or incorrect. If you notice any issues, please let me know!*

---

## 🔧 What is Minescript?

* Official site: [minescript.net](https://minescript.net/)
* Discord Community: [https://discord.gg/NjcyvrHTze](https://discord.gg/NjcyvrHTze)
  *(A great place to ask questions or find community-made scripts)*
* Overview:
  Minescript allows you to control and interact with Minecraft using Python scripts.
* Mod availability:
  You can download the mod from [Modrinth](https://modrinth.com/) or [CurseForge](https://www.curseforge.com/).
  It supports **Fabric**, **Forge**, and **NeoForge** mod loaders.
* Supported environments:
  **Client-side**
* 📄 Please review the [Terms of Service of Minescript](https://github.com/maxuser0/minescript/blob/main/TERMS_OF_SERVICE.md) to ensure that your usage is compliant.

---

## 🛠️ How to Set Up Minescript

### 🟩 Default Launcher (Official Minecraft Launcher)

- 🎬 Sample My Movie: [{ How to Set Up Minescript } No Launcher) - YouTube](https://www.youtube.com/watch?v=1Monkt8_mgk)

1. Download the required mods (Minescript + dependencies).
2. Set your Python path in `config.txt`.
3. Test it with a sample script.

### 🟦 Modrinth App (Recommended for Beginners)

- 🎬 Sample My Movie: [{ How to Set Up Minescript } Modrinth (4 Simple Steps) - YouTube](https://www.youtube.com/watch?v=2TMlJIipzpI)

1. Download [Modrinth](https://modrinth.com/) and create a new instance.
2. Install the required mods (Minescript + dependencies).
3. Set your Python path in `config.txt`.
4. Test it with a sample script.

💡 *Modrinth is a free Minecraft launcher available for Windows, macOS, and Linux.*

---

## ▶️ Running a Minescript

You can run your `.py` scripts directly in Minecraft via the chat console:

* Example: A script located at
  `minecraft/minescript/example.py`
  can be run as:

  ```
  \example
  ```

---

## 🎥 Sample My Movies and 📝Sample My Code

- [Minescript Memo](https://github.com/sam-ple/minecraft/tree/sample/MEMO.md)

---

## 📁 Where to Find Your Minecraft Folder

> 💬 *Note: Some of these paths may be unverified on Windows or with CurseForge.*  
> 💡 Each instance has its own `mods/`, `saves/`, and other folders.

### 🟩 Official Minecraft Launcher

| OS      | Folder Location                                      |
| ------- | ---------------------------------------------------- |
| Windows | `%APPDATA%\.minecraft\minescript\`                               |
| macOS   | `~/Library/Application Support/minecraft/minescript/` |
| Linux   | `~/.minecraft/minescript/`                                       |

### 🟦 Modrinth App

| OS      | Folder Location                                                             |
| ------- | --------------------------------------------------------------------------- |
| Windows | `%APPDATA%\ModrinthApp\profiles\<Instance>\minescript\`     |
| macOS   | `~/Library/Application Support/ModrinthApp/profiles/<Instance>/minescript/` |
| Linux   | `~/.config/ModrinthApp/profiles/<Instance>/minescript/` |

### 🟧 CurseForge Launcher

| OS      | Folder Location                                       |
| ------- | ----------------------------------------------------- |
| Windows | `%HOMEDRIVE%%HOMEPATH%\curseforge\minecraft\instances\<Instance>\minescript\` |
| macOS   | `~/Library/Application Support/curseforge/minecraft/instances/<Instance>/minescript/` |
| Linux   | `~/.curseforge/minecraft/instances/<Instance>/minescript/` |

---

#### Tips

##### ⊞ Windows

* Press ⊞ **Windows** + **R**, type `%APPDATA%\.minecraft`, and press **OK**.
* `%APPDATA%` equals:
  `C:\Users\<Username>\AppData\Roaming\`
* ⚠️ The `AppData` folder is hidden.
  In File Explorer, go to the **View** tab and enable **Hidden items** to see it.

##### 🍎 macOS

* Press ⇧ **Shift** + ⌘ **Command** + **G** in Finder, or open Spotlight from the menu bar.
* Enter:
  `~/Library/Application Support/minecraft`
* `~/Library/` equals:
  `/Users/<Username>/Library/`
* ⚠️ The `Library` folder is hidden.
  Use the **Go to Folder** shortcut or press **Command + Shift + .** to show hidden files.
* The `~` symbol refers to your **home directory** (e.g., `/Users/you/`).

##### 🐧 Linux

* The `~` symbol refers to your **home directory** (e.g., `/home/you/`).
* Folders starting with a dot (`.`), like `.minecraft`, are **hidden by default**.
* Most file managers toggle hidden files with **Ctrl + H**.

---

## 🐍 How to Find Your Python Installation Path

### ◾ Windows

1. Open Command Prompt (`Win + R` → type `cmd` → Enter)
2. Run: `where python`
3. Example path: `C:\Users\yourname\AppData\Local\Programs\Python\Python311\python.exe`

### ◾ macOS

1. Open Spotlight (`Cmd + Space`) → type `Terminal`
2. Run: `which python3`
3. Example output: `/usr/bin/python3`

*💬 Note: `which python` may show Python 2.*

