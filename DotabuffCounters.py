from requests import get
from bs4 import BeautifulSoup


def get_heroes_list():
    url2 = 'https://dota2.gamepedia.com/Heroes'
    response = get(url2)

    soup = BeautifulSoup(response.text, 'html.parser')
    dota_heroes = soup.find_all('a', href=True, title=True)
    dota_heroes_list = [a['title'] for a in dota_heroes]
    dota_heroes_list = dota_heroes_list[
                       dota_heroes_list.index('Strength') + 1:dota_heroes_list.index('Unreleased Content')]
    dota_heroes_list.remove('Strength')
    dota_heroes_list.remove('Intelligence')
    dota_heroes_list.remove('Intelligence')
    dota_heroes_list.remove('Agility')
    dota_heroes_list.remove('Agility')
    dota_heroes_list = [a.lower() for a in dota_heroes_list]
    return [a.replace(' ','-') for a in dota_heroes_list]


def heroes_nickname_dict():
    hero_dict = {'abby':'abbadon', 'alch':'alchemist', 'Brew':'brewmaster', 'bristle':'bristleback', 'centaur':'centaur-Warrunner',
             'Chaos':'Chaos-Knight', 'Clock':'Clockwerk', 'Clockwork': 'Clockwerk', 'dk': 'Dragon Knight', 'DK':'Dragon-Knight',
             'Shaker':'Earthshaker', 'Earth Shaker':'EarthShaker', 'ET':'Elder-Titan',
             'Wisp':'Io', 'LC':'Legion-Commander', 'LS':'Lifestealer', 'Life Stealer':'Lifestealer', 'Omni':'Omniknight',
             'SK':'Sand-King', 'Tide':'Tidehunter', 'Timber':'Timbersaw', 'Treant':'Treant-Protector', 'Pitlord':'Underlord',
             'AM':'Anti-Mage', 'Anti Mage':'Anti-Mage', 'Antimage':'Anti-Mage', 'Arc':'Arc-Warden', 'BS':'Bloodseeker',
             'Bounty':'Bounty-Hunter', 'Brood':'Broodmother', 'Brood Mother':'Broodmother', 'Drow':'Drow-Ranger',
             'Ember':'Ember-Spirit', 'Void':'Faceless-Void', 'Faceless':'Faceless-void', 'Gyro':'Gyrocopter',
             'LD':'Lone-Druid', 'Dusa':'Medusa', 'PoTM':'Mirana', 'POTM':'Mirana', 'Wukong':'Monkey-King', 'Monkey':'Monkey-King',
             'Morph':'Morphling', 'Naga':'Naga-Siren', 'Nyx':'Nyx-Assassin', 'Pango':'Pangolier', 'PA':'Phantom-Assassin',
             'PL':'Phantom-Lancer', 'SF':'Shadow-Fiend', 'TA':'Templar-Assassin', 'Lanaya':'Templar-Assassin', 'TB':'Terrorblade',
             'Troll':'Troll-Warlord', 'Venge':'Vengeful-spirit', 'Veno':'Venomancer', 'AA':'Ancient-Apparition', 'Bat':'Batrider',
             'Bat Rider':'Batrider', 'CM':'Crystal-Maiden', 'Willow':'Dark-Willow', 'DP':'Death-Prophet', 'Ench':'Enchantress',
             'KOTL':'Keeper-of-the-Light', 'Kotl':'Keeper-of-the-Light', 'KoTL':'Keeper-of-the-Light', 'Lesh':'Leshrac',
             'NP':'Natures-Prophet', 'Nature\'s Prophet':'Natures-prophet','Necro':'Necrophos', 'Ogre':'Ogre-Magi', 'OD':'Outworld-Devourer', 'QOP':'Queen-of-Pain',
             'Qop':'Queen-of-Pain', 'QoP':'Queen-of-Pain', 'Skywrath':'Skywrath-Mage', 'Storm':'Storm-Spirit', 'wyvern':'winter-wyvern',
             'WD':'Witch-Doctor'}

    hero_dict = {k.lower(): v.lower() for k, v in hero_dict.items()}
    return hero_dict


def is_hero_name(hero_name):
    url = 'https://www.dotabuff.com/heroes/{}/counters'.format(hero_name)
    response = get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    dota_counters = soup.find_all('td')
    a = [b.attrs.get('data-value', None) for b in dota_counters]
    a = list(filter(None, a))
    a = list(dict.fromkeys(a))[::3]
    a = a[:5]
    return ', '.join(b for b in a)


def is_nickname(hero_name, dota_heroes_list, hero_nickname):
    url = 'https://www.dotabuff.com/heroes/{}/counters'.format(hero_nickname[hero_name])
    response = get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, 'html.parser')
    dota_counters = soup.find_all('td')
    a = [b.attrs.get("data-value", None) for b in dota_counters]
    dota_heroes_list = [s.title() for s in dota_heroes_list]
    a = [b for b in a if b in dota_heroes_list]
    a = a[:10]
    a = list(dict.fromkeys(a))
    return ', '.join(b for b in a)


def get_counter(hero_name, dota_heroes_list, hero_nickname):
    if hero_name in hero_nickname.keys():
        return is_nickname(hero_name, dota_heroes_list, hero_nickname)
    elif hero_name in dota_heroes_list:
        return is_hero_name(hero_name)
    else:
        return 'Please enter the correct hero name or nickname.'


def get_hero_name(msg, nickname_dict, heroes_list):
    a = '-'.join(b.lower() for b in msg)
    if a in nickname_dict:
        return nickname_dict[a]
    if a in heroes_list:
        return a
    else:
        return "Please enter the correct hero name or nickname."


# dota_heroes_list = get_heroes_list()
# hero_nickname = heroes_nickname_dict()
# hero_name = str(input('Please enter a DotA 2 hero name ')).lower()
# hero_name = hero_name.split()
# hero_name = "-".join(b for b in hero_name)
#
# if hero_name in hero_nickname.keys():
#     print(is_nickname(hero_name, dota_heroes_list, hero_nickname))
# elif hero_name in dota_heroes_list:
#     print(is_hero_name(hero_name))
# else:
#     print('Please enter the correct hero name or nickname')