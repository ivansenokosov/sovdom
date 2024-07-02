from catalogs.models import Cities
from builds.models import Builds

from backend.sql_select import sql_select

def get_map_json(p_city_id):
    map_id = 1
    city = Cities.objects.get(pk = p_city_id)
    # builds = Builds.objects.filter(ymap != null).filter(report_number > 0)
    # v_center_coord = city.ymap
    sql = '''SELECT b.id,
       b.ymap, 
       s.name || ', ' || ifnull(b.number,'') || ifnull(b.litera,'') || ' ' || ifnull(b.corpse,'') addr,
       c.short_name,
	   (select count(id) from d_build_service_container sc where sc.build_id = b.id) q_report
  FROM d_build b, 
       s_street s,
       z_build_management m,
	   d_companies c
where b.street_id = s.id 
  and b.id = m.build_id
  and m.company_id = c.id
  and b.ymap is not null
  and (select count(id) from d_build_service_container sc where sc.build_id = b.id) > 0
  and b.ymap <> ''
  '''

    result = '['
  
    sql_result = sql_select(sql)

    for build in sql_result:
        result += '''{"type": "Feature", 
                        "id": ''' + build.get('id') + ''', 
                        "geometry": {"type": "Point", "coordinates":[''' + build.get('ymap') + ''']}, 
                        "options" : {"preset": "islands#blueStretchyIcon", "iconColor": "blue" },
                        "properties": {"balloonContentHeader": "''' + build.get('addr') + '''", "balloonContentBody": "''' + build.get('short_name').replace('"','') + '<br><br><b>Интерактивные сервисы и аналитика:</b><br><br>'''
             
        #  Анализ экономики
        if int(build.get('q_report')) > 0: 
            result += '''<a href='http://127.0.0.1:3000/site/build_economy?build_id=''' + build.get('id')  + '''' target='_blank'>Анализ экономики</a><br>'''
        else:
            result +='Анализ экономики ещё не выполнен.<br>'

        result += '" , "iconContent": "' + build.get('addr') + '''"}}, '''
        map_id += 1

    result = result[0:len(result)-2]

    result += ']'
    
    return result
################################################################################################################################################################################################################################################################################

