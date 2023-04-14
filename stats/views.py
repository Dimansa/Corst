from django.shortcuts import render

from corst.db_settings import Database
from main import lang
from .forms import Years

def switch_lang(req):
    if (req.find("en") != -1):
        lang.lang = "en"
    if (req.find("ru") != -1):
        lang.lang = "ru"

def stats(request):
    first_date = 1900
    second_date = 2200

    if request.method == "POST":
        form = Years(request.POST or None)
        if form.is_valid():
            first_date = int(form.cleaned_data.get('first_date'))
            second_date = int(form.cleaned_data.get('second_date'))
    print(first_date, second_date)

    form = Years()

    db = Database()
    query = db.execute(f'''select annotated.counter as annotated, checked.counter as checked, summary.counter as summary  from 
                      (select 1, count(annotated) as counter from annotator_document where annotated = 1 and date1 >= {first_date} and date2 <= {second_date}) as annotated
                      join (select 1, count(annotated) as counter from annotator_document where checked = 1 and date1 >= {first_date} and date2 <= {second_date}) as checked on checked.1 = annotated.1
                      join (select 1, count(annotated) as counter from annotator_document where date1 >= {first_date} and date2 <= {second_date}) as summary on summary.1 = annotated.1
''')
    doc_ann = query[0].get('annotated')
    doc_ann_percent = int(100 * query[0].get('annotated') / query[0].get('summary'))
    doc_check = query[0].get('checked')
    doc_check_percent = int(100 * query[0].get('checked') / query[0].get('summary'))
    docs = query[0].get('summary')

    words = db.execute(f'''select count(atk.id) as words from annotator_token atk
                            join annotator_document ad on ad.id = atk.doc_id
                            where ad.date1 >= {first_date} and ad.date2 <= {second_date}''')[0].get('words')

    sentences = db.execute(f'''select count(asn.id) as sentences from annotator_sentence asn
								join annotator_token at2 on at2.sent_id = asn.id
                                join annotator_document ad on ad.id = at2.doc_id 
								where ad.date1 >= {first_date} and ad.date2 <= {second_date}''')[0].get('sentences')

    annotations = db.execute(f'''select count(aa.id) as annotations from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}''')[0].get('annotations')

    gender = db.execute(f'''select case
	                                when gender = '' or gender is null  then 'unknown'
	                                when gender = 'ж' then 'женский'
	                                when gender = 'м' then 'мужской'
	                              end as gender_group,
	                              count(id) as counter from annotator_document
	                              where date1 >= {first_date} and date2 <= {second_date}
                          group by gender_group''')

    genre = db.execute(f'''select genre, count(id) as counter from annotator_document
                          where date1 >= {first_date} and date2 <= {second_date}
                          group by genre
                          order by genre''')

    major = db.execute(f'''select major, count(id) as counter from annotator_document
                              where date1 >= {first_date} and date2 <= {second_date}
                              group by major
                              order by major''')

    course = db.execute(f'''select course, count(id) as counter from annotator_document
                              where date1 >= {first_date} and date2 <= {second_date}
                              group by course
                              order by course''')

    domain = db.execute(f'''select domain, count(id) as counter from annotator_document
                                  where date1 >= {first_date} and date2 <= {second_date}
                                  group by course
                                  order by course''')

    total_errors = db.execute(f'''select count(tag) as error_count from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}''')[0].get('error_count')

    lex_errors = db.execute(f''' select count(tag) as error_count from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                 and tag like ('%lex%')
                                                or tag like('%word%')
                                                or tag like('%phrase%')
                                                or tag like('%meton%')
                                                or tag like('%intens%')
                                                or tag like('%deriv%')
                                                or tag like('%paron%')
                                                or tag like('%asp%')
                                                or tag like('%nmz%')
                                                or tag like('%aux%')''')[0].get('error_count')
    style_errors = db.execute(f'''select count(tag) as error_count from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                 and tag like ('%styl%')
                                                or tag like('%official%')
                                                or tag like('%colloq%')''')[0].get('error_count')

    gram_errors = db.execute(f'''select count(tag) as error_count from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                 and tag like ('%agr%')
                                                or tag like('%gov%')
                                                or tag like('%infl%')
                                                or tag like('%compar%')
                                                or tag like('%complex%')
                                                or tag like('%rel_clause%')
                                                or tag like('%sent_arg%')
                                                or tag like('%conn%')
                                                or tag like('%coord%')
                                                or tag like('%discoord%')
                                                or tag like('%ref%')
                                                or tag like('%converb%')
                                                or tag like('%pron%')
                                                or tag like('%voice%')
                                                or tag like('%lack%')
                                                or tag like('%constr%')''')[0].get('error_count')

    discourse_errors = db.execute(f'''select count(tag) as error_count from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                     and tag like ('%discourse%')
                                                    or tag like ('%parc%')
                                                    or tag like ('%logic%')
                                                    or tag like ('%link%')
                                                    or tag like ('%WO%')
                                                    and tag not like ('%word%')
                                                    or tag like ('%tauto%')
                                                    or tag like ('%top%')''')[0].get('error_count')

    cause_errors = db.execute(f'''select count(tag) as error_count from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                     and tag like ('%cause%')
                                                    or tag like('%typo%')
                                                    or tag like('%contam%')''')[0].get('error_count')

    errors_group_by_tag = db.execute(f'''select case
                                        when tag like '%lex%' then 'lex'
                                        when tag like '%word%' and tag not like '%WO%' then 'word'
                                        when tag like '%phrase%' then 'phrase'
                                        when tag like '%meton%' then 'meton'
                                        when tag like '%intens%' then 'intens'
                                        when tag like '%deriv%' then 'deriv'
                                        when tag like '%paron%' then 'paron'
                                        when tag like '%asp%' then 'asp'
                                        when tag like '%nmz%' then 'nmz'
                                        when tag like '%aux%' then 'aux'
                                        when tag like '%styl%' then 'styl'
                                        when tag like '%official%' then 'official'
                                        when tag like '%colloq%' then 'colloq'
                                        when tag like '%agr%' then 'agr'
                                        when tag like '%gow%' then 'gow'
                                        when tag like '%infl%' then 'infl'
                                        when tag like '%compar%' then 'compar'
                                        when tag like '%complex%' then 'complex'
                                        when tag like '%rel_clause%' then 'rel_clause'
                                        when tag like '%sent_arg%' then 'sent_arg'
                                        when tag like '%conn%' then 'conn'
                                        when tag like '%coord%' and tag not like '%discoord%' then 'coord'
                                        when tag like '%discoord%' then 'discoord'
                                        when tag like '%ref%' then 'ref'
                                        when tag like '%converb%' then 'converb'
                                        when tag like '%pron%' then 'pron'
                                        when tag like '%voice%' then 'voice'
                                        when tag like '%lack%' then 'lack'
                                        when tag like '%constr%' then 'constr'
                                        when tag like '%discourse%' then 'discourse'
                                        when tag like '%parc%' then 'parc'
                                        when tag like '%logic%' then 'logic'
                                        when tag like '%link%' then 'link'
                                        when tag like '%WO%' and tag not like '%word%' then 'WO'
                                        when tag like '%tauto%' then 'tauto'
                                        when tag like '%top%' then 'top'
                                        when tag like '%cause%' then 'cause'
                                        when tag like '%typo%' then 'typo'
                                        when tag like '%contam%' then 'contam'
                                        else 'unknown'
                                      end as tag_group, count(aa.id) as counter from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                    group by tag_group
                                    ''')

    errors_group_by_major = db.execute(f'''select ad.major, count(aa.id) as counter from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                    group by major''')

    errors_group_by_course = db.execute(f'''select ad.course, count(aa.id) as counter from annotator_annotation aa
                                            join annotator_sentence asn on aa.document_id = asn.id
                                            join annotator_document ad on asn.doc_id_id = ad.id
                                            where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                            group by course''')

    errors_group_by_genre = db.execute(f'''select ad.genre, count(aa.id) as counter from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                            group by genre''')

    errors_group_by_gender = db.execute(f'''select case
                                                    when ad.gender = '' or gender is null  then 'unknown'
                                                    when ad.gender = 'ж' then 'женский'
                                                    when ad.gender = 'м' then 'мужской'
                                                  end as gender_group, 
                                                  count(aa.id) as counter from annotator_annotation aa
                                                join annotator_sentence asn on aa.document_id = asn.id
                                                join annotator_document ad on asn.doc_id_id = ad.id
                                                where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                            group by gender_group''')

    errors_group_by_date = db.execute(f'''select case
                                                    when ad.date_displayed  = '' or ad.date_displayed  is null  then 'unknown'
                                                    else ad.date_displayed 
                                                  end as date_group, 
                                                  count(aa.id) as counter from annotator_annotation aa
                                    join annotator_sentence asn on aa.document_id = asn.id
                                    join annotator_document ad on asn.doc_id_id = ad.id
                                    where ad.date1 >= {first_date} and ad.date2 <= {second_date}
                                            group by date_group''')

    switch_lang(str(request))
    if(lang.lang=="en"):
        stat = 'main/statistics_en.html'
    else:
        stat = 'main/statistics.html'
    return render(request, stat, {'progress': [doc_ann,
                                                                 doc_ann_percent,
                                                                 doc_check,
                                                                 doc_check_percent, docs],
                                                    'errors' : [total_errors,
                                                                lex_errors,
                                                                style_errors,
                                                                gram_errors,
                                                                discourse_errors,
                                                                cause_errors],
                                                    'docs': docs,
                                                    'words': words,
                                                    'sentences': sentences,
                                                    'annotations': annotations,
                                                    'gender': gender,
                                                    'genre': genre,
                                                    'major': major,
                                                    'course': course,
                                                    'domain': domain,
                                                    'form': form,
                                                    'errors_by_tag': errors_group_by_tag,
                                                    'errors_by_major': errors_group_by_major,
                                                    'errors_by_course': errors_group_by_course,
                                                    'errors_by_genre': errors_group_by_genre,
                                                    'errors_by_gender': errors_group_by_gender,
                                                    'errors_by_date': errors_group_by_date,
                                                    'date': [first_date, second_date]
                                                    })
