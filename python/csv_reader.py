import sys
import csv

output_scr = open("/tmp/csv_reader.scr", "w+")

if len(sys.argv) != 2:
    print "error: invalid number of inputs"
    print "usage: python csv_reader.py [file.csv]"
    sys.exit(1)

device_name = 'MACHXO2-2000'
banks = [[]]

csvpath = sys.argv[1]
with open(csvpath, 'rb') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[0] != '0':
            try:
                bank = int(row[2])+1
            except ValueError:
                if(row[2] != '-'):
                    continue
                bank = 0;
            while bank > len(banks)-1:
                banks.append([])
            if(row[12] == '-'):
                continue
            banks[bank].append((int(row[12]), row[1]))

output_scr.write("edit " + device_name + ".dev\n")
output_scr.write("package TQFP-100 -6TG100\n")

for bank_index in range(0, len(banks)):
    bank = banks[bank_index]
    existing_pins = {''}
    pin_numbers = {}
    pin_position = 0;
    if bank_index == 0:
        output_scr.write("edit " + device_name + "-PWR.sym\n")
    else:
        output_scr.write("edit " + device_name + "-BANK" + str(bank_index-1) + ".sym\n")
    output_scr.write("grid in 0.1\n")
    for pin_index in range(0, len(bank)):
        pin = bank[pin_index]
        try:
            pin_numbers[pin[1]] += ' ' + str(pin[0])
        except KeyError:
            pin_numbers[pin[1]] = str(pin[0])
        if pin[1] in existing_pins:
            continue
        existing_pins |= {pin[1]}
        output_scr.write("pin '" + pin[1] + "' (0 " + str(pin_position) + ")\n")
        pin_position += 0.1
    output_scr.write("edit " + device_name + ".dev\n")
    if bank_index == 0:
        output_scr.write("add " + device_name + "-PWR G" + str(bank_index+1) + " (" + str(bank_index) + " 0)\n")
    else:
        output_scr.write("add " + device_name + "-BANK" + str(bank_index-1) + " G" + str(bank_index+1) + " (" + str(bank_index) + " 0)\n")
    existing_pins = {''}
    for pin_index in range(0, len(bank)):
        pin = bank[pin_index]
        if pin[1] in existing_pins:
            continue
        existing_pins |= {pin[1]}
        output_scr.write("connect G" + str(bank_index+1) + "." + pin[1] + " '" + pin_numbers[pin[1]] + "'\n")
    

#output_scr.write("attribute DIST_NAME '" + DIST_NAME + "'\n")
#output_scr.write("attribute DIST_PN '" + DIST_PN + "'\n")
#output_scr.write("attribute MFG_NAME '" + MFG_NAME + "'\n")
#output_scr.write("attribute MFG_PN '" + MFG_PN + "'\n")
#output_scr.write("description '" + DESC + "'\n")

output_scr.close()
