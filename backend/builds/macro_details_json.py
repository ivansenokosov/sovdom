from builds_services.models import BuildServiceContainer, ServiceGroups
from main.sql_select import sql_select
from builds_services.utils import count_services
from django.db.models import Q

def get_macro_details_json(p_build_id, p_extra_work):

# установка начальных значений
    v_stavka_total = 0
    v_report_sum_k = 0
    v_report_sum_e = 0
    v_report_sum_c = 0
    v_report_sum_m = 0
    v_report_sum_o = 0
    v_report_sum_u = 0
    v_stavka_sum_k = 0
    v_stavka_sum_e = 0
    v_stavka_sum_c = 0
    v_stavka_sum_m = 0
    v_stavka_sum_o = 0
    v_stavka_sum_u = 0
    v_stavka_sum_mun = 0
    v_stavka_by_report_sum = 0
    v_report_k_sum_tr = 0
    v_report_e_sum_tr = 0
    v_report_c_sum_tr = 0
    v_report_n_sum_tr = 0
    v_stavka_total_tr = 0

    v_data_report_k = ''
    v_data_report_e =  '' 
    v_data_report_c = '' 
    v_data_report_m = '' 
    v_data_report_o = ''
    v_data_report_u = ''
    v_data_stavka_k = ''
    v_data_stavka_e = ''
    v_data_stavka_c = ''
    v_data_stavka_m = ''
    v_data_stavka_o = ''
    v_data_stavka_u = ''
    v_data_stavka_mun = ''
    v_data_stavka_by_report = ''
    v_data_report_k_sum = ''
    v_data_report_e_sum = ''
    v_data_report_c_sum = ''
    v_data_report_m_sum = ''
    v_data_report_o_sum = ''
    v_data_report_u_sum = ''
    v_data_stavka_k_sum = ''
    v_data_stavka_e_sum = ''
    v_data_stavka_c_sum = ''
    v_data_stavka_m_sum = ''
    v_data_stavka_o_sum = ''
    v_data_stavka_u_sum = ''
    v_data_stavka_mun_sum = ''
    v_data_stavka_by_report_sum = ''
    v_data_report_k_tr = ''
    v_data_report_e_tr = ''
    v_data_report_c_tr = ''
    v_data_report_n_tr = ''
    v_data_report_k_ozhkh_tr = ''
    v_data_report_e_ozhkh_tr = ''
    v_data_report_c_ozhkh_tr = ''
    v_data_report_n_ozhkh_tr = ''
    v_data_document_tr = ''
    v_data_stavka_tr = ''
    v_data_report_k_sum_tr = ''
    v_data_report_e_sum_tr = ''
    v_data_report_c_sum_tr = ''
    v_data_report_n_sum_tr = ''
    v_data_report_k_sum_ozhkh_tr = ''
    v_data_report_e_sum_ozhkh_tr = ''
    v_data_report_c_sum_ozhkh_tr = ''
    v_data_report_n_sum_ozhkh_tr = ''
    v_data_document_sum_tr = ''
    v_data_stavka_sum_tr = ''

    v_series = ''
    result_sum = ''
    result_tr = ''
    result_tr_sum = ''

    months = 0
    s = 0

# получение исходных данных


