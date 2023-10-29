# WICHITG! EINE INITAL CSV IM SELBEN ORDNER WIE DIESES SCRIPT ABLEGEN UND NACH 'InitialExport.csv' BENENNEN


import csv

def extract_value(eigenschaften, key, ean):
    """Extracts the value for a given key from the eigenschaften string."""
    for pair in eigenschaften.split('|'):
        parts = pair.split(':')
        k = parts[0]
        v = ':'.join(parts[1:]).replace('ca. ', '')  # Ensure 'ca.' is always removed

        if k == key:
            if k in ['Breite', 'Höhe', 'Tiefe', 'Durchmesser']:
                v = v.replace(' cm', '')  # Move this line out of the if '.' in v: block
                if '.' in v:
                    values = v.split('.')
                    try:
                        v = str(sum([float(val.replace(',', '.')) for val in values]) / len(values))
                    except ValueError:
                        print(f"Error converting value '{v}' for key '{k}' in EAN {ean}.")
                        return None

                try:
                    val_float = float(v.replace(',', '.')) * 10  # Convert cm to mm
                    if val_float == int(val_float):  # Check if it's a whole number
                        v = str(int(val_float))
                    else:
                        v = str(val_float)
                    if v == '0':  # Check for 0 value
                        return None
                    return v  # Return as string
                except ValueError:
                    print(f"Error converting value '{v}' for key '{k}' in EAN {ean}.")
                    return None
            elif k in ['Leistung', 'Helligkeit', 'Farbtemperatur']:
                v = v.replace(' Watt', '').replace(' Lumen', '').replace('Kelvin', '')
                try:
                    val_float = float(v.replace(',', '.'))
                    if val_float == int(val_float):  # Check if it's a whole number
                        v = str(int(val_float))
                    else:
                        v = str(val_float)
                    if v == '0':  # Check for 0 value
                        return None
                    return v
                except ValueError:
                    print(f"Error converting value '{v}' for key '{k}' in EAN {ean}.")
                    return None
            else:
                if v == '0':  # Check for 0 value
                    return None
                return v
    return None








def replace_special_chars(text):
    """Replaces special German characters."""
    replacements = {
        'ß': 'ss',
        'ü': 'ue',
        'ö': 'oe',
        'ä': 'ae',
        'Ü': 'Ue',
        'Ö': 'Oe',
        'Ä': 'Ae'
    }

    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text



def process_farbe_value(farbe):
    """Process the farbe value to either lowercase or keep specific values with uppercase first letter."""
    exceptions = ["Mehrfarbig", "Anthrazit"]  # Add any other exceptions here
    if farbe in exceptions:
        return farbe
    return farbe.lower()


