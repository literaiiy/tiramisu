![Tiramisu logo](https://raw.githubusercontent.com/gist/literaiiy/a5151734080232985c55f7753dcc417d/raw/fa23a4507d1e34da1579afd26719cc47297153da/tiramisuFullText.svg)
# 🍰 tiramisu: Minecraft Name History & Hypixel Stats Analysis ☕
tiramisu is a Hypixel player statistics site that gives a comprehensive outlook on your Minecraft account and Hypixel profile- complete name history, detailed breakdowns of your Hypixel statistics (including an elaborate analysis of your SkyWars and BedWars stats), among other things. It is currently in an open beta, and there are bound to be a lot of bugs, but I am actively working on resolving these bugs and improving the experience tiramisu provides.

This is a private repository containing the source code for the project solely for backup purposes. This code may be released for the open-source community once the project hits a certain milestone in popularity. But probably not, we don't need no bum ass clones. If you're reading this, it means that I fucked up and didn't update the readme.

If you are here and not me, how? How is that even possible?

My main landing page is at literaiiy.me, where you can read more about me!


# FAQ

**How is your site different from NameMC, Plancke's site, or Sk1er's site?**
- Uh... next question. 

**What is a UUID?**
- A **UUID**, or **U**niversally **U**nique **ID**entifier, is a unique hexadecimal value that is tied directly to a Minecraft account. Your UUID is always attached to your account from the date of your account's registration, making it much more reliable to tie stats to.

**Will you ever put ads?**
- No. tiramisu is ad-free and plans to never change that. I am fully supported by donations, which go directly to me and are recycled back into working on tiramisu. Although donations are very nice and are a great way to show support, please don't be pressured to leave one if you don't want to. The site is free to use for all. :slightly_smiling_face:

**Are you stealing my data?**
- Also- no. This is covered in the [Privacy Policy](404.html). I don't take any personally identifiable information, or share anything with third parties.

**Why don't you have (this feature)?**
- tiramisu is a relatively new project. I am actively working on it as a project alongside school and other things, but most major features will be added as soon as possible.

**Why did you name your site tiramisu?**
- It's an Italian dessert that's quite lovely.

**Do you work alone?**
- Yes. I develop tiramisu independently.

**Is tiramisu open-source?**
- Not at the moment.

**Why is there a '>' symbol in front of my first name's duration had?**
- Mojang doesn't provide an account's creation date in the API, so if an account's Hypixel join date was before their first name change, that would be used as a substitute for a pseudo account creation date. This means that number is almost certainly not an accurate figure.

**What is the "Hypixel ____" on my profile?**
- This Hypixel seniority index is entirely based on how long you have been playing on the server- or more accurately, the amount of time since your first login. There are nine ranks, of which are based on the formula `y=9(log(x+1)`, where `x` is the amount, in years, required to achieve the `y`th rank.

**Why don't the player counts instantly update every time I refresh?**
- Player counts only update once every 3 seconds to avoid spam and running over the Hypixel API's rate limit of 120 requests per minute.

**Why can't I search for a name I've previously had?**
- At some point in November of 2020, Mojang stopped support for querying a UUID to receive a username at a certain timestamp, making it impossible to find a player's current name from a previous one. Sorry about that. Source: [Mojang API Documentation](https://wiki.vg/Mojang_API). See [this ticket](https://bugs.mojang.com/browse/WEB-3367) for more information on the topic.

*Last updated on March 29th, 2021*
