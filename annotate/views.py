from django.shortcuts import render
from main import lang
from corst.db_settings import Database
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .models import Document
import random
import re
from pymystem3 import Mystem


from .forms import Text



def switch_lang(req):
    if (req.find("en") != -1):
        lang.lang = "en"
    if (req.find("ru") != -1):
        lang.lang = "ru"

@csrf_exempt
def document_view(request):
    db = Database()
    if request.POST.get('tags') or request.POST.get('comment') or request.POST.get('word'):
        tags = str(request.POST.get('tags'))
        comment = str(request.POST.get('comment'))
        word = str(request.POST.get('word'))
        print(tags,comment,word)
        if request.POST.get('document_id') and request.POST.get('start'):
            document_id = request.POST.get('document_id')
            st = request.POST.get('start')
            current_datetime = datetime.now()
            date = str(current_datetime)
            date = date[:-7]
            letters = "012345678abcdef"
            guid = ''.join(random.choice(letters) for i in range(8)) +'-'+''.join(random.choice(letters) for i in range(4))+'-'+''.join(random.choice(letters) for i in range(4))+'-'+''.join(random.choice(letters) for i in range(4))+'-'+''.join(random.choice(letters) for i in range(12))

            s='{"ranges": [{"start": "/span['+str(st)+']", "end": "/span['+str(st)+']", "startOffset": 0, "endOffset": '+ str(len(word))+'}], "quote": "'+word+'", "text": "' + comment + '", "tags": ["'+tags+'"]}'
            db.execute(f'insert into annotator_annotation values (null, {document_id}, {document_id}, "{guid}", "{date}", "{date}", \'{s}\', "{tags}", {st}, {st})')
            t = f'insert into annotator_annotation values (null, {document_id}, {document_id}, "{guid}", "{date}", "{date}", \'{s}\', "{tags}", {st}, {st})'
            print(t)
            # tag = db.execute(f'select as2.id, as2.tagged from annotator_sentence as2 where doc_id_id = 34')
            # print(tag)
            # start = int(tag[0]['id'])
            # end = int(tag[len(tag) - 1]['id']) + 1
            # tag2 = tuple()
            # for i in range(start, end):
            #     tag2 += db.execute(f'select document_id, tag, data from annotator_annotation where document_id = {i}')
            # print(tag2)

    tag = db.execute(f'select as2.id, as2.tagged, as2.doc_id_id from annotator_sentence as2 where doc_id_id = {request.GET.get("doc")}')
    start = int(tag[0]['id'])
    end = int(tag[len(tag)-1]['id'])+1
    tag2=tuple()
    for i in range(start,end):
        tag2 += db.execute(f'select document_id, tag, data from annotator_annotation where document_id = {i}')
    print(tag)
    text = ''
    for i in tag:
        text += i.get('tagged')
    tag2 = str(tag2).replace('\\\\',"\\");
    title = db.execute(f'select title from annotator_document where id = {request.GET.get("doc")}')[0].get('title')
    t1 = str(tag)
    t2 = t1.rfind('doc_id_id')
    t3=t1[t2+12:-2]
    db.commit()
    return render(request, 'main/document_view.html', {'doc': [title, text, tag, tag2, t3]})

