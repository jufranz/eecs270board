#!/usr/bin/env python
import pdb
import sys
from xml.etree import ElementTree

def elements_equal(e1, e2):
    return (ElementTree.tostring(e1) == ElementTree.tostring(e2))
    #if type(e1) != type(e2): return False
    #if e1.tag != e1.tag: return False
    #if e1.text != e2.text: return False
    #if e1.tail != e2.tail: return False
    #if e1.attrib != e2.attrib: return False
    #if len(e1) != len(e2): return False
    #return all([elements_equal(c1, c2) for c1, c2 in zip(e1, e2)])

def contains_element(o, e):
    for elem in o:
        #print(e.get('name'), elem.get('name'))
        if elements_equal(e, elem):
            return True
    return False

def merge(a, b, o):
    r = a.copy()
    r.extend(b)
    conflict = False
    #print ElementTree.tostring(r)
    for elem1 in r:
        for elem2 in r:
            if elem1 == elem2:
                continue
            if elem1.get('name') == elem2.get('name'):
                # found duplicates
                if elements_equal(elem1, elem2):
                    r.remove(elem2)
                else:
                    if contains_element(o, elem1):
                        r.remove(elem1)
                    elif contains_element(o, elem2):
                        r.remove(elem2)
                    else:
                        conflict = True
                        if contains_element(a, elem1):
                            elem1.set('name', elem1.get('name')+'_CONFLICT_LOCAL')
                            elem2.set('name', elem2.get('name')+'_CONFLICT_BRANCH')
                        else:
                            elem1.set('name', elem1.get('name')+'_CONFLICT_BRANCH')
                            elem2.set('name', elem2.get('name')+'_CONFLICT_LOCAL')
                    #r.remove(elem2)
                    #print(elem1.get('name'), elem2.get('name'))
    return [r, conflict]


def run():
    conflict = False
    tree_a = ElementTree.parse(sys.argv[1])
    root_a = tree_a.getroot()
    root_b = ElementTree.parse(sys.argv[2]).getroot()
    root_o = ElementTree.parse(sys.argv[3]).getroot()
    library = root_a.find('drawing').find('library')
    for typestr in ['packages', 'symbols', 'devicesets']:
        packages_a = root_a.find('drawing').find('library').find(typestr).copy()
        packages_b = root_b.find('drawing').find('library').find(typestr).copy()
        packages_o = root_o.find('drawing').find('library').find(typestr).copy()
        library.remove(library.find(typestr))
        result = merge(packages_a, packages_b, packages_o)
        if(result[1]):
            conflict = True
        library.append(result[0])
    #print ElementTree.tostring(root_a)
    tree_a.write(sys.argv[1])
    exit(-1 if conflict else 0)

#pdb.set_trace()
run()
