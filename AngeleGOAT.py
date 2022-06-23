import random, re, time, tweepy, os, instaloader, glob, os.path, imghdr, shutil, emoji, unidecode
from datetime import datetime
from itertools import dropwhile, takewhile
from emoji import UNICODE_EMOJI
from urlextract import URLExtract

########################################################################################################################################################################################################################################################################

consumer_key = "IY6GHRIx5BUagVtEP2P5hxAfb"
consumer_secret = "u8a16mqEqXmwjRXvff49zCpF3oiJIexkOScu2evmhRFLQRftzt"

key = "1324444975342505986-NvzkfiEC0G6FUuG5wDhpbKiBSO0FrD"
secret = "I4HHSueZm8uNst2ePPG5W8phxe6tVYeC91SMmNmoN3Q5e"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(key, secret)
api = tweepy.API(auth, retry_count=10, retry_delay=5, retry_errors=set([503]))

########################################################################################################################################################################################################################################################################

fichier_1 = "dernier_id_mentions.txt"
fichier_2 = "dernier_id_recherche.txt"
fichier_3 = "dernier_id_goat.txt"
fichier_4 = "dernier_insta.txt"
fichier_5 = "dernier_story.txt"

########################################################################################################################################################################################################################################################################

def lire_dernier_id_vu(fichier):
    lire_fichier = open(fichier, 'r')
    dernier_id_vu = int(lire_fichier.read().strip())
    lire_fichier.close()
    return dernier_id_vu

def stocker_dernier_id_vu(fichier, tweet_id):
    ecrire_fichier = open(fichier, 'w')
    ecrire_fichier.write(str(tweet_id))
    ecrire_fichier.close()
    return

def lire_dernier_insta_vu(fichier):
    lire_fichier = open(fichier, 'r')
    dernier_id_vu = str(lire_fichier.read().strip())
    lire_fichier.close()
    return dernier_id_vu

def stocker_dernier_insta_vu(fichier, post_date):
    ecrire_fichier = open(fichier, 'w')
    ecrire_fichier.write(str(post_date))
    ecrire_fichier.close()
    return

def lire_texte(fichier):
    lire_fichier = open(fichier, 'r', encoding='utf-8')
    texte = str(lire_fichier.read().strip())
    lire_fichier.close()
    return texte

def formatage(string):
    raw = unidecode.unidecode(string.lower())
    return raw

def analyse_texte(tweet_id, string):
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    if re.search(r'\b' + string + r'\b', formatage(tweet.full_text)):
        return True

def compteur(tweet_id, string):
    tweet = api.get_status(tweet_id, tweet_mode='extended')
    compteur = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(string), formatage(tweet.full_text)))
    return compteur

def extract_emojis(s):
  return ''.join(c for c in s if c in emoji.UNICODE_EMOJI['en'])

########################################################################################################################################################################################################################################################################

