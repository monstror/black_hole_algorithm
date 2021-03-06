import random as r
import math as m
import statistics as st
import time as t

size = 100       #размерность популяции
coor_min = 0     #область поиска (минимум)
coor_max = 0     #область поиска (максимум)
dim = 2          #мерность координат
bh_rad = 0       #радиус черной дыры
time_end = 1     #время работы (в минутах)
iter_num = 10    #количество повторений каждой фукнции
time_arr = (3, 5, 15) #время прогона 
dim_arr = (5, 10, 50) #мерность
fit_name = {1:'Bent Cigar',2:'Discus',3:'Rastrigin',4:'Rosenbrok',5:'Sphere',6:'Schwefel'}
coor = ((-5,5),(-5,5),(-5.12,5.12),(-5,10),(-100,100),(-500,500)) 


def gen_coor(): #генерация координат
    a = []
    for i in range(dim):
        a.append(r.uniform(coor_min,coor_max))
    return a

def fit_ev(x, num): #функция cigar
    if num == 1:
        return x[0]**2 + 10**6 * sum([(x[i]**2) for i in range(1, dim)]) #cigar
    if num == 2:
        return (10**6)*x[0]**2 + sum([(x[i]**2) for i in range(1, dim)]) #discus
    if num == 3:
        return 10*dim + sum([((x[i])**2 - 10 * m.cos(2 * m.pi * x[i])) for i in range(dim)]) #rastrigin
    if num == 4:
        return sum([(100*(x[i]**2 - x[i+1])**2 + (x[i] - 1)**2) for i in range(dim-1)]) #rosenbrok
    if num == 5:
        return sum([(x[i]**2) for i in range(dim)]) #sphere
    if num == 6:
        return 418.9829*dim - sum([(x[i]*m.sin(m.sqrt(abs(x[i])))) for i in range(0, dim)])

def radius(bh, st):  #проверка на вхождение за горизонт событий
    a = m.sqrt(sum([((bh[i]-st[i])**2) for i in range(dim)]))
    if a < bh_rad:
        return 1
    else:
        return 0

for fit_num in sorted(fit_name):
    for var_num in range(1,iter_num):
        print(fit_name[fit_num], var_num)
        print('_________________________')
        for dim in dim_arr:
            for time_end in time_arr:
                coor_min = coor[fit_num-1][0]
                coor_max = coor[fit_num-1][1]

                print(fit_name[fit_num],' dim =',dim,' time =',time_end)
                print('(',coor_min,',',coor_max,')')

                r.seed()
                star = [] #список координат звезд
                fit = []  #список значений фитнес функций

                for i in range(size): #генерация звезд и расчет значений фитнес функций
                    star.append(gen_coor())
                    fit.append(fit_ev(star[i],fit_num))  
                bh_i = fit.index(min(fit)) #находим минимальное значение фитнес функции
                bh_fit = fit.pop(bh_i) #достаем значение фитнес функции будущей черной дыры
                black_hole = star.pop(bh_i) #достаем координаты будущей черной дыры
                bh_rad = bh_fit / sum(fit) #рассчитываем радиус горизонта событий
                gen = 1
                flag = gen
                timer = t.time()
                while t.time() - timer < time_end * 60:
                    for i in range(size-1): 
                        rand = r.random() #генерируем рандомное значение для шума
                        for j in range(dim):
                            star[i][j] = star[i][j] + rand * (black_hole[j] - star[i][j]) #изменяем положение звезды в пространстве
                        if radius(black_hole, star[i]) == 1: #если звезда попала в горизонт событий
                            star[i] = gen_coor() #создаем новую звезду
                        fit[i] = fit_ev(star[i],fit_num)
                    if min(fit) < bh_fit:           #если минимальная из полученных фитнес функций меньше фитнес функции черной дыры
                        bh_i = fit.index(min(fit))
                        fit.append(bh_fit)
                        bh_fit = fit.pop(bh_i)
                        star.append(black_hole)
                        black_hole = star.pop(bh_i)
                        bh_rad = (bh_fit / sum(fit))
                        flag = gen
                    gen += 1

                print('Best solution founded on', flag,'generation (total',gen,'generations)')
                print('Black fit = ',bh_fit,'\n')
