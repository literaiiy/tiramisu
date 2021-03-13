# 🍰 tiramisu: Name History and Hypixel Stats Analysis ☕
tiramisu is a player statistics site that gives a comprehensive outlook on your Minecraft & Hypixel profiles- complete name history, detailed breakdowns of your Hypixel statistics (including an elaborate analysis of your SkyWars and BedWars stats), among other things. It is currently in an open Beta, and there are bound to be a lot of bugs, but I am actively working on resolving these bugs and improving the experience tiramisu provides.

This is a private repository containing the source code for the project solely for backup purposes. This code may be released for the open-source community once the project hits a certain milestone in popularity. But probably not, we don't need no bum ass clones. If you're reading this, it means that I fucked up and didn't update the readme.

If you are here and not me, how? How is that even possible?

# About literaiiy
Hello! I am literaiiy (styled lowercase), a high-school student in the San Francisco Bay Area. I am fascinated with technology, especially smartphones and other mobile devices, older personal and datacenter computer components, as well as circuit board electronics. I have years of experience in the Microsoft Office and Adobe Creative Cloud suites.

literaiiy is a pseudonym I adopted in March of 2018, as an intentionally incorrectly spelt version of the word literally- although a word that has a simple definition, is also a word that most people cannot use correctly- a common word that has dulled due to overuse. 

Computers, statistics, and working with financial assets and spreadsheets are my passion, and I’m in love with a lot to do with them! You’ll see most of my posts relating to them, but occasionally another post will sneak past. Special thanks to Liechtenstein for letting me borrow their country code TLD.

My main landing page is at literaiiy.me, where you can read more about me!


# FAQ

**How is your site different from NameMC, Plancke's site, or Sk1er's site?**
- Uh... next question. 

**What is a UUID?**
- A **UUID**, or **U**niversally **U**nique **ID**entifier, is a unique hexadecimal value that is tied directly to a Minecraft account. Your UUID is always attached to your account from the date of your account's registration, making it much more reliable to tie stats to.

**Will you ever put ads?**
- No. tiramisu is ad-free and plans to never change that. I am fully supported by donations, which go directly to me and are recycled back into working on Tiramisu. Although donations are very nice and are a great way to show support, please don't be pressured to leave one if you don't want to. The site is free to use for all. :slightly_smiling_face:

**Are you stealing my data?**
- Also- no. This is covered in the (Privacy Policy)[404.html]. I don't take any personally identifiable information, or share anything with third parties.

**Why don't you have (this feature)?**
- tiramisu is a relatively new project. I am actively working on it as a project alongside school and other things, but most major features will be added as soon as possible.

**Why did you name your site tiramisu?**
- It's an Italian dessert that's quite lovely.

**Do you work alone?**
- Yes. I develop Tiramisu independently.

**Is tiramisu open-source?**
- Not at the moment, and most likely won't be.

**Why is there a '>' symbol in front of my first name's duration?**
- Mojang doesn't provide an account's creation date in the API, so if an account's Hypixel join date was before their first name change, that would be used as a substitute for a pseudo account creation date. This means that number is almost certainly not an accurate figure.

**What is the "Hypixel ____" on my profile?**
- This Hypixel seniority index is entirely based on how long you have been playing on the server- or more accurately, the amount of time since your first login. There are nine ranks, of which are based on the formula `y=12(log(x+1)`, where `x` is the amount, in years, required to achieve the `y`th rank.

**Why don't the player counts instantly update every time I refresh?**
- Player counts only update once every 15 seconds to avoid spam and running over the Hypixel API's rate limit of 120 requests per minute.

**Why can't I search for a previous name I had?**
- At some point in November of 2020, Mojang stopped support for querying a UUID to receive a username at a certain timestamp, making it impossible to find a player's current name from a previous one. Sorry about that. Source: [Mojang API Documentation](https://wiki.vg/Mojang_API). See [this ticket](https://bugs.mojang.com/browse/WEB-3367) for more information on the topic.

*Last updated on March 13th, 2021*