def tweet_mention(tweet_id):
    print("mention" + " - " + str(tweet_id))
    temp = random.randint(0,1)
    if temp == 0:
        api.update_status(status=reponses_mentions[random.randint(0,3)], in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
        time.sleep(5)
    else:
        upload_result = api.chunked_upload("reponses_mentions_video/" + str(random.randint(0,1)) + ".mp4", media_category="amplify_video")
        api.update_status(status="", media_ids=[upload_result.media_id_string], in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True)
        time.sleep(5)

def mentions():
    tweets = tweepy.Cursor(api.search_tweets, q="(@Angele_GOAT) OR (to:@Angele_GOAT) -filter:retweets", since_id=lire_dernier_id_vu(fichier_1), tweet_mode='extended').items()
    for tweet in tweets:
        try:
            if tweet.in_reply_to_status_id == None:
                tweet_mention(tweet.id)
            elif compteur(tweet.id, "angele_goat") >= 2 or (compteur(tweet.in_reply_to_status_id, "angele_goat") == 0 and analyse_texte(tweet.id, "angele_goat")): #fonctionne pas pour personne qui se rep' et qui a déjà @
                tweet_mention(tweet.id)
            else:
                print(".")
            if tweet.id > lire_dernier_id_vu(fichier_1):
                stocker_dernier_id_vu(fichier_1, tweet.id)
        except tweepy.errors.TweepyException as e:
            print (e)
            pass

########################################################################################################################################################################################################################################################################

def goat():
    try:
        tweets = tweepy.Cursor(api.search_tweets, q="from:@angele_vl -filter:retweets", since_id=lire_dernier_id_vu(fichier_3), tweet_mode='extended').items()
    except:
        return
    
    liste_rt = []
    for tweet in tweets:
        liste_rt.append(tweet)
            
    liste_rt.reverse()

    for tweet in liste_rt:
        try:
            api.retweet(tweet.id)
            print("Retweet")
            time.sleep(5)
            if tweet.id > lire_dernier_id_vu(fichier_3):
                stocker_dernier_id_vu(fichier_3, tweet.id)
        except tweepy.errors.TweepyException as e:
            print (e)
            pass

########################################################################################################################################################################################################################################################################

def insta():

    #USERNAME = "HuproZ"
    #PASSWORD = "Cdjpmy1234567%"

    try:
        #L = instaloader.Instaloader()
        #L.load_session_from_file("HuproZ")
        #L.login(USERNAME,PASSWORD)
        posts = instaloader.Profile.from_username(L.context, "angele_vl").get_posts()
    except:
        return

    SINCE = datetime.strptime(lire_dernier_insta_vu(fichier_4), '%Y-%m-%d %H:%M:%S')
    UNTIL = datetime.strptime(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')

    post_list = []

    for post in takewhile(lambda p: p.date > SINCE, dropwhile(lambda p: p.date > UNTIL, posts)):
        post_list.append(post)
        if post.date > datetime.strptime(lire_dernier_insta_vu(fichier_4), '%Y-%m-%d %H:%M:%S'):
                stocker_dernier_insta_vu(fichier_4, post.date)

    post_list.reverse()

    for post in post_list:
        try:
            L.download_post(post, "temp")

            nbPhotos = len(glob.glob1("temp","*.jpg"))

            date = str(post.date)
            date = date.replace(" ","_")
            date = date.replace(":","-")
            date = date + "_UTC"

            if os.path.exists("temp/" + date + ".jpg"):
                os.rename("temp/" + date + ".jpg", "temp/" + date + "_0.jpg")
            if os.path.exists("temp/" + date + ".mp4"):
                os.rename("temp/" + date + ".mp4", "temp/" + date + "_0.mp4")
            
            temp = 0

            while temp <= nbPhotos:
                if os.path.exists("temp/" + date + "_" + str(temp) + ".jpg") and os.path.exists("temp/" + date + "_" + str(temp) + ".mp4"):
                    os.remove("temp/" + date + "_" + str(temp) + ".jpg")
                temp = temp + 1

            liste_media = []
            liste_temp = []
            temp = 0

            while temp <= nbPhotos:
                if os.path.exists("temp/" + date + "_" + str(temp) + ".jpg"):
                    liste_temp.append("temp/" + date + "_" + str(temp) + ".jpg")
                    while os.path.exists("temp/" + date + "_" + str(temp + 1) + ".jpg") and len(liste_temp) < 4:
                        liste_temp.append("temp/" + date + "_" + str(temp + 1) + ".jpg")
                        temp = temp + 1
                    if len(liste_temp) == 1:
                        liste_media.append(liste_temp[0])
                    else:
                        liste_media.append(liste_temp)
                    liste_temp = []
                elif os.path.exists("temp/" + date + "_" + str(temp) + ".mp4"):
                    liste_media.append("temp/" + date + "_" + str(temp) + ".mp4")
                temp = temp + 1

            liste_texte = [".@angele_vl sur Instagram :","","","","","","","","","","","","","","","","","","",""]

            if os.path.exists("temp/" + date + ".txt"):
                liste_texte[0] = liste_texte[0] + "\n" + "\n" + "\""

                texte = lire_texte("temp/" + date + ".txt").strip()
                longueur = len(texte) + len(extract_emojis(texte))
                extractor = URLExtract()
                urls = extractor.find_urls(texte)
                if len(urls) > 0:
                    for champs in urls:
                        longueur = longueur + 8

                if longueur <= 249 and len(liste_media) == 1:
                    liste_texte[0] = liste_texte[0] + texte + "\""
                elif longueur <= 244 and len(liste_media) > 1:
                    liste_texte[0] = liste_texte[0] + texte + "\""
                elif longueur > 249 or len(liste_media) > 1:
                    liste_mots = texte.split()

                    index = 0
                    for mot in liste_mots:
                        longueur = len(liste_texte[index] + mot + " ") + len(extract_emojis(liste_texte[index] + mot + " "))
                        extractor = URLExtract()
                        urls = extractor.find_urls(liste_texte[index] + mot + " ")
                        if len(urls) > 0:
                            for champs in urls:
                                longueur = longueur + 8
                        if longueur <= 272:
                            liste_texte[index] = liste_texte[index] + mot + " "
                        else:
                            liste_texte[index + 1] = liste_texte[index + 1] + mot + " "
                            index = index + 1

            compteur = 0
            for champs in liste_texte:
                if champs != "":
                    compteur = compteur + 1

            if compteur > 1:
                temp = 0
                while temp < compteur - 1:
                    liste_texte[temp] = liste_texte[temp] + "..."
                    temp = temp + 1
                liste_texte[compteur - 1] = liste_texte[compteur - 1][:-1]
                liste_texte[compteur - 1] = liste_texte[compteur - 1] + "\""

            nbT = max(compteur, len(liste_media))
            print(nbT)
            temp = 1

            if nbT > 1:
                while temp <= nbT:
                    if liste_texte[temp - 1] == "":
                        liste_texte[temp - 1] = liste_texte[temp - 1] + str(temp) + "/" + str(nbT)
                    else:
                        liste_texte[temp - 1] = liste_texte[temp - 1] + "\n" + "\n" + str(temp) + "/" + str(nbT)
                    temp = temp + 1

            print(liste_texte)

            temp = 0

            while temp < nbT:
                if temp == 0:
                    if len(liste_media[temp]) > 1 and len(liste_media[temp]) <= 4:
                        images = liste_media[temp]
                        media_ids = [api.media_upload(i).media_id_string for i in images]
                        api.update_status(status=liste_texte[temp], media_ids=media_ids, auto_populate_reply_metadata=True)
                        time.sleep(5)
                    else:
                        if imghdr.what(liste_media[temp]) == "jpeg":
                            api.update_status_with_media(status=liste_texte[temp],filename=liste_media[temp], auto_populate_reply_metadata=True)
                            time.sleep(5)
                        else:
                            upload_result = api.chunked_upload(filename=liste_media[temp], media_category="amplify_video")
                            api.update_status(status=liste_texte[temp], media_ids=[upload_result.media_id_string], auto_populate_reply_metadata=True)
                            time.sleep(5)
                else:
                    tweets = api.user_timeline(screen_name="Angele_GOAT", count = 1)
                    for tweet in tweets:
                        tweet_id_temp = tweet.id
                    if len(liste_media) < nbT:
                        api.update_status(status=liste_texte[temp], in_reply_to_status_id=tweet_id_temp, auto_populate_reply_metadata=True)
                        time.sleep(5)
                    else:
                        if len(liste_media[temp]) > 1 and len(liste_media[temp]) <= 4:
                            images = liste_media[temp]
                            media_ids = [api.media_upload(i).media_id_string for i in images]
                            api.update_status(status=liste_texte[temp], media_ids=media_ids, in_reply_to_status_id=tweet_id_temp, auto_populate_reply_metadata=True)
                            time.sleep(5)
                        else:
                            if imghdr.what(liste_media[temp]) == "jpeg":
                                api.update_status_with_media(status=liste_texte[temp],filename=liste_media[temp], in_reply_to_status_id=tweet_id_temp, auto_populate_reply_metadata=True)
                                time.sleep(5)
                            else:
                                upload_result = api.chunked_upload(filename=liste_media[temp], media_category="amplify_video")
                                api.update_status(status=liste_texte[temp], media_ids=[upload_result.media_id_string], in_reply_to_status_id=tweet_id_temp, auto_populate_reply_metadata=True)
                                time.sleep(5)
                temp = temp + 1
            shutil.rmtree("temp", ignore_errors=True)
        except:
            pass

########################################################################################################################################################################################################################################################################

def stories():

    try:
        #L = instaloader.Instaloader()
        #L.load_session_from_file("HuproZ")
        st = L.get_stories(userids=[1540792116])
    except:
        return

    SINCE = datetime.strptime(lire_dernier_insta_vu(fichier_5), '%Y-%m-%d %H:%M:%S')
    liste_story = []

    for story in st:
        for item in story.get_items():
            if item.date > SINCE:
                liste_story.append(item)

    for item in liste_story:  
        if item.date > datetime.strptime(lire_dernier_insta_vu(fichier_5), '%Y-%m-%d %H:%M:%S'):
            stocker_dernier_insta_vu(fichier_5, item.date)

    liste_story.reverse()
    
    for item in liste_story:
        try:
            L.download_storyitem(item, "temp")

            date = str(item.date)
            date = date.replace(" ","_")
            date = date.replace(":","-")
            date = date + "_UTC"
            
            if os.path.exists("temp/" + date + ".jpg") and os.path.exists("temp/" + date + ".mp4"):
                upload_result = api.chunked_upload(filename="temp/" + date + ".mp4", media_category="amplify_video")
                api.update_status(status="Nouvelle story IG d'@angele_vl " + u"\U0001F633", media_ids=[upload_result.media_id_string])
                time.sleep(5)
            elif os.path.exists("temp/" + date + ".jpg") and (os.path.exists("temp/" + date + ".mp4") == False):
                api.update_status_with_media(status="Nouvelle story IG d'@angele_vl " + u"\U0001F633", filename="temp/" + date + ".jpg")
        except:
            pass
    shutil.rmtree("temp", ignore_errors=True)

########################################################################################################################################################################################################################################################################
               
while True:
    #print("MENTIONS()")
    #mentions()
    print("goat()")
    goat()

    USERNAME = "HuproZ"
    PASSWORD = "Cdjpmy1234567%"

    try:
        L = instaloader.Instaloader()
        #L.load_session_from_file("HuproZ")
        L.login(USERNAME,PASSWORD)
    except:
        pass

    print("INSTA()")
    insta()
    print("STORIES()")
    stories()
    print("...")
    time.sleep(960)