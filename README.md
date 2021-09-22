## Updated Easy-Apply Linkedin Bot

#### Theoretically if you were to use this on an Linkedin account then here are the theoretical procedures and warnings
# WARNING :warning:

#### If you use this script on https://Linkedin.com/in/ you are at risk of violating the Linkedin's TOS agreement. 

#### You are not allowed to access the Linkedin services using automation, anything done with this script 

#### will be your responsibility. 

### Getting Started 

Make sure you have python 3.7 installed onto your system using your favorite IDE.

After you have python and an ide installed, once you clone the repo, then you should have notifications on libraries that need to 
be installed.   Install the libraries and make sure all dependencies have been resolved.  I would say there are about 3 dependencies
that most developers don't have and 5 neede overall.

### Modifications

On line 88 you can insert this line ONLY if you are experiencing issues sustaining the automation loop:

```pyautogui.FAILSAFE = False```

Also you can change the amount of sleep time under the method ```wait_for_login()```

change ```time.sleep(30)``` to ```time.sleep(120)``` if you are being prompted for a CAPTCHa, there is no automation for this.

Once the system is running you will not be prompted for a CAPTCHa and I have the automation run through thousands of job listing without
it going offline.

If there are any issues then please raise an issue request.  I will be working on an additional script that will harvest the 
questions of Easy-Apply applications that "pop-out" into a new tab.  I believe this was an effort to stop automation, but it seems
like a paid feature that not everyoen cares about.

No go apply you some jobs for great good!


### Search Term Tips
 
I would go with broad terms such as ```devops```, ```software engineer```, or even keyword tech like ```Java```, ```C#```, ```Python```,
```AWS```, etc.

#### Warning for Junior Developers
tempting to search for ```Junior developer``` and ```Junior``` on it's own.  I would just apply generally mainly because
there are senior listings under junior search results, also it GREATLY reduces your job listings.  Pretty much excludes 70-80% of the
results for the normal search terms.

## WARNING OVERALL
You are about to be putting your resume out to a lot of people and as we all know, there are scammers and recruiters overseas selling your information.  Phone Number, Email, and Github are safe but DO NOT post birthdate, personal address, or any super-specific detail like "I work at this company in North LA".  Everyone looking at this repo should know these things but there are always a couple of people needing this piece of advice.

# Stay Safe And Always Proof Read Scripts Before Running Them!
