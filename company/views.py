from django.shortcuts import render, redirect
from django.utils.text import slugify as django_slugify
from .models import *
from city.models import City
import os
import json
import re
from datetime import datetime

# Пытаемся использовать python-slugify для транслитерации, если установлен
try:
    from slugify import slugify as python_slugify
    # Используем python-slugify - он автоматически транслитерирует русский текст
    slugify = python_slugify
except ImportError:
    slugify = django_slugify

def company_list(request):
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return render(request, 'company/company_list.html', context)



def par(request):
    categories = Category.objects.prefetch_related('subcategories').order_by('name')
    
    # Группируем категории с подкатегориями
    category_hierarchy = {}
    for category in categories:
        category_hierarchy[category] = category.subcategories.all().order_by('name')
    
    cities = City.objects.select_related('region').order_by('region__name', 'name')
    
    # Группируем города по регионам (без округов)
    city_hierarchy = {}
    for city in cities:
        region = city.region
        
        if region.name not in city_hierarchy:
            city_hierarchy[region.name] = []
        
        city_hierarchy[region.name].append(city)

    path = "company/work_data/"
    cat_data = []

    try:
        if os.path.exists(path):
            dir_list = os.listdir(path)
            for item in dir_list:
                try:
                    item_cat = item.split('.')[0].strip()
                    parts = item_cat.split('_')
                    if len(parts) >= 2:
                        quantity = parts[1].strip()
                        if quantity.isdigit() and int(quantity) > 0:
                            cat_data.append(item)
                except (ValueError, IndexError):
                    continue
    except OSError:
        pass  # Директория не существует или нет доступа

    context = {
        "city_hierarchy": city_hierarchy,
        "category_hierarchy": category_hierarchy, 
        "cat_data": cat_data, 
        #"all_cat": i
        }
    return render(request, 'company/par.html', context)