# определяем есть ли вообще текущие ремонты
    sql = ''' 
select count(s.id) as count 
  from d_build_service_container sc, 
       s_build_services s 
 where sc.build_id = ''' + str(p_build_id) + '''
   and sc.id = s.container_id 
   and s.is_repair = True
                       '''
    v_tr_count = int(sql_select(sql)[0].get('count'))
    
    reports = BuildServiceContainer.objects.filter(build_id = p_build_id).filter(type_id = 3).order_by('dend')

    for report in reports:

        stavka =  report.get_stavka_container_by_report() # опрелеояем ставку платы отчёту
        v_series += '"' + report.dend.strftime('%Y') + '", '

        months = report.months()
        s = report.build.s()

        if stavka != report:
            v_stavka_tr = stavka.get_services_sum(-1, -1) * months * s
        else:
            v_stavka_tr = 0
        


        v_report_k = report.get_services_sum(49, -1) * months * s # конструктивные элементы
        v_report_e = report.get_services_sum(50, -1) * months * s  # инженерия
        v_report_c = report.get_services_sum(51, -1) * months * s # прочее ОИ
        v_report_m = report.get_services_sum(760, -1) * months * s # управление
        v_report_o = report.get_services_sum(1340, -1) * months * s # не входящие в минимальный перечень
        v_report_u = report.get_services_sum(40635, -1) * months * s # инженерия


        # текущие ремонты
        v_report_k_tr = report.get_services_sum(49, 1) * months * s # конструктивные элементы
        v_report_e_tr = report.get_services_sum(50, 1) * months * s # инженерия
        v_report_c_tr = report.get_services_sum(51, 1) * months * s # прочее ОИ
        v_report_n_tr = report.get_services_sum(1340, 1) * months * s # Не входящее в минимальный перечень
  

        # ставка платы
        v_stavka_k = stavka.get_services_sum(49, -1) * months * s
        v_stavka_e = stavka.get_services_sum(50, -1) * months * s
        v_stavka_c = stavka.get_services_sum(51, -1) * months * s
        v_stavka_m = stavka.get_services_sum(760, -1) * months * s
        v_stavka_o = stavka.get_services_sum(1340, -1) * months * s
        v_stavka_u = stavka.get_services_sum(40635, -1) * months * s  # неопределённые работы для недетализированных ставок


        if p_extra_work == 1:
            v_report_o = report.get_services_sum(1340, -1) * months * s # не входящие в минимальный перечень
            v_report_o_tr = report.get_services_sum(1340, 1) * months * s # Не входящее в минимальный перечень
        else:
           v_report_o = 0
           v_report_o_tr = 0


        v_stavka_mun = 0
        v_stavka_by_report = report.total_rub
        v_stavka_total = v_stavka_total + v_stavka_k + v_stavka_e + v_stavka_c + v_stavka_m + v_stavka_o + v_stavka_u
        v_stavka_by_report_to_show = 1
        v_show_oss_stavka = 1

        v_report_sum_k += v_report_k
        v_report_sum_e += v_report_e
        v_report_sum_c += v_report_c
        v_report_sum_m += v_report_m
        v_report_sum_o += v_report_o
        v_report_sum_u += v_report_u
        
        v_stavka_sum_k += v_stavka_k
        v_stavka_sum_e += v_stavka_e
        v_stavka_sum_c += v_stavka_c
        v_stavka_sum_m += v_stavka_m
        v_stavka_sum_o += v_stavka_o
        v_stavka_sum_u += v_stavka_u

        v_stavka_sum_mun += v_stavka_mun
        v_stavka_by_report_sum += v_stavka_by_report
      
      
        # текущие ремионты {

        v_report_k_sum_tr += v_report_k_tr
        v_report_e_sum_tr += v_report_e_tr
        v_report_c_sum_tr += v_report_c_tr
        v_report_n_sum_tr += v_report_n_tr


