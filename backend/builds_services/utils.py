from builds_services.models import BuildServiceContainer, BuildsServices
from backend.sql_select import sql_select

def count_services(container_id):
    sql = '''select count(s.id) count
               from d_build_service_container sc,
                    s_services s
              where sc.id = container_id
                and s.contaner_id = sc.id
          '''
    return sql_select(sql)[0].get('count')
