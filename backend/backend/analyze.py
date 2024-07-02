# возвращает оптимальную стоммость обследований
def get_optimum_inspection_price (build):
    result = build.q_porchs * 5000 
    if result < 40000:
        result = 40000
    return result / build.s() / 12