#        v_stavka_sum_tr   += v_stavka_sum_tr + v_stavka_tr       # ставка платы для текущих ремонтов
#        v_document_sum_tr = v_document_sum_tr,0) + v_document_tr,0) -- подтверждено

        # текущие ремионты }     




        v_data_report_k +=  str(round(v_report_k,2)) + ', ' 
        v_data_report_e +=  str(round(v_report_e,2)) + ', ' 
        v_data_report_c +=  str(round(v_report_c,2)) + ', ' 
        v_data_report_m +=  str(round(v_report_m,2)) + ', ' 
        v_data_report_o +=  str(round(v_report_o,2)) + ', ' 
        v_data_report_u +=  str(round(v_report_u,2)) + ', ' 
        
        v_data_stavka_k +=  str(round(v_stavka_k,2))  + ', ' 
        v_data_stavka_e +=  str(round(v_stavka_e,2))  + ', ' 
        v_data_stavka_c +=  str(round(v_stavka_c,2))  + ', ' 
        v_data_stavka_m +=  str(round(v_stavka_m,2))  + ', ' 
        v_data_stavka_o +=  str(round(v_stavka_o,2))  + ', ' 
        v_data_stavka_u +=  str(round(v_stavka_u,2))  + ', ' 


        v_data_stavka_mun +=  str(round(v_stavka_mun * 12 * report.build.s(), 2)) + ', ' 
        
        v_data_stavka_by_report += str(round(v_stavka_by_report,2)) + ', ' 

        # для накопительного итога

        v_data_report_k_sum +=  str(round(v_report_sum_k,2))  + ', ' 
        v_data_report_e_sum +=  str(round(v_report_sum_e,2))  + ', ' 
        v_data_report_c_sum +=  str(round(v_report_sum_c,2))  + ', ' 
        v_data_report_m_sum +=  str(round(v_report_sum_m,2))  + ', ' 
        v_data_report_o_sum +=  str(round(v_report_sum_o,2))  + ', ' 
        v_data_report_u_sum +=  str(round(v_report_sum_u,2))  + ', ' 
        
        v_data_stavka_k_sum +=  str(round(v_stavka_sum_k,2))  + ', ' 
        v_data_stavka_e_sum +=  str(round(v_stavka_sum_e,2))  + ', ' 
        v_data_stavka_c_sum +=  str(round(v_stavka_sum_c,2))  + ', ' 
        v_data_stavka_m_sum +=  str(round(v_stavka_sum_m,2))  + ', ' 
        v_data_stavka_o_sum +=  str(round(v_stavka_sum_o,2))  + ', ' 
        v_data_stavka_u_sum +=  str(round(v_stavka_sum_u,2))  + ', ' 
        
        v_data_stavka_mun_sum +=  str(round(v_stavka_sum_mun * 12 * report.build.s(), 2)) + ', ' 
        
        v_data_stavka_by_report_sum += str(round(v_stavka_by_report_sum, 2)) + ', '  


        # текущие ремионты {


        v_stavka_total_tr += v_stavka_tr

        v_data_report_k_tr +=  str(round(v_report_k_tr, 2))  + ', ' 
        v_data_report_e_tr +=  str(round(v_report_e_tr, 2))  + ', ' 
        v_data_report_c_tr +=  str(round(v_report_c_tr, 2))  + ', ' 
        v_data_report_n_tr +=  str(round(v_report_n_tr, 2))  + ', ' 
        # v_data_report_k_ozhkh_tr +=  str(round(v_report_k_ozhkh_tr, 2))  + ', ' 
        # v_data_report_e_ozhkh_tr +=  str(round(v_report_e_ozhkh_tr, 2))  + ', ' 
        # v_data_report_c_ozhkh_tr +=  str(round(v_report_c_ozhkh_tr, 2))  + ', ' 
        # v_data_report_n_ozhkh_tr +=  str(round(v_report_n_ozhkh_tr, 2))  + ', ' 
        # v_data_document_tr +=  str(round(v_document_tr, 2))  + ', ' 
        v_data_stavka_tr +=  str(round(v_stavka_tr, 2))  + ', ' 

        v_data_report_k_sum_tr +=  str(round(v_report_k_sum_tr, 2))  + ', ' 
        v_data_report_e_sum_tr +=  str(round(v_report_e_sum_tr, 2))  + ', ' 
        v_data_report_c_sum_tr +=  str(round(v_report_c_sum_tr, 2))  + ', ' 
        v_data_report_n_sum_tr +=  str(round(v_report_n_sum_tr, 2))  + ', ' 
        # v_data_report_k_sum_ozhkh_tr +=  str(round(v_report_k_sum_ozhkh_tr, 2))  + ', ' 
        # v_data_report_e_sum_ozhkh_tr +=  str(round(v_report_e_sum_ozhkh_tr, 2))  + ', ' 
        # v_data_report_c_sum_ozhkh_tr +=  str(round(v_report_c_sum_ozhkh_tr, 2))  + ', ' 
        # v_data_report_n_sum_ozhkh_tr +=  str(round(v_report_n_sum_ozhkh_tr, 2))  + ', ' 
        # v_data_document_sum_tr +=  str(round(v_document_sum_tr, 2))  + ', ' 
        # v_data_stavka_sum_tr +=  str(round(v_stavka_sum_tr, 2))  + ', ' 


        # текущие ремионты }

    # удяляем лишние зяпятые для нормалиазции JSON
    v_series = v_series[0:len(v_series)-2]
    v_data_report_k = v_data_report_k[0:len(v_data_report_k)-2]
    v_data_report_e = v_data_report_e[0:len(v_data_report_e)-2]
    v_data_report_c = v_data_report_c[0:len(v_data_report_c)-2]
    v_data_report_m = v_data_report_m[0:len(v_data_report_m)-2]
    v_data_report_o = v_data_report_o[0:len(v_data_report_o)-2]
    v_data_report_u = v_data_report_u[0:len(v_data_report_u)-2]
        
    v_data_stavka_k = v_data_stavka_k[0:len(v_data_stavka_k)-2]
    v_data_stavka_e = v_data_stavka_e[0:len(v_data_stavka_e)-2]
    v_data_stavka_c = v_data_stavka_c[0:len(v_data_stavka_c)-2]
    v_data_stavka_m = v_data_stavka_m[0:len(v_data_stavka_m)-2]
    v_data_stavka_o = v_data_stavka_o[0:len(v_data_stavka_o)-2]
    v_data_stavka_u = v_data_stavka_u[0:len(v_data_stavka_u)-2]
    v_data_stavka_mun = v_data_stavka_mun[0:len(v_data_stavka_mun)-2]
    v_data_stavka_by_report = v_data_stavka_by_report[0:len(v_data_stavka_by_report)-2]

    v_data_report_k_sum = v_data_report_k_sum[0:len(v_data_report_k_sum)-2] 
    v_data_report_e_sum = v_data_report_e_sum[0:len(v_data_report_e_sum)-2] 
    v_data_report_c_sum = v_data_report_c_sum[0:len(v_data_report_c_sum)-2] 
    v_data_report_m_sum = v_data_report_m_sum[0:len(v_data_report_m_sum)-2] 
    v_data_report_o_sum = v_data_report_o_sum[0:len(v_data_report_o_sum)-2] 
    v_data_report_u_sum = v_data_report_u_sum[0:len(v_data_report_u_sum)-2] 
       
    v_data_stavka_k_sum = v_data_stavka_k_sum[0:len(v_data_stavka_k_sum)-2]
    v_data_stavka_e_sum = v_data_stavka_e_sum[0:len(v_data_stavka_e_sum)-2]
    v_data_stavka_c_sum = v_data_stavka_c_sum[0:len(v_data_stavka_c_sum)-2]
    v_data_stavka_m_sum = v_data_stavka_m_sum[0:len(v_data_stavka_m_sum)-2]
    v_data_stavka_o_sum = v_data_stavka_o_sum[0:len(v_data_stavka_o_sum)-2]
    v_data_stavka_u_sum = v_data_stavka_u_sum[0:len(v_data_stavka_u_sum)-2]
    v_data_stavka_mun_sum = v_data_stavka_mun_sum[0:len(v_data_stavka_mun_sum)-2]
    v_data_stavka_by_report_sum = v_data_stavka_by_report_sum[0:len(v_data_stavka_by_report_sum)-2]




    v_color_k = ServiceGroups.objects.get(pk = 49).color
    v_color_e = ServiceGroups.objects.get(pk = 50).color
    v_color_c = ServiceGroups.objects.get(pk = 51).color
    v_color_m = ServiceGroups.objects.get(pk = 760).color
    v_color_o = ServiceGroups.objects.get(pk = 1340).color
    v_color_n = 'ff0000'
    v_color1 = '303030'


  

