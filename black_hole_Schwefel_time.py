import random as r
import math as m
import statistics as st
import time as t
from playsound import playsound

size = 100       #размерность популяции
coor_min = -500 #область поиска (минимум)
coor_max = 500  #область поиска (максимум)

dim = 0          #мерность координат
time_end = 0     #время работы (в минутах)
time_arr = (5,)
dim_arr = (2,)

def gen_coor(): #генерация координат
    a = []
    for i in range(dim):
        a.append(r.uniform(coor_min,coor_max))
    return a

def fit_ev(x): #функция 
        return 418.9829*dim - sum([(x[i]*m.sin(m.sqrt(abs(x[i])))) for i in range(0, dim)])

def radius(bh, st):  #проверка на вхождение за горизонт событий
    a = m.sqrt(sum([((bh[i]-st[i])**2) for i in range(dim)]))
    if a < bh_rad:
        return 1
    else:
        return 0

playsound('start.wav')

for dim in dim_arr:
    for time_end in time_arr:
        print('dim=',dim)
        print('time=',time_end)

        r.seed()
        star = [] #список координат звезд
        fit = []  #список значений фитнес функций
        bh_rad = 0       #радиус черной дыры
        bh_fit = 0       #значение фитнес функции черной дыры
        gen = 0          #номер итерации
        bh_i = 0         #номер черной дыры в списке звезд

        for i in range(size): #генерация звезд и расчет значений фитнес функций
            star.append(gen_coor())
            fit.append(fit_ev(star[i]))  
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
                fit[i] = fit_ev(star[i])
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
        print('Black hole coor = ',black_hole)
        print('Black hole fit = ',bh_fit)
        print('time=',(t.time() - timer)/60,'\n')

playsound('end.wav')