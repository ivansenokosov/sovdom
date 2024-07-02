from backend import sql_select
from builds_services.models import CostContainer, BuildServiceContainer, BuildCostContainers, BuildCostContainerData, CostContainerPrices
from backend.analyze import get_optimum_inspection_price


def get_denominator(build, p_denomintor_id):
  result = 0
  if p_denomintor_id == 1:
    result = build.s()
  elif p_denomintor_id == 2:
    result = build.s_mop
  elif p_denomintor_id == 3:
    result = build.s_zem
  elif p_denomintor_id == 4:
    result = build.q_lifts
  elif p_denomintor_id == 5:
    result = 1
  elif p_denomintor_id == 6:
    result = build.uu()
  
  if result == 0:
    result = 100 
  
  return result      


def get_micro_details_json(build):
  result = ''
  years = ''
  v_number = 1
  rownum = 0

  print('мы здесь')

  build_cost_containers =  BuildCostContainers.objects.filter(build_id = build.id).order_by('cost_container__display_order')
  result += "["

  for build_cost_container in build_cost_containers:
    rownum += 1
    cost_container = CostContainer.objects.get(id = build_cost_container.cost_container_id)
    denominator_build_value = get_denominator(build, cost_container.denominator.id)


    v_work      =''
    v_repair    =''
    v_stavka    =''
    v_stavka_tr =''
    v_avg       =''
    v_minmax    =''
    years       = ''
    v_price     =''
    v_container_max_value = 0
  
    reports = BuildServiceContainer.objects.filter(build_id = build.id).filter(type_id= 3).order_by('dend')



    for report in reports:
      year = int(report.dend.strftime('%Y'))
      container_data = BuildCostContainerData.objects.filter(cost_container_id = build_cost_container.cost_container_id).filter(build_id = build.id).filter(year = year).first()
      stavka = report.get_stavka_container_by_report()

      if container_data:
        years += "'" + str(year) + "',"

        if container_data.cost_rub: 
          v_work   +=  str(round(container_data.cost_rub,2)) + ','
        else:
          v_work   +=  '0,'  

        if container_data.cost_tr_rub:
          v_repair +=  str(round(container_data.cost_tr_rub,2)) + ','
        else:
          v_repair +=  '0,'

        if container_data.cost_rub + container_data.cost_tr_rub > v_container_max_value:
          v_container_max_value = container_data.cost_rub + container_data.cost_tr_rub

        if container_data.stavka_rub:
          v_stavka += str(round(float(container_data.stavka_rub) * float(build.s()) / float(denominator_build_value), 2)) + ',' 
        else:
          v_stavka += '0,'

        if container_data.stavka_tr_rub:
          v_stavka_tr += str(round(float(container_data.stavka_tr_rub) * float(build.s()) / float(denominator_build_value), 2)) + ',' 
        else:
          v_stavka_tr += '0,'
 


######### расчёт среднего, минимумов, максимуов по отчётам за год
        # sql_query = '''select round(avg(cost),2) as avg, 
        #                            round(min(cost),2) as min, 
        #                            round(max(cost),2) as max
        #         from (
        #             select l.build_id, 
        #                   sum( s.cost * (b.s_live + b.s_no_live) / ''' + str(denominator_build_value) + '''  ) cost
        #             from d_build_service_container l,
        #                  s_build_services s,
        #                  d_build b
        #             where s.container_id = l.id 
        #               and b.id = l.build_id
        #               and l.city_id = ''' + str(build.street.city_id) + '''
        #               and l.type_id = 3
        #               and extract(year from dbegin) = ''' + str(year) + ''' 
        #               and ((''' + str(cost_container.denominator.id) + ''' = 3 and COALESCE(b.s_zem,0) > 100) or (''' + str(cost_container.denominator.id) + ''' = 4 and COALESCE(b.q_lifts,0) > 0) or (''' + str(cost_container.denominator.id) + ''' = 6 and COALESCE(b.q_uu,0) > 0) or (''' + str(cost_container.denominator.id) + ''' in (1,2,5)))
        #               and COALESCE(s.cost,0)>0
        #               and (s.subgroup_id in (select subgroup_id from S_COST_CONTAINER_GROUPS where cost_container_id = ''' + str(cost_container.id) + ''') 
        #                    or s.to_290 in (select service_id from S_COST_CONTAINER_SERVICES  where cost_container_id = ''' + str(cost_container.id) + '''))
        #         group by l.build_id
        #         )'''
        
        # print(sql_query)
        # sql_response = sql_select(sql_query)

        # v_avg += str(round(sql_response[0].get('avg'),2)) + ','
        # v_minmax += '[' + str(round(sql_response[0].get('min'),2)) + ',' + str(round(sql_response[0].get('max'),2)) + '],'