# формирование графиков
    result = '''[{"categories": [''' + v_series + ''']}, 
                      {"macro":['''
#    result = '{'
    
    if v_stavka_total > 0:
        result += '''{
            "name": "Конструктивные элементы Ставка",
            "data": [''' +  v_data_stavka_k + '''],
            "stack": "Ставка<br>платы",
            "color": "#''' + v_color_k + '''"
        }, {
            "name": "Инженерия Ставка",
            "data":  [''' + v_data_stavka_e + '''],
            "stack": "Ставка<br>платы",
            "color": "#''' + v_color_e + '''"
        }, {
            "name": "Прочее имущество Ставка",
            "data":  [''' + v_data_stavka_c + '''],
            "stack": "Ставка<br>платы",
            "color": "#'''+ v_color_c + '''"
        }, {
            "name": "Управление Ставка",
            "data":  [''' + v_data_stavka_m + '''],
            "stack": "Ставка<br>платы",
            "color": "#''' + v_color_m + '''"
        }, '''
    
    if v_stavka_sum_u:
        result += '''{
            "name": "Недетализированные работы",
            "data":  [''' + v_data_stavka_u + '''],
            "stack": "Ставка<br>платы",
            "color": "#c0c0c0"
        },'''


    if p_extra_work == 1:
        result += '''{
            "name": "Не входящее в минимальный перечень Ставка",
            "data":  [''' + v_data_stavka_o + '''],
            "stack": "Ставка<br>платы",
            "color": "#''' + v_color_o + '''"
        },'''

    result += '''{
        "name": "Начислено",
        "data":  [''' + v_data_stavka_by_report + '''],
        "stack": "Начислено<BR>отчёт",
        "color": "#385C54"
    },'''


 
    result += '''{
        "name": "Конструктивные элементы Отчёт",
        "data": [''' + v_data_report_k + '''],
        "stack": "Отчёт",
        "color": "#''' + v_color_k + '''"
    }, {
        "name": "Инженерия Отчёт",
        "data":  [''' + v_data_report_e + '''],
        "stack": "Отчёт",
        "color": "#''' + v_color_e + '''"
    }, {
        "name": "Прочее имущество Отчёт",
        "data":  [''' + v_data_report_c + '''],
        "stack": "Отчёт",
        "color": "#'''+ v_color_c + '''"
    }, {
        "name": "Управление Отчёт",
        "data":  [''' + v_data_report_m + '''],
        "stack": "Отчёт",
        "color": "#'''+ v_color_m + '''"
    }'''
    
    
    if v_report_sum_u:
        result += ''', {
        "name": 'Недетализированные работы',
        "data":  [''' + v_data_report_u + '''],
        "stack": "Отчёт",
        "color": "#c0c0c0"
        }''' 
    
    if p_extra_work == 1:
        result += ''', {
        "name": "Не входящее в минимальный перечень Отчёт",
        "data":  [''' + v_data_report_o + '''],
        "stack": "Отчёт",
        "color": "#'''+ v_color_o + '''"
        }''' 
    
    
    result += ']},'


