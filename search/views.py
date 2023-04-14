from django.shortcuts import render

from django.core.paginator import Paginator
from django.http import FileResponse
import ast
import re
import xlsxwriter
from nltk.stem.snowball import RussianStemmer
from main import lang
from corst.db_settings import Database

def switch_lang(req):
    if (req.find("en=EN") != -1):
        lang.lang = "en"
    if (req.find("ru=RU") != -1):
        lang.lang = "ru"

def bold(word, sent):
    s = re.sub('('+word+')', '<b>\\1</b>', sent)
    return s

def download(request):
    if request.POST:
        workbook = xlsxwriter.Workbook('data.xlsx')
        worksheet = workbook.add_worksheet()

        cell_format = workbook.add_format({'bold' : True})
        cell_format.set_bg_color('#99EE6B')
        cell_format.set_border()

        worksheet.write('A1', 'Период', cell_format)
        worksheet.write('B1', 'Тип работы', cell_format)
        worksheet.write('C1', 'Вид научной деятельности', cell_format)
        worksheet.write('D1', 'Курс', cell_format)
        worksheet.write('E1', 'Текст', cell_format)
        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, 1, 15)
        worksheet.set_column(2, 2, 25)
        worksheet.set_column(3, 3, 15)
        worksheet.set_column(4, 4, 100)

        data = request.POST.getlist('download')
        data_list = []
        for el in data:
            data_list.append(ast.literal_eval(el))
        for i in range(1, len(data_list) + 1):
            worksheet.write(i, 0, data_list[i-1]['date_displayed'])
            worksheet.write(i, 1, data_list[i - 1]['genre'])
            worksheet.write(i, 2, data_list[i-1]['major'])
            worksheet.write(i, 3, data_list[i-1]['course'])
            worksheet.write(i, 4, data_list[i-1]['text'])
        workbook.close()
        return FileResponse(open('data.xlsx', 'rb'))


