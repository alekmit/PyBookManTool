#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pybookman.py
#
#  Copyright 2018 alekmit <alekmit@alekmit-Aspire-V3-372>
#
#

import sys
import re
import os
import shutil
import zipfile
import xml.etree.ElementTree as ET

XP_ALL = "./*"
XP_GENRE = ".//%sgenre"
XP_AUTHOR_L = ".//%slast-name"
XP_AUTHOR_F = ".//%sfirst-name"
XP_SEQUENCE = ".//%ssequence"


source_path = './'
target_fb2 = '../books/fb2/'
target_epub = '../books/epub/'
target_txt = '../books/txt/'

counter = 0

author_genres = ['Science Fiction', 'Horror', 'Fantasy', 'Detective', 'Prose',
    'Adventure', 'Antique', 'Philosophy', 'Politics', 'Publicism', 'Religion']

translit = {
    'а':'a',
    'б':'b',
    'в':'v',
    'г':'g',
    'д':'d',
    'е':'e',
    'ё':'yo',
    'ж':'zh',
    'з':'z',
    'и':'i',
    'й':'y',
    'к':'k',
    'л':'l',
    'м':'m',
    'н':'n',
    'о':'o',
    'п':'p',
    'р':'r',
    'с':'s',
    'т':'t',
    'у':'u',
    'ф':'f',
    'х':'h',
    'ц':'ts',
    'ч':'ch',
    'ш':'sh',
    'щ':'shch',
    'ъ':'y',
    'ы':'y',
    'ь':"'",
    'э':'e',
    'ю':'yu',
    'я':'ya',

    'А':'A',
    'Б':'B',
    'В':'V',
    'Г':'G',
    'Д':'D',
    'Е':'E',
    'Ё':'Yo',
    'Ж':'Zh',
    'З':'Z',
    'И':'I',
    'Й':'Y',
    'К':'K',
    'Л':'L',
    'М':'M',
    'Н':'N',
    'О':'O',
    'П':'P',
    'Р':'R',
    'С':'S',
    'Т':'T',
    'У':'U',
    'Ф':'F',
    'Х':'H',
    'Ц':'Ts',
    'Ч':'Ch',
    'Ш':'Sh',
    'Щ':'Shch',
    'Ъ':'Y',
    'Ы':'Y',
    'Ь':"'",
    'Э':'E',
    'Ю':'Yu',
    'Я':'Ya'
}