# накопительным  итогом

    result +=  '{"macro_sum":['

    if v_stavka_total > 0:
    
        result += '''{
        "name": "Конструктивные элементы Ставка",
        "data": [''' + v_data_stavka_k_sum + '''],
        "stack": "Ставка<br>платы",
        "color": "#'''+ v_color_k + '''"
    }, {
        "name": "Инженерия Ставка",
        "data":  [''' + v_data_stavka_e_sum + '''],
        "stack": "Ставка<br>платы",
        "color": "#'''+ v_color_e + '''"
    }, {
        "name": "Прочее имущество Ставка",
        "data":  [''' + v_data_stavka_c_sum + '''],
        "stack": "Ставка<br>платы",
        "color": "#''' + v_color_c + '''"
    }, {
        "name": "Управление Ставка",
        "data":  [''' + v_data_stavka_m_sum + '''],
        "stack": "Ставка<br>платы",
        "color": "#'''+ v_color_m + '''"
    }, '''
    
    if v_stavka_sum_u:
        result += '''{
            "name": "Недетализированные работы",
            "data":  [''' + v_data_stavka_u_sum + '''],
            "stack": "Ставка<br>платы",
            "color": "#c0c0c0"
        },'''
    
    if p_extra_work == 1:
        result += '''{
            "name": "Не входящее в минимальный перечень Ставка",
            "data":  [''' + v_data_stavka_o_sum + '''],
            "stack": "Ставка<br>платы",
            "color": "#'''+ v_color_o + '''"
        },'''

    result += '''{
        "name": "Начислено",
        "data":  [''' + v_data_stavka_by_report_sum + '''],
        "stack": "Начислено<br>отчёт",
        "color": "#385C54"
    },'''



    result += '''{ "name": "Конструктивные элементы Отчёт", "data": [''' + v_data_report_k_sum + '''], "stack": "Отчёт", "color": "#'''+ v_color_k + '''" }, 
                 { "name": "Инженерия Отчёт", "data":  [''' + v_data_report_e_sum + '''], "stack": "Отчёт", "color": "#'''+ v_color_e + '''" }, 
                 { "name": "Прочее имущество Отчёт", "data":  [''' + v_data_report_c_sum + '''], "stack": "Отчёт", "color": "#''' + v_color_c + '''" }, 
                 { "name": "Управление Отчёт", "data":  [''' + v_data_report_m_sum + '''], "stack": "Отчёт", "color": "#'''+ v_color_m + '''"  }''' 

    if v_report_sum_u:
        result += ''', { "name": "Недетализированные работы", "data":  [''' + v_data_report_u_sum + '''], "stack": "Отчёт", "color": "#c0c0c0"}''' 


    if p_extra_work == 1:
        result += ''', { "name": "Не входящее в минимальный перечень Отчёт", "data":  [''' + v_data_report_o_sum + '''], "stack": "Отчёт", "color": "#''' + v_color_o + '''" }'''  

    result += ']'
    result += '}]'
  

    
    