def annotate(request):
    switch_lang(str(request))
    db = Database()
    users = db.execute("select username, first_name, last_name, id from auth_user where first_name <> ''")
    types = db.execute("select distinct major from annotator_document where major <> ''")

    not_annotated_quer = 'select id, title from annotator_document WHERE annotated = 0'
    if request.GET.get('usr'):
        usr = request.GET.get('usr')
        not_annotated_quer += f" AND owner_id = {usr}"
    if request.GET.get('major'):
        major = request.GET.get('major')
        not_annotated_quer += f" AND major = '{major}'"

    annotated_not_checked_quer = 'select id, title from annotator_document WHERE annotated = 1 AND checked = 0'
    if request.GET.get('usr'):
        usr = request.GET.get('usr')
        annotated_not_checked_quer += f" AND owner_id = {usr}"
    if request.GET.get('major'):
        major = request.GET.get('major')
        annotated_not_checked_quer += f" AND major = '{major}'"

    annotated_and_checked_quer = 'select id, title from annotator_document WHERE annotated = 1 AND checked = 1'
    if request.GET.getlist('usr'):
        usr = request.GET.get('usr')
        annotated_and_checked_quer += f" AND owner_id = {usr}"
    if request.GET.getlist('major'):
        major = request.GET.get('major')
        annotated_and_checked_quer += f" AND major = '{major}'"

    not_annotated = db.execute(not_annotated_quer)
    annotated_not_checked = db.execute(annotated_not_checked_quer)
    annotated_and_checked = db.execute(annotated_and_checked_quer)

    if(lang.lang=="en"):
        return render(request, 'main/annotate_en.html', {'users': users,
                                                  'types': types,
                                                  'not_annotated': not_annotated,
                                                  'annotated_not_checked': annotated_not_checked,
                                                  'annotated_and_checked': annotated_and_checked})
    else:
        return render(request, 'main/annotate.html', {'users': users,
                                                      'types': types,
                                                      'not_annotated': not_annotated,
                                                      'annotated_not_checked': annotated_not_checked,
                                                      'annotated_and_checked': annotated_and_checked
                                                      })