genres_types = {
    'sf_history': 'Science Fiction',
    'sf_action': 'Science Fiction',
    'sf_epic': 'Science Fiction',
    'sf_heroic': 'Science Fiction',
    'sf_detective': 'Science Fiction',
    'sf_cyberpunk': 'Science Fiction',
    'sf_space': 'Science Fiction',
    'sf_social': 'Science Fiction',
    'sf_horror': 'Horror',
    'sf_humor': 'Science Fiction',
    'sf_fantasy': 'Fantasy',
    'sf_stimpank', 'Steam Punk',
    'romance_sf': 'Science Fiction',
    'foreign_sf': 'Science Fiction',
    'economics': 'Economics',
    'economics_ref': 'Economics',
    'sf_etc': 'Science Fiction',
    'sf': 'Science Fiction',
    'det_classic': 'Detective',
    'det_police': 'Detective',
    'det_action': 'Detective',
    'det_irony': 'Detective',
    'det_history': 'Detective',
    'det_espionage': 'Detective',
    'det_crime': 'Detective',
    'det_political': 'Detective',
    'det_maniac': 'Detective',
    'det_hard': 'Detective',
    'thriller': 'Detective',
    'detective': 'Detective',
    'prose': 'Prose',
    'prose_classic': 'Prose',
    'prose_history': 'Prose',
    'prose_contemporary': 'Prose',
    'prose_counter': 'Prose',
    'prose_rus_classic': 'Prose',
    'prose_su_classics': 'Prose',
    'foreign_prose': 'Prose',
    'love': 'Love',
    'love_contemporary': 'Love',
    'love_history': 'Love',
    'love_detective': 'Love',
    'love_short': 'Love',
    'love_erotica': 'Love',
    'adv_western': 'Adventure',
    'adv_history': 'Adventure',
    'adv_indian': 'Adventure',
    'adv_maritime': 'Adventure',
    'adv_geo': 'Adventure',
    'adventure': 'Adventure',
    'child_adv': 'Child',
    'children': 'Child',
    'child_tale': 'Child',
    'child_prose': 'Child',
    'child_sf': 'Child',
    'child_det': 'Child',
    'child_education': 'Child',
    'poetry': 'Poetry',
    'dramaturgy': 'Dramaturgy',
    'child_verse': 'Child',
    'antique_ant': 'Antique',
    'antique_european': 'Antique',
    'antique_russian': 'Antique',
    'antique_east': 'Antique',
    'antique_myths': 'Antique',
    'antique': 'Antique',
    'sci_cosmos', 'Astronomy'
    'sci_history': 'History',
    'sci_psychology': 'Psychology',
    'sci_culture': 'Culture',
    'sci_philosophy': 'Philosophy',
    'sci_politics': 'Politics',
    'sci_business': 'Economics',
    'sci_juris': 'Juris',
    'sci_linguistic': 'Linguistic',
    'sci_medicine': 'Medicine',
    'sci_phys': 'Physics',
    'sci_math': 'Math',
    'sci_chem': 'Chemistry',
    'sci_biology': 'Biology',
    'sci_tech': 'Tech',
    'sci_transport': 'Tech',
    'sci_radio': 'Radio',
    'sci_geo': 'Geo'
    'science': 'Science',
    'comp_www': 'IT',
    'comp_programming': 'Programming',
    'comp_hard': 'Computers',
    'comp_soft': 'IT',
    'comp_db': 'IT',
    'comp_osnet': 'IT',
    'computers': 'IT',
    'ref_encyc': 'Reference',
    'ref_dict': 'Reference',
    'ref_ref': 'Reference',
    'ref_guide': 'Reference',
    'reference': 'Reference',
    'nonf_biography': 'Biography',
    'nonf_publicism': 'Publicism',
    'nonf_criticism': 'Publicism',
    'nonfiction': 'Publicism',
    'design': 'Art',
    'adv_animal': 'Nature',
    'religion': 'Religion',
    'religion_rel': 'Religion',
    'religion_esoterics': 'Religion',
    'religion_catholicism': 'Religion',
    'religion_self': 'Religion',
    'sci_religion': 'Religion',
    'humor_anecdote': 'Humor',
    'humor_prose': 'Humor',
    'humor_verse': 'Humor',
    'humor': 'Humor',
    'home_cooking': 'Home',
    'home_pets': 'Home',
    'home_crafts': 'Home',
    'home_entertain': 'Home',
    'home_health': 'Home',
    'home_garden': 'Home',
    'home_diy': 'Home',
    'home_sport': 'Home',
    'home_sex': 'Home',
    'home': 'Home',
    'military_special': 'Military',
    'military_weapon': 'Military',
    'literature_20': 'Misc',
    'foreign_edu': 'Education'
}


def translate(s):
  ts = []
  for c in s:
    ts.append(translit.get(c, c))
  return ''.join(ts)