# Запускаем добавление компаний в категорию
def form_company(request):
    if request.method == 'POST':
        data = request.POST
        id_subcat = data.get("id_subcat")
        id_city = data.get("id_city")
        cat = data.get("cat")

        if not id_subcat or not id_city or not cat:
            return redirect('par')

        path = "company/work_data/"
        
        # Извлекаем название файла без подчеркивания, цифр и расширения
        # Например: "category_100.json" -> "category"
        file_name_clean = cat.split('.')[0].strip()  # Убираем расширение
        if '_' in file_name_clean:
            file_name_clean = file_name_clean.split('_')[0].strip()  # Берем часть до первого подчеркивания
        
        # Проверяем, не был ли файл уже обработан
        if ProcessedFile.objects.filter(file_name=file_name_clean).exists():
            # Файл уже обработан, логируем и удаляем его
            log_path = "company/logs/"
            os.makedirs(log_path, exist_ok=True)
            log_file = os.path.join(log_path, f"{file_name_clean}.log")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                with open(log_file, "a", encoding='utf-8') as f:
                    f.write(f"[{timestamp}] [WARNING] Файл уже был обработан ранее. Пропуск.\n")
            except:
                pass
            try:
                os.remove(path + cat)
            except:
                pass
            return redirect('par')
        
        try:
            # Получаем подкатегорию по ID
            subcategory = Subcategory.objects.get(id=id_subcat)
        except Subcategory.DoesNotExist:
            return redirect('par')

        try:
            # Получаем город по ID
            city = City.objects.get(id=id_city)
        except City.DoesNotExist:
            return redirect('par')

        # Читаем JSON файл
        try:
            with open(path + cat, "r", encoding='utf-8') as read_file:
                data_json = json.load(read_file)
        except FileNotFoundError:
            return redirect('par')

        # Настраиваем логирование
        log_path = "company/logs/"
        os.makedirs(log_path, exist_ok=True)
        log_file = os.path.join(log_path, f"{file_name_clean}.log")
        
        # Счетчики для статистики
        success_count = 0
        duplicate_count = 0
        error_count = 0
        
        def write_log(message, log_type="INFO"):
            """Записывает сообщение в лог-файл"""
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{timestamp}] [{log_type}] {message}\n"
            try:
                with open(log_file, "a", encoding='utf-8') as f:
                    f.write(log_message)
            except:
                pass
        
        # Начало обработки
        write_log(f"Начало обработки файла: {cat}")
        write_log(f"Подкатегория: {subcategory.name} (ID: {subcategory.id})")
        write_log(f"Город: {city.name} (ID: {city.id})")
        write_log(f"Всего компаний в файле: {len(data_json)}")
        write_log("-" * 80)

        # Обрабатываем каждую компанию из файла
        for item_company in data_json:
            try:
                # Подготовка данных компании
                name = item_company.get("company", "").strip()
                if not name:
                    continue  # Пропускаем, если нет названия

                # Адрес
                address = item_company.get("adress", "").strip()

                # Получаем email - берем только первый, если их несколько
                emails = item_company.get("emails", [])
                email = ''
                if isinstance(emails, list) and len(emails) > 0:
                    email = str(emails[0]).strip()
                elif emails:
                    email_str = str(emails).replace("['", '').replace("']", '').replace("'", '').strip()
                    # Если email пришел как строка с несколькими через запятую, берем только первый
                    if email_str:
                        email = email_str.split(',')[0].strip()

                # Получаем телефоны как список
                phones = item_company.get("phones", [])
                phone_list = []
                if isinstance(phones, list) and len(phones) > 0:
                    phone_list = [str(p).strip() for p in phones if p and str(p).strip()]
                elif phones:
                    # Если телефон пришел как строка, парсим его
                    phone_str = str(phones).replace("['", '').replace("']", '').replace("'", '').strip()
                    if phone_str:
                        phone_list = [p.strip() for p in phone_str.split(',') if p.strip()]
                
                # Для проверки дубликатов используем первый телефон
                phone_for_check = phone_list[0] if phone_list else None
                
                # Проверка на дубликаты
                is_duplicate = False
                duplicate_reason = ""
                
                # 1. Проверка по email (если есть)
                if email:
                    if Company.objects.filter(email=email).exists():
                        is_duplicate = True
                        duplicate_reason = f"по email: {email}"
                
                # 2. Проверка по названию + адрес + город (основная проверка)
                if not is_duplicate:
                    duplicate_query = Company.objects.filter(
                        name__iexact=name,
                        city=city
                    )
                    if address:
                        duplicate_query = duplicate_query.filter(address__iexact=address)
                    
                    if duplicate_query.exists():
                        is_duplicate = True
                        duplicate_reason = f"по названию '{name}' в городе '{city.name}'"
                        if address:
                            duplicate_reason += f" и адресу '{address}'"
                
                # 3. Дополнительная проверка по телефону (если есть и другие проверки не сработали)
                if not is_duplicate and phone_for_check:
                    # Проверяем, есть ли компании с таким телефоном в этом городе
                    # Ищем в JSONField через __contains
                    if Company.objects.filter(phone__contains=[phone_for_check], city=city).exists():
                        is_duplicate = True
                        duplicate_reason = f"по телефону '{phone_for_check}' в городе '{city.name}'"
                
                # Пропускаем, если найден дубликат
                if is_duplicate:
                    duplicate_count += 1
                    write_log(f"ДУБЛИКАТ ПРОПУЩЕН: {name} - {duplicate_reason}", "DUPLICATE")
                    continue

                # Генерируем slug из названия компании
                name_slug = slugify(name)
                # Если после slugify получилась пустая строка, используем название напрямую
                if not name_slug or name_slug.strip() == '':
                    # Преобразуем название в slug вручную
                    # Приводим к нижнему регистру, заменяем пробелы и спецсимволы на дефисы
                    name_slug = name.lower().strip()
                    # Заменяем пробелы и множественные спецсимволы на дефисы
                    name_slug = re.sub(r'[^\w\s-]', '', name_slug)  # Удаляем спецсимволы
                    name_slug = re.sub(r'[-\s]+', '-', name_slug)  # Заменяем пробелы и дефисы на один дефис
                    name_slug = name_slug.strip('-')  # Убираем дефисы в начале и конце
                    # Ограничиваем длину
                    name_slug = name_slug[:100] if len(name_slug) > 100 else name_slug
                    # Если всё равно пусто, используем первые символы названия
                    if not name_slug:
                        name_slug = name[:50].lower().replace(' ', '-')
                        name_slug = re.sub(r'[^\w-]', '', name_slug)
                        if not name_slug:
                            name_slug = 'company'
                
                # Телефон уже получен выше при проверке дубликатов
                
                # Вид деятельности
                type_work = item_company.get("type_work", "").strip()

                # Режим работы
                work_time = item_company.get("time_work", "").strip()

                # Социальные сети (сохраняем как список)
                social_link = item_company.get("social_link", "")
                social_link_list = []
                if isinstance(social_link, list):
                    social_link_list = [str(s).strip() for s in social_link if s and str(s).strip()]
                elif social_link:
                    social_link_str = str(social_link).replace("['", '').replace("']", '').replace("'", '').strip()
                    if social_link_str:
                        social_link_list = [s.strip() for s in social_link_str.split(',') if s.strip()]

                # Сайт - берем только первый, если их несколько
                sites_link = item_company.get("sites_link", "")
                website = None
                if isinstance(sites_link, list) and len(sites_link) > 0:
                    website = str(sites_link[0]).strip()
                elif sites_link:
                    website_str = str(sites_link).replace("['", '').replace("']", '').replace("'", '').strip()
                    # Если сайт пришел как строка с несколькими через запятую, берем только первый
                    if website_str:
                        website = website_str.split(',')[0].strip()
                        # Убираем протоколы для отображения в описании, но сохраняем полный URL
                        if website and not website.startswith(('http://', 'https://')):
                            website = 'https://' + website

                # Карта - ссылка
                map_url = item_company.get("map_link", "").strip()

                # Карта - координаты
                map_zn = item_company.get("map_zn", "")
                if isinstance(map_zn, list):
                    map_zn = ', '.join(str(m).strip() for m in map_zn if m)
                else:
                    map_zn = str(map_zn).replace("['", '').replace("']", '').replace("'", '').strip()

                # Услуги (сохраняем как список)
                uslugi = item_company.get("uslugi", "")
                uslugi_list = []
                if isinstance(uslugi, list):
                    uslugi_list = [str(u).strip() for u in uslugi if u and str(u).strip()]
                elif uslugi:
                    uslugi_str = str(uslugi).replace("['", '').replace("']", '').replace("'", '').strip()
                    if uslugi_str:
                        uslugi_list = [u.strip() for u in uslugi_str.split(',') if u.strip()]

                # Описание
                description = item_company.get("description", "")
                if not description or description.strip() == '':
                    # Формируем описание автоматически
                    description_parts = [f'<p>Компания "{name}"']
                    if address:
                        description_parts.append(f'располагается по адресу: {address}')
                    description_parts.append('.</p>')
                    
                    if uslugi_list:
                        uslugi_str = ', '.join(uslugi_list)
                        description_parts.append(f'<p>Компания {name} предлагает вам свои товары и услуги:</p>')
                        description_parts.append(f'<p>{uslugi_str}</p>')
                    
                    if phone_list:
                        phones_str = ', '.join(phone_list)
                        description_parts.append(f'<p>На все вопросы вам ответят по телефону {phones_str}.</p>')
                    
                    if website:
                        website_clean = website.replace('https://', '').replace('http://', '')
                        description_parts.append(f'<p>Более полную информацию смотрите на нашем сайте {website_clean}.</p>')
                    
                    description = ''.join(description_parts)
                else:
                    description = str(description).replace("/n", '<br />')

                # Создаем компанию
                company = Company(
                    name=name,
                    subcategory=subcategory,
                    city=city,
                    address=address,
                    email=email,
                    phone=phone_list if phone_list else [],
                    website=website if website else None,
                    type_work=type_work,
                    work_time=work_time,
                    social_link=social_link_list if social_link_list else [],
                    map_url=map_url,
                    map_zn=map_zn,
                    description=description,
                    uslugi=uslugi_list if uslugi_list else [],
                    slug='',  # Временно пустой, обновим после сохранения с ID
                    status=1,
                    public=True
                )
                company.save()
                
                # Создаем финальный slug с ID компании: nazvanie-kompanii-123
                final_slug = f"{name_slug}-{company.id}"
                # Проверяем уникальность и добавляем счетчик при необходимости
                slug_counter = 0
                while Company.objects.filter(slug=final_slug).exclude(id=company.id).exists():
                    slug_counter += 1
                    final_slug = f"{name_slug}-{company.id}-{slug_counter}"
                
                company.slug = final_slug
                company.save(update_fields=['slug'])
                
                success_count += 1
                write_log(f"УСПЕШНО СОЗДАНА: {name} (ID: {company.id}, Email: {email if email else 'нет'})", "SUCCESS")

            except Exception as e:
                error_count += 1
                error_msg = f"ОШИБКА при создании компании '{name}': {str(e)}"
                write_log(error_msg, "ERROR")
                continue

        # Итоговая статистика
        write_log("-" * 80)
        write_log(f"Обработка завершена")
        write_log(f"Успешно создано: {success_count}")
        write_log(f"Пропущено дубликатов: {duplicate_count}")
        write_log(f"Ошибок: {error_count}")
        write_log(f"Всего обработано: {success_count + duplicate_count + error_count} из {len(data_json)}")
        write_log("=" * 80)
        
        # Создаем запись об обработанном файле
        ProcessedFile.objects.create(
            file_name=file_name_clean,
            subcategory=subcategory
        )
        
        # Удаляем обработанный файл
        try:
            os.remove(path + cat)
        except:
            pass

    return redirect('par')