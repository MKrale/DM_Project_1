"""
    Creates a valid Dictionary for Ironclad cards, which can be used by other scripts
"""
import numpy as np

#Lists of cards in array:
ironcladCardNames = ["Bash","Defend","Strike","Anger","Armaments","Body Slam","Clash","Cleave","Clothesline","Flex","Havoc","Headbutt","Heavy Blade","Iron Wave","Perfected Strike","Pommel Strike","Shrug It Off","Sword Boomerang","Thunderclap","True Grit","Twin Strike","Warcry","Wild Strike","Battle Trance","Blood for Blood","Bloodletting","Burning Pact","Carnage","Combust","Dark Embrace","Disarm","Dropkick","Dual Wield","Entrench","Evolve","Feel No Pain","Fire Breathing","Flame Barrier","Ghostly Armor","Hemokinesis","Infernal Blade","Inflame","Intimidate","Metallicize","Power Through","Pummel","Rage","Rampage","Reckless Charge","Rupture","Searing Blow","Second Wind","Seeing Red","Sentinel","Sever Soul","Shockwave","Spot Weakness","Uppercut","Whirlwind","Barricade","Berserk","Bludgeon","Brutality","Corruption","Demon Form","Double Tap","Exhume","Feed","Fiend Fire","Immolate","Impervious","Juggernaut","Limit Break","Offering","Reaper"]

silentCardNames = ["Defend","Neutralize","Strike","Survivor","Acrobatics","Backflip","Bane","Blade Dance","Cloak and Dagger","Dagger Spray","Dagger Throw","Deadly Poison","Deflect","Dodge and Roll","Flying Knee","Outmaneuver","Piercing Wail","Poisoned Stab","Prepared","Quick Slash","Slice","Sneaky Strike","Sucker Punch","Accuracy","All-Out Attack","Backstab","Blur","Bouncing Flask","Calculated Gamble","Caltrops","Catalyst","Choke","Concentrate","Crippling Cloud","Dash","Distraction","Endless Agony","Escape Plan","Eviscerate","Expertise","Finisher","Flechettes","Footwork","Heel Hook","Infinite Blades","Leg Sweep","Masterful Stab","Noxious Fumes","Predator","Reflex","Riddle with Holes","Setup","Skewer","Tactician","Terror","Well-Laid Plans","A Thousand Cuts","Adrenaline","After Image","Alchemize","Bullet Time","Burst","Corpse Explosion","Die Die Die","Doppelganger","Envenom","Glass Knife","Grand Finale","Malaise","Nightmare","Phantasmal Killer","Storm of Steel","Tools of the Trade","Unload","Wraith Form"]

colorlessCardNames = ["Bandage Up","Blind","Dark Shackles","Deep Breath","Discovery","Dramatic Entrance","Enlightenment","Finesse","Flash of Steel","Forethought","Good Instincts","Impatience","Jack of All Trades","Madness","Mind Blast","Panacea","Panic Button","Purity","Swift Strike","Trip","Apotheosis","Chrysalis","Hand of Greed","Magnetism","Master of Strategy","Mayhem","Metamorphosis","Panache","Sadistic Nature","Secret Technique","Secret Weapon","The Bomb","Thinking Ahead","Transmutation","Violence","Apparition","Become Almighty","Beta","Bite","Expunger","Fame and Fortune","Insight","J.A.X.","Live Forever","Miracle","Omega","Ritual Dagger","Safety","Shiv","Smite","Through Violence"]

curseCardNames = ["Clumsy","Decay","Doubt","Injury","Normality","Pain","Parasite","Regret","Shame","Writhe","Ascender's Bane","Curse of the Bell","Necronomicurse","Pride"]

def classCardDict(thisClass):
    if (thisClass == 'Ironclad'):
        validCardNames = ironcladCardNames + colorlessCardNames + curseCardNames
    elif (thisClass == 'Silent'):
        validCardNames = silentCardNames + colorlessCardNames + curseCardNames
    nmbrCards = len(validCardNames)
    
    #convert valid card names to dictionary:
    cardDict = {}
    for i in range(nmbrCards):
        cardDict[validCardNames[i]] = i
        
    #Manual additions to prevent common errors:
    cardDict["AscendersBane"] = cardDict["Ascender's Bane"]
    cardDict["Strike_R"] = cardDict["Strike"]
    cardDict["Defend_R"] = cardDict["Defend"]
    cardDict["Strike_G"] = cardDict["Strike"]
    cardDict["Defend_G"] = cardDict["Defend"]
    cardDict["Jack Of All Trades"] = cardDict["Jack of All Trades"]
    cardDict["RitualDagger"] = cardDict["Ritual Dagger"]
    cardDict["PanicButton"] = cardDict["Panic Button"]
    cardDict["HandOfGreed"] = cardDict["Hand of Greed"]
    cardDict["CurseOfTheBell"] = cardDict["Curse of the Bell"]
    if (thisClass=='Ironclad'):
        cardDict["Ghostly"] = cardDict["Ghostly Armor"]
    if (thisClass=='Silent'):
        cardDict["Cloak And Dagger"] = cardDict["Cloak and Dagger"]
        cardDict["Well Laid Plans"] = cardDict["Well-Laid Plans"]
        cardDict["Crippling Poison"] = cardDict["Crippling Cloud"]
        cardDict["PiercingWail"] = cardDict["Piercing Wail"]
        cardDict["Underhanded Strike"] = cardDict["Sneaky Strike"]
        cardDict["Wraith Form v2"] = cardDict["Wraith Form"]
        cardDict["Venomology"] = cardDict["Noxious Fumes"]      #not exactly the same, but very close
        cardDict["All Out Attack"] = cardDict["All-Out Attack"]
        cardDict["Riddle With Holes"] = cardDict["Riddle with Holes"]
    
    return cardDict

def toName(i, thisClass):
    if (thisClass == 'Ironclad'):
        classCards = ironcladCardNames
    elif (thisClass == 'Silent'):
        classCards = silentCardNames
    
    if (i<len(classCards)):
        return classCards[i]
    i -= len(ironcladCardNames)
    if (i< len(colorlessCardNames)):
        return colorlessCardNames[i]
    i-= len(colorlessCardNames)
    if (i< len(curseCardNames)):
        return curseCardNames[i]
    return "ERROR In ToName: this card number does not exist (nmbr="+str(i)+")"
    
    
#prints a deck as names
def deckToNames(deck, thisClass):
    names = []
    amount = []
    for i in range(len(deck)):
        if (deck[i] != 0):
            names = np.append(names, toName(i, thisClass))
            amount = np.append(amount, deck[i])
    for i in range(len(names)):
        print(str(names[i])+": "+str(int(amount[i])))



