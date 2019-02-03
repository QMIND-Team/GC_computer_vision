import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    #loop for training images
    for item in ['annies_snickerdoodle_cinnamon_sugar', 'blue_diamond_nut_thins_almond_cheddar', 'blue_diamond_nut_thins_almond_seasalt','higgins_and_burke_naturals_peppermint','hot_kid_rice_crisps_sesame','patels_dal_tadka_lentil_curry']:
        image_path = os.path.join(os.getcwd(), 'Data/train/{}'.format(item))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv('Data/train/{}_labels.csv'.format(item), index=None)
        print('Successfully converted xml to csv.')
    #loop for testing images
    for item in ['annies_snickerdoodle_cinnamon_sugar', 'blue_diamond_nut_thins_almond_cheddar', 'blue_diamond_nut_thins_almond_seasalt','higgins_and_burke_naturals_peppermint','hot_kid_rice_crisps_sesame','patels_dal_tadka_lentil_curry']:
        image_path = os.path.join(os.getcwd(), 'Data/test/{}'.format(item))
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv('Data/test/{}_labels.csv'.format(item), index=None)
        print('Successfully converted xml to csv.')


main()