def search(request):
    flag = True
    quer = '''SELECT distinct as2.text, as2.tagged, ad.date_displayed , ad.genre, ad.major, ad.course  FROM annotator_sentence as2 
                                LEFT JOIN annotator_document ad ON ad.id = as2.doc_id_id 
                                LEFT JOIN annotator_annotation aa ON ad.id = aa.document_id and as2.num = aa.start
                                LEFT JOIN annotator_token at2 ON at2.doc_id = ad.id and as2.num = at2.num
                                LEFT JOIN annotator_morphology am ON am.token_id = at2.id
                                WHERE'''


    if request.GET.get('genAnswer'):
        quer += ' gender = "' + request.GET.get('genAnswer') + '"'

    quer += ' AND ( '

    if request.GET.get('cas6'):
        quer += ' OR course = "6 курс спец"'
    if request.GET.get('cas5'):
        quer += ' OR course = "5 курс спец"'
    if request.GET.get('cas4'):
        quer += ' OR course = "4 курс спец"'
    if request.GET.get('cas3'):
        quer += ' OR course = "3 курс спец"'
    if request.GET.get('cas2'):
        quer += ' OR course = "2 курс спец"'
    if request.GET.get('cas1'):
        quer += ' OR course = "1 курс спец"'
    if request.GET.get('cab4'):
        quer += ' OR course = "4 курс бак"'
    if request.GET.get('cab3'):
        quer += ' OR course = "3 курс бак"'
    if request.GET.get('cab2'):
        quer += ' OR course = "2 курс бак"'
    if request.GET.get('cab1'):
        quer += ' OR course = "1 курс бак"'

    quer += ' ) AND ( '

    if request.GET.get('conference'):
        quer += ' OR genre = "обзор конференции"'
    if request.GET.get('course_work'):
        quer += ' OR genre = "курсовая"'
    if request.GET.get('аutobiography'):
        quer += ' OR genre = "автобиография"'
    if request.GET.get('VKR'):
        quer += ' OR genre = "вкр"'
    if request.GET.get('statement'):
        quer += ' OR genre = "заявление"'
    if request.GET.get('essay'):
        quer += ' OR genre = "эссе"'
    if request.GET.get('annotation'):
        quer += ' OR genre = "аннотация"'
    if request.GET.get('paragraph'):
        quer += ' OR genre = "абзац"'
    if request.GET.get('course_work_draft'):
        quer += ' OR genre = "курсовая (черновик)"'
    if request.GET.get('semester_work'):
        quer += ' OR genre = "семестровая работа"'
    if request.GET.get('project_summary'):
        quer += ' OR genre = "аннотация проекта"'
    if request.GET.get('diploma'):
        quer += ' OR genre = "диплом"'
    if request.GET.get('commercial_offer'):
        quer += ' OR genre = "коммерческое предложение"'
    if request.GET.get('abstract'):
        quer += ' OR genre = "реферат"'

    quer += ' ) AND ( '

    if request.GET.get('Культурология'):
        quer += ' OR major = "Культурология"'
    if request.GET.get('Экономика'):
        quer += ' OR major = "Экономика"'
    if request.GET.get('История'):
        quer += ' OR major = "История"'
    if request.GET.get('Журналистика'):
        quer += ' OR major = "Журналистика"'
    if request.GET.get('Дизайн'):
        quer += ' OR major = "Дизайн"'
    if request.GET.get('Востоковедение'):
        quer += ' OR major = "Востоковедение"'
    if request.GET.get('Медиакоммуникации'):
        quer += ' OR major = "Медиакоммуникации"'
    if request.GET.get('Политология'):
        quer += ' OR major = "Политология"'
    if request.GET.get('Лингвистика'):
        quer += ' OR major = "Лингвистика"'
    if request.GET.get('Юриспруденция'):
        quer += ' OR major = "Юриспруденция"'
    if request.GET.get('Менеджмент'):
        quer += ' OR major = "Менеджмент"'
    if request.GET.get('Социология'):
        quer += ' OR major = "Социология"'
    if request.GET.get('Логистика'):
        quer += ' OR major = "Логистика"'
    if request.GET.get('Математика'):
        quer += ' OR major = "Математика"'
    if request.GET.get('Иностранные языки'):
        quer += ' OR major = "Иностранные языки"'
    if request.GET.get('Мировая экономика'):
        quer += ' OR major = "Мировая экономика"'
    if request.GET.get('Современное искусство'):
        quer += ' OR major = "Современное искусство"'
    if request.GET.get('Прикладная математика и информатика'):
        quer += ' OR major = "Прикладная математика и информатика"'
    if request.GET.get('Реклама и связи с общественностью'):
        quer += ' OR major = "Реклама и связи с общественностью"'
    if request.GET.get('Психология'):
        quer += ' OR major = "Психология"'
    if request.GET.get('История искусств'):
        quer += ' OR major = "История искусств"'
    if request.GET.get('Филология'):
        quer += ' OR major = "Филология"'

    quer += ' ) AND ( '

    if request.GET.get('политология_d'):
        quer += ' OR domain = "политология"'
    if request.GET.get('психология_d'):
        quer += ' OR domain = "психология"'
    if request.GET.get('разнородная_тематика_d'):
        quer += ' OR domain = "разнородная тематика"'
    if request.GET.get('менеджмент_d'):
        quer += ' OR domain = "менеджмент"'
    if request.GET.get('журналистика_d'):
        quer += ' OR domain = "журналистика"'
    if request.GET.get('право_d'):
        quer += ' OR domain = "право"'
    if request.GET.get('cоциология_d'):
        quer += ' OR domain = "cоциология"'
    if request.GET.get('риторика_d'):
        quer += ' OR domain = "риторика"'
    if request.GET.get('cоциолингвистика_d'):
        quer += ' OR domain = "cоциолингвистика"'
    if request.GET.get('лингвистика'):
        quer += ' OR domain = "лингвистика"'
    if request.GET.get('образование_d'):
        quer += ' OR domain = "образование"'
    if request.GET.get('филология_d'):
        quer += ' OR domain = "филология"'

    quer += ' ) AND ( '


    if request.GET.get('years1'):
        first_date = request.GET.get('years1')
        if (str(first_date).isdigit()):
            quer += f' date1 >= {first_date}'

    quer += ' ) AND ( '

    if request.GET.get('years2'):
        second_date = request.GET.get('years2')
        if(str(second_date).isdigit()):
            quer += f' date2 <= {second_date}'

    quer += ' ) AND ( '

    exact = ''
    wide = ''
    if request.GET.get('search1'):
        exact = request.GET.get('search1')
        quer += f" (locate(' {exact} ', text) OR locate(' {exact}.', text) OR locate(' {exact},', text)) AND lem = '{exact}'"

    if request.GET.get('search2'):
        stemmer = RussianStemmer()
        wide = request.GET.get('search2')
        initial_form = stemmer.stem(wide)
        quer += f" locate('<b>{wide}, ', tagged)"

    quer += ' ) AND ( '


    if request.GET.get('s'):
        quer += ' OR lex = "S"'

    if request.GET.get('a'):
        quer += ' OR lex = "A"'

    if request.GET.get('num'):
        quer += ' OR lex = "NUM"'

    if request.GET.get('anum'):
        quer += ' OR lex = "ANUM"'

    if request.GET.get('v'):
        quer += ' OR lex = "V"'

    if request.GET.get('adv'):
        quer += ' OR lex = "ADV"'

    if request.GET.get('adj'):
        quer += ' OR lex = "A"'

    if request.GET.get('parenth'):
        quer += ' OR lex = "PARENTH"'

    if request.GET.get('praedic'):
        quer += ' OR lex = "PRAEDIC"'

    if request.GET.get('advpro'):
        quer += ' OR lex = "ADVPRO"'

    if request.GET.get('spro'):
        quer += ' OR lex = "SPRO"'


    if request.GET.get('apro'):
        quer += ' OR lex = "APRO"'

    if request.GET.get('pr'):
        quer += ' OR lex = "PR"'

    if request.GET.get('CONJ'):
        quer += ' OR lex = "CONJ"'

    if request.GET.get('part'):
        quer += ' OR lex = "PART"'

    if request.GET.get('intj'):
        quer += ' OR lex = "INTJ"'


    quer += ' ) AND ( '

    if request.GET.get('m'):
        quer += " OR locate('m ', gram)"
    if request.GET.get('f'):
        quer += " OR locate('f ', gram)"
    if request.GET.get('n'):
        quer += " OR locate('n ', gram)"
    if request.GET.get('mf'):
        quer += " OR locate('mf ', gram)"
    if request.GET.get('nom'):
        quer += " OR locate('nom ', gram)"
    if request.GET.get('acc'):
        quer += " OR locate('acc ', gram)"
    if request.GET.get('dat'):
        quer += " OR locate('dat ', gram)"
    if request.GET.get('gen'):
        quer += " OR locate('gen ', gram)"
    if request.GET.get('ins'):
        quer += " OR locate('ins ', gram)"
    if request.GET.get('loc'):
        quer += " OR locate('loc ', gram)"
    if request.GET.get('loc2'):
        quer += " OR locate('loc2 ', gram)"
    if request.GET.get('gen2'):
        quer += " OR locate('gen2 ', gram)"
    if request.GET.get('comp'):
        quer += " OR locate('comp ', gram)"
    if request.GET.get('comp2'):
        quer += " OR locate('comp2 ', gram)"
    if request.GET.get('sup'):
        quer += " OR locate('sup ', gram)"
    if request.GET.get('plen'):
        quer += " OR locate('plen ', gram)"
    if request.GET.get('brev'):
        quer += " OR locate('brev ', gram)"
    if request.GET.get('sg'):
        quer += " OR locate('sg ', gram)"
    if request.GET.get('pl'):
        quer += " OR locate('pl ', gram)"
    if request.GET.get('anim'):
        quer += " OR locate('anim ', gram)"
    if request.GET.get('inan'):
        quer += " OR locate('inan ', gram)"
    if request.GET.get('indic'):
        quer += " OR locate('indic ', gram)"
    if request.GET.get('imper'):
        quer += " OR locate('imper ', gram)"
    if request.GET.get('imper2'):
        quer += " OR locate('imper2 ', gram)"
    if request.GET.get('inf'):
        quer += " OR locate('inf ', gram)"
    if request.GET.get('partcp'):
        quer += " OR locate('partcp ', gram)"
    if request.GET.get('ger'):
        quer += " OR locate('ger ', gram)"
    if request.GET.get('praes'):
        quer += " OR locate('praes ', gram)"
    if request.GET.get('fut'):
        quer += " OR locate('fut ', gram)"
    if request.GET.get('praet'):
        quer += " OR locate('praet ', gram)"
    if request.GET.get('pf'):
        quer += " OR locate('pf ', gram)"
    if request.GET.get('ipf'):
        quer += " OR locate('ipf ', gram)"
    if request.GET.get('1p'):
        quer += " OR locate('1p ', gram)"
    if request.GET.get('2p'):
        quer += " OR locate('2p ', gram)"
    if request.GET.get('3p'):
        quer += " OR locate('3p ', gram)"
    if request.GET.get('act'):
        quer += " OR locate('act ', gram)"
    if request.GET.get('pas'):
        quer += " OR locate('pas ', gram)"
    if request.GET.get('med'):
        quer += " OR locate('med ', gram)"
    if request.GET.get('tran'):
        quer += " OR locate('tran ', gram)"
    if request.GET.get('intr'):
        quer += " OR locate('intr ', gram)"
    if request.GET.get('famn'):
        quer += " OR locate('famn ', gram)"
    if request.GET.get('persn'):
        quer += " OR locate('persn ', gram)"
    if request.GET.get('patrn'):
        quer += " OR locate('patrn ', gram)"
    if request.GET.get('ciph'):
        quer += " OR locate('ciph ', gram)"
    if request.GET.get('anom'):
        quer += " OR locate('anom ', gram)"
    if request.GET.get('distort'):
        quer += " OR locate('distort ', gram)"
    if request.GET.get('INIT'):
        quer += " OR locate('INIT ', gram)"
    if request.GET.get('abbr'):
        quer += " OR locate('abbr ', gram)"
    if request.GET.get('0'):
        quer += " OR locate('0 ', gram)"
    if request.GET.get('topon'):
        quer += " OR locate('topon ', gram)"

    quer += ' ) AND ( '

    if request.GET.get('lex'):
        quer += " OR locate('lex, ', tag) OR locate('lex', tag)"
    if request.GET.get('word'):
        quer += " OR locate('word, ', tag) OR locate('word', tag)"
    if request.GET.get('phrase'):
        quer += " OR locate('phrase, ', tag) OR locate('phrase', tag)"
    if request.GET.get('meton'):
        quer += " OR locate('meton, ', tag) OR locate('meton', tag)"
    if request.GET.get('intens'):
        quer += " OR locate('intens, ', tag) OR locate('intens', tag)"
    if request.GET.get('deriv'):
        quer += " OR locate('deriv, ', tag) OR locate('deriv', tag)"
    if request.GET.get('paron'):
        quer += " OR locate('paron, ', tag) OR locate('paron', tag)"
    if request.GET.get('asp'):
        quer += " OR locate('asp, ', tag) OR locate('asp', tag)"
    if request.GET.get('nmz'):
        quer += " OR locate('nmz, ', tag) OR locate('nmz', tag)"
    if request.GET.get('aux'):
        quer += " OR locate('aux, ', tag) OR locate('aux', tag)"
    if request.GET.get('styl'):
        quer += " OR locate('styl, ', tag) OR locate('styl', tag)"
    if request.GET.get('official'):
        quer += " OR locate('official, ', tag) OR locate('official', tag)"
    if request.GET.get('colloq'):
        quer += " OR locate('colloq, ', tag) OR locate('colloq', tag)"
    if request.GET.get('agr'):
        quer += " OR locate('agr, ', tag) OR locate('agr', tag)"
    if request.GET.get('gov'):
        quer += " OR locate('gov, ', tag) OR locate('gov', tag)"
    if request.GET.get('infl'):
        quer += " OR locate('infl, ', tag) OR locate('infl', tag)"
    if request.GET.get('compar'):
        quer += " OR locate('compar, ', tag) OR locate('compar', tag)"
    if request.GET.get('complex'):
        quer += " OR locate('complex, ', tag) OR locate('complex', tag)"
    if request.GET.get('rel_clause'):
        quer += " OR locate('rel_clause, ', tag) OR locate('rel_clause', tag)"
    if request.GET.get('sent_arg'):
        quer += " OR locate('sent_arg, ', tag) OR locate('sent_arg', tag)"
    if request.GET.get('conn'):
        quer += " OR locate('conn, ', tag) OR locate('conn', tag)"
    if request.GET.get('coord'):
        quer += " OR locate('coord, ', tag) OR locate('coord', tag)"
    if request.GET.get('discoord'):
        quer += " OR locate('discoord, ', tag) OR locate('discoord', tag)"
    if request.GET.get('ref'):
        quer += " OR locate('ref, ', tag) OR locate('ref', tag)"
    if request.GET.get('converb'):
        quer += " OR locate('converb, ', tag) OR locate('converb', tag)"
    if request.GET.get('pron'):
        quer += " OR locate('pron, ', tag) OR locate('pron', tag)"
    if request.GET.get('voice'):
        quer += " OR locate('voice, ', tag) OR locate('voice', tag)"
    if request.GET.get('lack'):
        quer += " OR locate('lack, ', tag) OR locate('lack', tag)"
    if request.GET.get('constr'):
        quer += " OR locate('constr, ', tag) OR locate('constr', tag)"
    if request.GET.get('discourse'):
        quer += " OR locate('discourse, ', tag) OR locate('discourse', tag)"
    if request.GET.get('parc'):
        quer += " OR locate('parc, ', tag) OR locate('parc', tag)"
    if request.GET.get('logic'):
        quer += " OR locate('logic, ', tag) OR locate('logic', tag)"
    if request.GET.get('link'):
        quer += " OR locate('link, ', tag) OR locate('link', tag)"
    if request.GET.get('WO'):
        quer += " OR locate('tauto, ', tag) OR locate('tauto', tag)"
    if request.GET.get('top'):
        quer += " OR locate('top, ', tag) OR locate('top', tag)"
    if request.GET.get('cause'):
        quer += " OR locate('cause, ', tag) OR locate('cause', tag)"
    if request.GET.get('typo'):
        quer += " OR locate('typo, ', tag) OR locate('typo', tag)"
    if request.GET.get('contam'):
        quer += " OR locate('contam, ', tag) OR locate('contam', tag)"

    quer += ' )'


    if request.GET.get('sort_by'):
        quer += ' ORDER BY'
        if request.GET.get('sort_by') == "Лексеме" or request.GET.get('sort_by') == "Lexeme":
            quer += ' lex'
        if request.GET.get('sort_by') == "Словоформе" or request.GET.get('sort_by') == "Wordform":
            quer += f' {initial_form}'
        if request.GET.get('sort_by') == "Дате" or request.GET.get('sort_by') == "Date":
            quer += ' date1'
        if request.GET.get('sort_by') == "Дате в порядке убывания" or request.GET.get('sort_by') == "Date descending":
            quer += ' date1 desc'
        if request.GET.get('sort_by') == "Коду студента" or request.GET.get('sort_by') == "Student code":
            quer += ' student_code'


    for i in range(10):
        quer = quer.replace("  ", " ")
        quer = quer.replace('( )', '')
        quer = quer.replace('( OR ', '( ')
        quer = quer.replace('WHERE AND', 'WHERE ')
        quer = quer.replace('AND AND', 'AND')
    if quer[-4:] == "AND ":
        quer = quer[:-4]
    if quer[-6:] == "WHERE ":
        quer = quer[:-6]

    quer += ' LIMIT 1000'

    #print('\n\n\n' + quer + '\n\n\n')
    results = Database().execute(quer)
    if request.GET.get('page_number'):
        paginator = Paginator(results, int(request.GET.get('page_number')))
    else:
        paginator = Paginator(results, 100)

    if exact:
        for i in results:
            i['tagged'] = bold(exact, i['tagged'])

    if wide:
        for i in results:
            i['tagged'] = bold(initial_form, i['tagged'])

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    req = str(request)[27:-2]
    print(req)
    switch_lang(str(request))
    if(lang.lang == "en"):
        return render(request, 'main/search_en.html', {'page_obj': page_obj,
                                                    'results': results, 'req': req})
    else:
        return render(request, 'main/search.html', {'page_obj': page_obj,
                                                    'results' : results, 'req' : req})






