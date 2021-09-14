import pymysql
import random
from TextLib import add_dicts,get_csv_dict, rank_dict

class Users(object):
    """docstring forUsers."""

    def __init__(self):
        self.preferences = dict()
        self.av_length = 0
        self.fav_types = {'ShortStory':0,'Poem':0,'Book':0}
        #choose a random name
        names = open('names.txt','r+')
        rand_int = random.choice(range(1000))
        counter = 0
        for line in names:
            if (counter == rand_int):
                self.name = line
                names.close()
                break
            counter += 1

    def get_fav_types(self):
        return self.fav_types

    def set_fav_types(self,favorite_types):
        self.fav_types = favorite_types

    def get_av_length(self):
        return self.av_length

    def set_av_length(self,new_length):
        self.av_length = new_length

    def get_preferences(self):
        return self.preferences

    def set_preferences(self,pref):
        self.preferences = pref

    def traverse_site(self):
        conn = pymysql.connect(host='127.0.0.1', user='root', passwd='Konoha.12')
        cur = conn.cursor()
        cur.execute('USE americanliterature')
        visited_ids = list()
        #STARTING PLACE!!
        page = random.choice(['https://americanliterature.com/home','https://americanliterature.com/100-great-short-stories'
        ,'https://americanliterature.com/100-great-poems','https://americanliterature.com/twenty-five-great-american-novels'])

        #travels through the page
        number = 10
        n_words = 0
        # n_words_PM = 0
        # n_words_BK = 0
        preference = dict()

        while number > 0:
            cur.execute('SELECT id FROM Content')
            id = random.choice(cur.fetchall())
            #check if it has text
            cur.execute('SELECT preferences,length,type FROM Content WHERE id = %s',(id,))
            data = cur.fetchone()
            pref,length,type = data[0],data[1],data[2]

            if (pref == None):
                continue
            # if (type == 'ShortStory'):
            #     n_words_SS += length
            # if (type == 'Poem'):
            #     n_words_PM += length
            # if (type == 'Book'):
            #     n_words_BK += length
            n_words += length
            favorite_types = self.get_fav_types()
            favorite_types[type] = favorite_types[type] + length
            self.set_fav_types(favorite_types)
            #preferences
            new_pref = add_dicts(self.get_preferences(),get_csv_dict(pref))
            self.set_preferences(new_pref)
            number -=1
            print(self.get_fav_types())

        self.set_av_length(n_words/100)
        print('length: ',self.get_av_length(),'favorite types: ',self.get_fav_types())

        #get every content page

        cur.execute('SELECT * FROM CONTENT WHERE type = %s',('ShortStory',))
        s_stories = cur.fetchall()
        cur.execute('SELECT * FROM CONTENT WHERE type = %s',('Poem',))
        poems = cur.fetchall()
        cur.execute('SELECT * FROM CONTENT WHERE type = %s',('Book',))
        books = cur.fetchall()
        #select three random pages of every type, which one does our user like the most
        highest_score = 0
        favorite_page = tuple()
        for n in range(6):
            if (n < 2) :
                page = random.choice(s_stories)
                s_score = rank_dict(self.get_preferences(),get_csv_dict(page[3]))*self.get_fav_types()['ShortStory']

                if (s_score > highest_score):
                    highest_score = s_score
                    favorite_page = page
            if (2 <= n < 4) :
                page = random.choice(poems)
                p_score = rank_dict(self.get_preferences(),get_csv_dict(page[3]))*self.get_fav_types()['Poem']

                if (p_score > highest_score):
                    highest_score = p_score
                    favorite_page = page

            if (4 <= n < 6) :
                page = random.choice(books)
                b_score = rank_dict(self.get_preferences(),get_csv_dict(page[3]))*self.get_fav_types()['Book']

                if (b_score > highest_score):
                    highest_score = b_score
                    favorite_page = page

        print('name:',self.name,'favorite page is: ',favorite_page)
        conn.close()
        cur.close()
            #page = random.choice(cur.fetchall())

user = Users()
user.traverse_site()