def document_add(request):
    if request.method == "POST":
        form = Text(request.POST or None)
        if form.is_valid():
            doc_id = int(form.cleaned_data.get('id'))
            title = form.cleaned_data.get('title')
            text = form.cleaned_data.get('text')
            owner = int(form.cleaned_data.get('owner'))
            author = form.cleaned_data.get('author')
            gender = form.cleaned_data.get('gender')
            major = form.cleaned_data.get('major')
            genre = form.cleaned_data.get('genre')
            domain = form.cleaned_data.get('domain')
            university = form.cleaned_data.get('university')
            student_code = int(form.cleaned_data.get('student_code'))
            university_code = int(form.cleaned_data.get('university_code'))
            date_1 = int(form.cleaned_data.get('date_1'))
            date_2 = int(form.cleaned_data.get('date_2'))
            course = form.cleaned_data.get('course')
            is_marked = form.cleaned_data.get('is_marked')
            is_checked = form.cleaned_data.get('is_checked')

            current_datetime = datetime.now()
            created = str(current_datetime)

            db = Database()
            db.execute('SET FOREIGN_KEY_CHECKS=0')

            m = Mystem(entire_input=True, grammar_info=True, disambiguation=True)

            analyzed_text = m.analyze(text)
            print(analyzed_text)
            i = 0
            sentence = ''
            sentence_tagged = ''
            sentences = []
            sentences_tagged = []
            num_words = 0

            while i <= len(analyzed_text) - 1:
                word = analyzed_text[i]['text']
                num_words += 1
                if 'analysis' in analyzed_text[i].keys() and analyzed_text[i]['analysis'] != []:
                    word_tagged = '<span class="token" data-toggle="tooltip" title="<b>' + \
                                  analyzed_text[i]['analysis'][0]['lex'] + ',' + analyzed_text[i]['analysis'][0][
                                      'gr'] + '</b>">' + analyzed_text[i]['text'] + "</span>"
                else:
                    word_tagged = analyzed_text[i]['text']
                if word == '\s' or i == len(analyzed_text) - 1:
                    sentences.append(sentence)
                    sentences_tagged.append(sentence_tagged)
                    sentence = ''
                    sentence_tagged = ''
                else:
                    sentence += word
                    sentence_tagged += word_tagged
                i += 1



            title_new = genre + "(" + major + ',' + course + ")"
            quer1 = f'insert into annotator_document values ({doc_id}, {owner}, "{created}", "{title_new}", "{text}", "{author}", "{title}", {date_1}, {date_2}, "{genre}", "{gender}", "{major}", "{course}", null, null, "{domain}", " ", " ", "{university}", {university_code}, {student_code}, {num_words}, {len(sentences)}, {date_1}, {is_marked}, {is_checked})'
            print(quer1)

            db.execute(quer1)
            db.commit()

            doc = Document(id = doc_id,
                           title=title,
                           text=text,
                           owner=owner,
                           author=author,
                           gender=gender,
                           major=major,
                           genre=genre,
                           domain=domain,
                           university=university,
                           student_code=student_code,
                           university_code=university_code,
                           date_1=date_1,
                           date_2=date_2,
                           course=course,
                           is_marked=bool(is_marked),
                           is_checked=bool(is_checked))
            doc.save(force_insert=True)




            j = 0
            sentence_ids = []
            while j <= len(sentences) - 1:
                id = int(db.execute("select max(id) as id from annotator_sentence aa ")[0].get('id')) + 1
                quer2 = f'insert into annotator_sentence values ({id}, \'{sentences[j]}\', {doc_id}, {j}, \'{sentences_tagged[j]}\', null)'
                db.execute(quer2)
                sentence_ids.append(id)
                db.commit()
                j += 1

            print(sentence_ids)

            word_num = 0
            sentence_num = 0
            sentence_insert = sentence_ids[sentence_num]
            while word_num <= len(analyzed_text) - 1:
                word = analyzed_text[word_num]['text']
                if word  == '\s':
                    sentence_num += 1
                    sentence_insert = sentence_ids[sentence_num]
                    continue
                if text == ' ' or text == ', ':
                    continue
                if 'analysis' in analyzed_text[word_num].keys() and analyzed_text[word_num]['analysis'] != []:
                    gr_split = re.split(r',',analyzed_text[word_num]['analysis'][0]['gr'])
                    if len(gr_split) == 1:
                        morph_id = int(db.execute("select max(id) as id from annotator_morphology aa ")[0].get('id')) + 1
                        lex = gr_split[0]
                        gram = ''
                        lem = analyzed_text[word_num]['analysis'][0]['lex']

                        token_id = int(db.execute("select max(id) as id from annotator_token aa ")[0].get('id')) + 1
                        token_text = analyzed_text[word_num]['text']
                        token_doc_id = doc_id
                        sent_id = sentence_insert
                        num = word_num
                        punctl = ''
                        punctr = ''
                        sent_pos = ''

                        quer3 = f'insert into annotator_token values ({token_id}, \'{token_text}\', {token_doc_id}, {sentence_insert}, {num}, \'{punctl}\', \'{punctr}\', \'{sent_pos}\')'
                        quer4 = f'insert into annotator_morphology values ({morph_id}, {token_id}, \'{lem}\', \'{lex}\', \'{gram}\')'
                        print(quer3)
                        print(quer4)
                        db.execute(quer3)
                        db.commit()
                        db.execute(quer4)
                        db.commit()

                    elif len(gr_split) > 1:
                        morph_id = int(db.execute("select max(id) as id from annotator_morphology aa ")[0].get('id')) + 1
                        lex = gr_split[0]
                        gram = ",".join(gr_split[1:])
                        lem = analyzed_text[word_num]['analysis'][0]['lex']

                        token_id = int(db.execute("select max(id) as id from annotator_token aa ")[0].get('id')) + 1
                        token_text = analyzed_text[word_num]['text']
                        token_doc_id = doc_id
                        sent_id = sentence_num
                        num = word_num
                        punctl = ''
                        punctr = ''
                        sent_pos = ''

                        quer3 = f'insert into annotator_token values ({token_id}, \'{token_text}\', {token_doc_id}, {sent_id}, {num}, \'{punctl}\', \'{punctr}\', \'{sent_pos}\')'
                        quer4 = f'insert into annotator_morphology values ({morph_id}, {token_id}, \'{lem}\', \'{lex}\', \'{gram}\')'
                        print(quer3)
                        print(quer4)
                        db.execute(quer3)
                        db.commit()
                        db.execute(quer4)
                        db.commit()
                word_num += 1
            db.execute('SET FOREIGN_KEY_CHECKS=1')
    form = Text()
    return render(request, 'main/add_document.html', {'form': form})