def parseFb2(fb2):
  print("Parsing a fb2 file %s\n" % fb2)
  tree = None
  try:
    tree = ET.parse(fb2)
  except:
    print("Error while parsing a fb2 file %s\n" % fb2)
    return
  root = tree.getroot()
  m = re.match('\{.*\}', root.tag)
  ns = m.group(0) if m else ''
  genre = tree.findall(XP_GENRE % ns)
  p_genre = genre[0].text
  lname = tree.findall(XP_AUTHOR_L % ns)
  fname = tree.findall(XP_AUTHOR_F % ns)
  sequence = tree.findall(XP_SEQUENCE % ns)
  try:
    p_author = lname[0].text + ' ' + fname[0].text
    #print("p_author: %s\n" % p_author)
  except:
    p_author = None
  try:
    p_seq = sequence[0].get('name')
    print("p_seq: %s\n" % p_seq)
  except:
    p_seq = None
  #print("Genre: %s\n" % p_genre)
  #print("Author: %s\n" % p_author)
  p_genre = genres_types.get(p_genre, 'Misc')
  #print("Decoded Genre: %s\n" % p_genre)
  p_author = p_author.strip() if p_author and p_genre in author_genres else ''
  p_seq = p_seq.strip() if p_seq else ''
  new_target = os.path.join(target_fb2, p_genre, p_author, p_seq)
  new_target = translate(new_target)
  os.makedirs(new_target, exist_ok=True)
  tp =  os.path.join(new_target, os.path.basename(fb2))
  print("Target path: %s\n" % tp)
  shutil.copyfile(fb2, tp, follow_symlinks=False)
  print("Removing: %s\n" % fb2)
  os.remove(fb2)


def processFb2ZipFile(f):
  zf = zipfile.ZipFile(f)
  os.makedirs(target_fb2, exist_ok=True)
  for z in zf.namelist():
    unzipped = zf.extract(z, target_fb2)
    parseFb2(unzipped)
  zf.close()
  os.remove(f)


def processFb2File(f):
  os.makedirs(target_fb2, exist_ok=True)
  tp =  os.path.join(target_fb2, os.path.basename(f))
  shutil.copyfile(f, tp, follow_symlinks=False)
  parseFb2(tp)
  os.remove(f)

def processEpubFile(root, f):
  owndir = os.path.split(root)[-1] if len(os.path.split(root)) > 1 else ''
  dir = os.path.join(target_epub, owndir)
  os.makedirs(dir, exist_ok=True)
  tp = os.path.join(dir, os.path.basename(f))
  try:
    shutil.copyfile(f, tp, follow_symlinks=False)
    os.remove(f)
  except:
    print("Transfering Error %s\n" % f)

def processTxtZipFile(f):
  zf = zipfile.ZipFile(f)
  dir =  target_txt
  if (len(zf.namelist()) > 1):
    zn = os.path.splitext(os.path.basename(f))[0]
    dir = os.path.join(dir, zn)
  os.makedirs(dir, exist_ok=True)
  for z in zf.namelist():
    unzipped = zf.extract(z, dir)
    shutil.copyfile(f, unzipped, follow_symlinks=False)
  zf.close()
  os.remove(f)

def processTxtFile(root, f):
  owndir = os.path.split(root)[-1] if len(os.path.split(root)) > 1 else ''
  dir = os.path.join(target_txt, owndir)
  os.makedirs(dir, exist_ok=True)
  tp = os.path.join(dir, os.path.basename(f))
  try:
    shutil.copyfile(f, tp, follow_symlinks=False)
    os.remove(f)
  except:
    print("Transfering Error %s\n" % f)

def walkBooks():
  global counter
  for root, dirs, files in os.walk(source_path):
    for f in files:
      fn = f.lower()
      f = os.path.join(root, f)
      if fn.endswith(".fb2.zip"):
        print("Processing a fb2 file %s\n" % f)
        processFb2ZipFile(f)
        counter += 1
      elif fn.endswith(".fb2"):
        print("Processing a fb2 file %s\n" % f)
        processFb2File(f)
        counter += 1
      elif fn.endswith(".epub"):
        print("Transfering a epub file %s\n" % f)
        processEpubFile(root, f)
        counter += 1
      if fn.endswith(".txt.zip"):
        print("Processing a txt.zip file %s\n" % f)
        processTxtZipFile(f)
        counter += 1
      elif fn.endswith(".txt"):
        print("Transfering a txt file %s\n" % f)
        processTxtFile(root, f)
        counter += 1


def main(argv):
    pcount = len(argv)
    if (pcount > 2):
      source_path = argv[1]
      target_path = argv[2]
    elif pcount > 1:
      target_path = argv[1]
    walkBooks()
    return 0

if __name__ == '__main__':
    main(sys.argv)
    print("Processed %d book files\n" % counter)
    sys.exit(0)