# текущие ремонты {





    if v_tr_count:
  
        # это версия для печати
#         if v_page_id == 21: 
#             result_tr += '''
#   <p style="page-break-before: always">&nbsp</p>
#   <div align="center">          <h2>        Макропоказатели выполнения текущих ремонтов    </h2></div>'''
    
        # это версия для сайта
        # else:
        result_tr += '''<div class="block-header"><center><h2>Макропоказатели выполнения текущих ремонтов    </h2></center></div>'''
    
    

        result_tr += '''
  <div id="container_repair"></div>
  <div id="container_repair_sum"></div>
  <script>
  Highcharts.chart('container_repair', {

    chart: {type: 'column', bakgroundColor:'transparent'},
    title: {text: 'Текущие ремонты по отчётам. Работы, которые можно отнести к текущим ремонтам. Работы, подтверждённые актами выполненных работ. Ставка платы на текущие ремонты (при наличии).<br>По годам.'},
    xAxis: {categories: [''' + v_series + ''']},
    yAxis: {
        allowDecimals: false,
        min: 0,
        title: { text: 'руб.' },
        stackLabels: {
           enabled: true,
           verticalAlign: 'top',
           //crop: false,
           formatter: function() {return this.stack;},
           style: {fontSize: '8px'}
        }
    },
    
    tooltip: {
        formatter: function () {
            return '<b>' + this.x + ' год</b><br/>' +  this.series.name + ': ' + (this.y).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' руб.<br/>' + 'Итого: ' + (this.point.stackTotal).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' руб.';
        }
    },

    plotOptions: {
        column: {
            stacking: 'normal'
        }
    },

    series: ['''
    
    
    if v_stavka_total_tr > 0:
        result_tr += '''{
                name: 'Ставка',
                data: [' + v_data_stavka_tr + '],
                stack: 'Ставка<br>платы',
                color: '#''' + v_color1 + ''''
            }, '''
     
        result_tr += '''{
        name: 'Конструктивные элементы Отчёт',
        data: [''' + v_data_report_k_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#'''+ v_color_k + ''''
    },
    {
        name: 'Инженерия Отчёт',
        data: [''' + v_data_report_e_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#''' + v_color_e + ''''
    },
    {
        name: 'Прочее имущество Отчёт',
        data: [''' + v_data_report_c_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#''' + v_color_c + ''''
    },
    {
        name: 'Не входящее в минимальный перечень Отчёт',
        data: [''' + v_data_report_n_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#''' + v_color_n + ''''
    },'''
    
    
    # if v_report_k_sum_ozhkh_tr,0) + v_report_e_sum_ozhkh_tr,0) + v_report_c_sum_ozhkh_tr,0) + v_report_n_sum_ozhkh_tr,0) > 0:
    
    # result_tr += '''{
    #     name: 'Конструктивные элементы Анализ',
    #     data: [' + v_data_report_k_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_k + ''
    # },
    # {
    #     name: 'Инженерия Анализ',
    #     data: [' + v_data_report_e_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_e + ''
    # },
    # {
    #     name: 'Прочее имущество Анализ',
    #     data: [' + v_data_report_c_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_c + ''
    # },
    # {
    #     name: 'Не входящее в минимальный перечень Анализ',
    #     data: [' + v_data_report_n_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_n + ''
    # },'''
    # end if
    
    #     if v_document_sum_tr > 0:
    #         result_tr += '''{
    #     name: 'Текущий ремонт Подтверждено',
    #     data: [' + v_data_document_tr + '],
    #     stack: 'Подтверждено',
    #     pointPadding: 0.3,
    #     pointPlacement: -0.2,
    #     color: '#'+ v_color3 + ''
    # }'''
    
    
    
        result_tr += ''']
});'''



# накопительным итогом




        result_tr_sum += '''Highcharts.chart('container_repair_sum', {

    chart: {type: 'column', bakgroundColor:'transparent'},
    title: {text: 'Текущие ремонты по отчётам. Работы, которые можно отнести к текущим ремонтам. Работы, подтверждённые актами выполненных работ. Ставка платы на текущие ремонты (при наличии).<br>Накопительным итогом'},
    xAxis: {categories: [''' + v_series + ''']},
    yAxis: {
        allowDecimals: false,
        min: 0,
        title: { text: 'руб.' },
        stackLabels: {
           enabled: true,
           verticalAlign: 'top',
           //crop: false,
           formatter: function() {return this.stack;},
           style: {fontSize: '8px'}
        }
    },
    
    tooltip: {
        formatter: function () {
            return '<b>' + this.x + ' год</b><br/>' +  this.series.name + ': ' + (this.y).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' руб.<br/>' + 'Итого: ' + (this.point.stackTotal).toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ") + ' руб.';
        }
    },

    plotOptions: {
        column: {
            stacking: 'normal'
        }
    },

    series: ['''
    
    
        if v_stavka_total_tr > 0:
    
    
            result_tr_sum += '''{
        name: 'Ставка',
        data: [''' + v_data_stavka_sum_tr + '''],
        stack: 'Ставка<br>платы',
        color: '#''' + v_color1 + ''''
    }, '''
    
    
     
            result_tr_sum += '''{
        name: 'Конструктивные элементы Отчёт',
        data: [''' + v_data_report_k_sum_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#'''+ v_color_k + ''''
    },
    {
        name: 'Инженерия Отчёт',
        data: [''' + v_data_report_e_sum_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#''' + v_color_e + ''''
    },
    {
        name: 'Прочее имущество Отчёт',
        data: [''' + v_data_report_c_sum_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#''' + v_color_c + ''''
    },
    {
        name: 'Не входящее в минимальный перечень Отчёт',
        data: [''' + v_data_report_n_sum_tr + '''],
        stack: 'Отчёт<br>УК',
        color: '#''' + v_color_n + ''''
    },'''
    
    
    # if v_report_k_sum_ozhkh_tr,0) + v_report_e_sum_ozhkh_tr,0) + v_report_c_sum_ozhkh_tr,0) + v_report_n_sum_ozhkh_tr,0) > 0:
    # dbms_lob.append(v_return_data_sum_tr,  '
    # {
    #     name: 'Конструктивные элементы Анализ',
    #     data: [' + v_data_report_k_sum_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_k + ''
    # },
    # {
    #     name: 'Инженерия Анализ',
    #     data: [' + v_data_report_e_sum_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_e + ''
    # },
    # {
    #     name: 'Прочее имущество Анализ',
    #     data: [' + v_data_report_c_sum_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_c + ''
    # },
    # {
    #     name: 'Не входящее в минимальный перечень Анализ',
    #     data: [' + v_data_report_n_sum_ozhkh_tr + '],
    #     stack: 'Анализ<br>Совдом',
    #     color: '#'+ v_color_n + ''
    # },'''
    # end if
    
    
    #     if v_document_sum_tr > 0:
    #         result_tr_sum += '''{

    #     name: 'Текущий ремонт Подтверждено',
    #     data: [''' + v_data_document_sum_tr + '''],
    #     stack: 'Подтверждено',
    #     pointPadding: 0.3,
    #     pointPlacement: -0.2,
    #     color: '#'+ v_color3 + ''
    # }'''
    
    
    
        result_tr_sum += ''']
});

  </script>'''



    return result