########### определение оптимальной цены
        if cost_container.id == 9:
          v_price1 = get_optimum_inspection_price(build)
          v_price_count = 1
        else:
          monitoring_price = CostContainerPrices.objects.filter(cost_container_id = cost_container.id).filter(year = year).first()
          if monitoring_price:
            v_price1 = monitoring_price.price
            # тут можно ещё коэффициенты поприменять
            
        v_price += str(round(v_price1,2)) + ','
        
#### нормализуем данеые под JSON-объект
    years = years[0:len(years)-1]
    v_work= v_work[0:len(v_work)-1]
    v_repair = v_repair[0:len(v_repair)-1]
    v_stavka = v_stavka[0:len(v_stavka)-1]
    v_stavka_tr =v_stavka_tr[0:len(v_stavka_tr)-1]
    v_price =v_price[0:len(v_price)-1]

    result += '''[[{"name": "''' + cost_container.name + '''",
                   "subtitle": "''' + cost_container.subtitle + '''",
                   "denominator": "''' + cost_container.denominator.name + '''",
                   "container_max_value": "''' + str(v_container_max_value*2) + '''",
                   "denominator_value": "''' + str(denominator_build_value) + '''"}], ['''


    

  ############ Диапазон
    # if cost_container.show_minmax == True:
    #   result += """{
    #     type: 'arearange',
    #     name: 'Диапазон по отчётам',
    #     color: '#e0e0e0',
    #     data: [""" + v_minmax + """],
    #     pointPadding: 0.3,
    #     pointPlacement: 0.2,
    #     stack: '1'
    #   },"""

    if stavka:
      result += '''{
        "type": "column",
        "name": "Ставка платы",
        "color": "#b0b0b0",
        "data": [''' + v_stavka + '''],
        "pointPlacement": "0.2",
        "stack": "2"
      },'''
    
    if cost_container.show_repair == True and container_data.cost_tr_rub > 0:
      result += '''{
      "type": "column",
      "name": "Ставка платы ТР",
      "color": "#999999",
      "data": [''' + v_stavka_tr + '''],
      "pointPlacement": "0.2",
      "stack": "2"
    },'''

  ########## Работы
    result += '''{
    "type": "column",
    "name": "''' + cost_container.work_name + '''",
    "color": "#''' + cost_container.color1 + '''",
    "data": [''' + v_work + '''],
    "pointPadding": "0.3",
    "pointPlacement": "0.2",
    "stack": "1"
  }, '''
  
  
########### Текущий ремонт
    if cost_container.show_repair == True:
      result += '''{
        "type": "column",
        "name": "''' + cost_container.repair_name + '''",
        "color": "#''' + cost_container.color2 + '''",
        "data": [''' + v_repair + '''],
        "pointPadding": "0.3",
        "pointPlacement": "0.2",
        "stack": "1"
      },'''

  ############## Оптимальное
    if v_price_count > 0:
      result += '''{
        "type": "line",
        "name": "Оптимальное",
        "color": "#000000",
        "data": [''' +  v_price + '''],
        "pointPadding": "0.3",
        "pointPlacement": "0.2",
        "stack": "1"
      },'''

  # -------------- Среднее
    # if cost_container.show_avg == True:
    #   result += """{
    #     type: 'line',
    #     name: 'Среднее по отчётам',
    #     color: '#707070',
    #     data: [""" + v_avg + """],
    #     pointPadding: 0.3,
    #     pointPlacement: 0.2,
    #     stack: '1'
    #   }"""
    
    result = result[0:len(result)-1]

    result += ']],'

  result = result[0:len(result)-1]
  result += ']'

  v_number += 1





  return result;                      