with open('InitialExport.csv', 'r') as csvFile:
    reader = csv.DictReader(csvFile)

    with open('Blomus_Import_New.csv', 'w') as newFile:
        fieldnames = ['sku', 'categories', 'enabled', 'family', 'modell', 'bauform', 'Hersteller', 'preis_vk-mylivings-EUR', 'ek_preis-EUR', 'uvp-EUR', 'color', 'Geraetebreite_mm', 'Geraetehoehe_mm', 'Geraetetiefe_mm', 'durchmesser', 'groups', 'Gewicht_kg', 'fassung', 'Energieeffizienzklasse', 'energie_leuchten', 'Energylabel_image', 'leistung_watt_num', 'Leuchtenart', 'Leuchtmittel_austauschbar', 'leuchtmittel_im_lieferumfang', 'lichtfarbe', 'lichtfarbe_kelvin', 'lichtstrom_in_lumen', 'lieferant', '2_bild', '3_bild', '4_bild', '5_bild', '6_bild', '7_bild', 'auslaufartikel', 'bild_1', 'breite_verpackt', 'comment', 'delete', 'description', 'dimmbar', 'ecoro_id', 'export_plenty', 'export_shopware', 'form', 'geraetebreite_verpackt_mm', 'geraetehoehe_verpackt_mm', 'Geraetetiefe_verpackt_mm', 'Gestell', 'Gestellfarbe', 'gewichtNetto_kg', 'Highlights', 'hoehe_max', 'hoehe_verpackt', 'idealo-mylivings', 'idealo_direktkauf-mylivings', 'item_state', 'klappbar', 'lieferumfang', 'Lieferzustand', 'manual', 'mark', 'material', 'material_gestell', 'measure_image', 'measure_image_2', 'measure_image_3', 'measure_image_4', 'measure_image_5', 'measure_image_6', 'meta_desc-mylivings', 'meta_titel-mylivings', 'Mindestabnahme', 'min_vk-EUR', 'ModelNrHersteller', 'montage', 'name-de_DE-mylivings', 'panelImage', 'plenty_varianten_id', 'produktblatt', 'produktserie', 'produktvideo', 'schutzart', 'schutzklasse', 'short_desc', 'Sitzkapa', 'Staffelung', 'std_wiederauffuellzeit', 'stil', 'sw_id', 'tiefe_verpackt', 'top_feature_01', 'top_feature_02', 'top_feature_03', 'top_feature_04', 'top_feature_05', 'url', 'verkaufsprogramm', 'versandart', 'wireless_bluetooth', 'zuleitungslaenge']

        writer = csv.DictWriter(newFile, fieldnames=fieldnames)
        
        writer.writeheader()

        for line in reader:
            if line['Hersteller'] == 'blomus':
                farbe_extracted = extract_value(line['Eigenschaften'], 'Farbe', line['EAN'])
                farbe_value = process_farbe_value(replace_special_chars(farbe_extracted)) if farbe_extracted else None
                breite_value = extract_value(line['Eigenschaften'], 'Breite', line['EAN'])
                hoehe_value = extract_value(line['Eigenschaften'], 'Höhe', line['EAN'])
                tiefe_value = extract_value(line['Eigenschaften'], 'Tiefe', line['EAN'])
                durchmesser_value = extract_value(line['Eigenschaften'], 'Durchmesser', line['EAN'])
                leistung_value = extract_value(line['Eigenschaften'], 'Leistung', line['EAN'])
                lichtstrom_value = extract_value(line['Eigenschaften'], 'Helligkeit', line['EAN'])
                lichtfarbe_value = extract_value(line['Eigenschaften'], 'Farbtemperatur', line['EAN'])
                fassung_value = extract_value(line['Eigenschaften'], 'Leuchtmitteltyp', line['EAN'])

                leuchtmittel_value = extract_value(line['Eigenschaften'], 'Leuchtmittel fest verbaut', line['EAN'])
                leuchtmittel_processed = '1' if leuchtmittel_value and leuchtmittel_value.lower() == 'ja' else '0'

                material_value = extract_value(line['Eigenschaften'], 'Materialunterart', line['EAN'])

                dimmbar_value = extract_value(line['Eigenschaften'], 'Verstellbarkeit und Funktion', line['EAN'])
                dimmbar_processed = '1' if dimmbar_value and 'dimmbar' in dimmbar_value.lower() else '0'



                writer.writerow({'sku': line['EAN'], 
                                 'Hersteller': line['Hersteller'], 
                                 'preis_vk-mylivings-EUR': line['Produktpreis'], 
                                 'modell': line['Produktname'], 
                                 'Geraetebreite_mm': breite_value, 
                                 'Geraetehoehe_mm': hoehe_value, 
                                 'Geraetetiefe_mm': tiefe_value,
                                 'durchmesser': durchmesser_value, 
                                 'color': farbe_value,
                                 'enabled': '0',
                                 'leistung_watt_num': leistung_value,
                                 'lichtstrom_in_lumen': lichtstrom_value,
                                 'lichtfarbe_kelvin': lichtfarbe_value,
                                 'fassung': fassung_value,
                                 'leuchtmittel_im_lieferumfang': leuchtmittel_processed,
                                 'material': material_value,
                                 'dimmbar': dimmbar_processed,
                                 })
